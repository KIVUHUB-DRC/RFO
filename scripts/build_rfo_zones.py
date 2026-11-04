#!/usr/bin/env python3
"""Build a 2 km October 2026 Sentinel-2 NDVI screening grid for the RFO."""

import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np
import planetary_computer
import rasterio
import requests
from pyproj import Transformer
from rasterio.enums import Resampling
from rasterio.features import geometry_mask
from rasterio.transform import Affine
from rasterio.windows import Window, from_bounds
from shapely.geometry import box, mapping, shape
from shapely.ops import transform as transform_geometry


ROOT = Path(__file__).resolve().parents[1]
BOUNDARY = ROOT / "data" / "raw" / "RFO Limit.json"
OUTPUT = ROOT / "data" / "processed" / "RFO_Oct2026_NDVI_Zones.geojson"
STAC = "https://planetarycomputer.microsoft.com/api/stac/v1"
PIXEL_M = 100
ZONE_M = 2_000
MONTH = "2026-10"


def fetch_october_items(aoi):
    session = requests.Session()
    body = {
        "collections": ["sentinel-2-l2a"],
        "intersects": aoi,
        "datetime": "2026-10-01T00:00:00Z/2026-10-31T23:59:59Z",
        "limit": 100,
    }
    response = session.post(f"{STAC}/search", json=body, timeout=90)
    response.raise_for_status()
    document = response.json()
    items = list(document.get("features", []))
    while True:
        next_link = next(
            (link for link in document.get("links", []) if link.get("rel") == "next"),
            None,
        )
        if not next_link:
            break
        response = session.post(
            next_link["href"], json=next_link.get("body", {}), timeout=90
        )
        response.raise_for_status()
        document = response.json()
        items.extend(document.get("features", []))
    return items


def nearest_clear_scenes(items):
    tiles = defaultdict(list)
    for item in items:
        props = item["properties"]
        tiles[props.get("s2:mgrs_tile", "unknown")].append(item)
    return sorted(
        (
            min(
                scenes,
                key=lambda item: (
                    item["properties"].get("eo:cloud_cover", 100),
                    item["properties"]["datetime"],
                ),
            )
            for scenes in tiles.values()
        ),
        key=lambda item: item["properties"].get("eo:cloud_cover", 100),
    )


def read_at_100m(asset, transform, width, height, window, resampling):
    with rasterio.open(asset) as dataset:
        with rasterio.vrt.WarpedVRT(
            dataset,
            crs=dataset.crs,
            transform=transform,
            width=width,
            height=height,
            resampling=resampling,
        ) as warped:
            return warped.read(1, window=window)


def main():
    feature = json.loads(BOUNDARY.read_text())["features"][0]
    reserve = shape(feature["geometry"])
    to_utm = Transformer.from_crs(4326, 32635, always_xy=True).transform
    reserve_utm = transform_geometry(to_utm, reserve)
    min_x, min_y, max_x, max_y = reserve_utm.bounds

    left = math.floor(min_x / ZONE_M) * ZONE_M
    top = math.ceil(max_y / ZONE_M) * ZONE_M
    width = math.ceil((max_x - left) / PIXEL_M)
    height = math.ceil((top - min_y) / PIXEL_M)
    width = math.ceil(width / (ZONE_M // PIXEL_M)) * (ZONE_M // PIXEL_M)
    height = math.ceil(height / (ZONE_M // PIXEL_M)) * (ZONE_M // PIXEL_M)
    transform = Affine(PIXEL_M, 0, left, 0, -PIXEL_M, top)

    items = fetch_october_items(mapping(reserve.simplify(0.003, preserve_topology=True)))
    scenes = nearest_clear_scenes(items)
    if not scenes:
        raise RuntimeError("No Sentinel-2 L2A items found for October 2026.")

    ndvi_mosaic = np.full((height, width), np.nan, dtype=np.float32)
    evi_mosaic = np.full((height, width), np.nan, dtype=np.float32)

    for item in scenes:
        intersection = reserve.intersection(shape(item["geometry"]))
        if intersection.is_empty:
            continue
        intersection = transform_geometry(to_utm, intersection)
        signed = planetary_computer.sign(item)
        with rasterio.open(signed["assets"]["B04"]["href"]) as red_ds:
            bounds = red_ds.bounds
            tile_left = math.floor(bounds.left / PIXEL_M) * PIXEL_M
            tile_top = math.ceil(bounds.top / PIXEL_M) * PIXEL_M
            tile_width = math.ceil((bounds.right - tile_left) / PIXEL_M)
            tile_height = math.ceil((tile_top - bounds.bottom) / PIXEL_M)
            tile_transform = Affine(PIXEL_M, 0, tile_left, 0, -PIXEL_M, tile_top)
            requested = from_bounds(*intersection.bounds, transform=tile_transform)
            row0 = max(0, math.floor(requested.row_off))
            col0 = max(0, math.floor(requested.col_off))
            row1 = min(tile_height, math.ceil(requested.row_off + requested.height))
            col1 = min(tile_width, math.ceil(requested.col_off + requested.width))
            if row1 <= row0 or col1 <= col0:
                continue
            window = Window(col0, row0, col1 - col0, row1 - row0)
            shape_out = (int(window.height), int(window.width))
            window_transform = rasterio.windows.transform(window, tile_transform)

        red = read_at_100m(
            signed["assets"]["B04"]["href"],
            tile_transform,
            tile_width,
            tile_height,
            window,
            Resampling.average,
        ).astype(np.float32) * 0.0001
        nir = read_at_100m(
            signed["assets"]["B08"]["href"],
            tile_transform,
            tile_width,
            tile_height,
            window,
            Resampling.average,
        ).astype(np.float32) * 0.0001
        blue = read_at_100m(
            signed["assets"]["B02"]["href"],
            tile_transform,
            tile_width,
            tile_height,
            window,
            Resampling.average,
        ).astype(np.float32) * 0.0001
        scl = read_at_100m(
            signed["assets"]["SCL"]["href"],
            tile_transform,
            tile_width,
            tile_height,
            window,
            Resampling.mode,
        )

        inside = geometry_mask(
            [mapping(intersection)],
            out_shape=shape_out,
            transform=window_transform,
            invert=True,
        )
        valid = (
            inside
            & np.isin(scl, [4, 5])
            & (red > 0)
            & (nir > 0)
            & (blue > 0)
        )
        with np.errstate(divide="ignore", invalid="ignore"):
            ndvi = (nir - red) / (nir + red)
            evi = 2.5 * (nir - red) / (nir + 6 * red - 7.5 * blue + 1)
        valid &= (
            np.isfinite(ndvi)
            & np.isfinite(evi)
            & (ndvi >= -1)
            & (ndvi <= 1)
            & (evi >= -1)
            & (evi <= 2)
        )

        global_row = round((top - tile_top) / PIXEL_M) + row0
        global_col = round((tile_left - left) / PIXEL_M) + col0
        row_end = global_row + shape_out[0]
        col_end = global_col + shape_out[1]
        destination_ndvi = ndvi_mosaic[global_row:row_end, global_col:col_end]
        destination_evi = evi_mosaic[global_row:row_end, global_col:col_end]
        fill = valid & np.isnan(destination_ndvi)
        destination_ndvi[fill] = ndvi[fill]
        destination_evi[fill] = evi[fill]

    zone_pixels = ZONE_M // PIXEL_M
    grid_height, grid_width = height // zone_pixels, width // zone_pixels
    roi_mask = geometry_mask(
        [mapping(reserve_utm)],
        out_shape=(height, width),
        transform=transform,
        invert=True,
    )
    expected = roi_mask.reshape(
        grid_height, zone_pixels, grid_width, zone_pixels
    ).sum(axis=(1, 3))
    valid_mask = roi_mask & np.isfinite(ndvi_mosaic)
    valid_count = valid_mask.reshape(
        grid_height, zone_pixels, grid_width, zone_pixels
    ).sum(axis=(1, 3))
    ndvi_sum = np.where(valid_mask, ndvi_mosaic, 0).reshape(
        grid_height, zone_pixels, grid_width, zone_pixels
    ).sum(axis=(1, 3))
    evi_sum = np.where(valid_mask, evi_mosaic, 0).reshape(
        grid_height, zone_pixels, grid_width, zone_pixels
    ).sum(axis=(1, 3))
    with np.errstate(divide="ignore", invalid="ignore"):
        ndvi_mean = ndvi_sum / valid_count
        evi_mean = evi_sum / valid_count
        coverage = 100 * valid_count / expected

    include = (expected > 0) & (coverage >= 25) & (valid_count > 0)
    values = ndvi_mean[include]
    if values.size == 0:
        raise RuntimeError("No 2 km RFO cells met the 25% valid-observation threshold.")
    q25, q50, q75 = np.quantile(values, [0.25, 0.5, 0.75])
    breaks = [float(q25), float(q50), float(q75)]
    labels = [
        "Lower relative NDVI (Q1)",
        "Moderate relative NDVI (Q2)",
        "Higher relative NDVI (Q3)",
        "Highest relative NDVI (Q4)",
    ]

    features = []
    for row, col in zip(*np.where(include)):
        cell_left = left + col * ZONE_M
        cell_top = top - row * ZONE_M
        cell = box(cell_left, cell_top - ZONE_M, cell_left + ZONE_M, cell_top)
        clipped = cell.intersection(reserve_utm)
        if clipped.is_empty:
            continue
        clipped = clipped.simplify(25, preserve_topology=True).intersection(reserve_utm)
        value = float(ndvi_mean[row, col])
        zone = sum(value > threshold for threshold in breaks)
        geometry = transform_geometry(
            Transformer.from_crs(32635, 4326, always_xy=True).transform,
            clipped,
        )
        features.append(
            {
                "type": "Feature",
                "geometry": mapping(geometry),
                "properties": {
                    "zone_id": f"RFO-{row:03d}-{col:03d}",
                    "month": MONTH,
                    "ndvi_mean": round(value, 6),
                    "evi_mean": round(float(evi_mean[row, col]), 6),
                    "valid_coverage_pct": round(float(coverage[row, col]), 2),
                    "valid_100m_pixels": int(valid_count[row, col]),
                    "reserve_100m_pixels": int(expected[row, col]),
                    "ndvi_quartile": zone + 1,
                    "zone_label": labels[zone],
                    "emissions_status": "NOT_QUANTIFIABLE",
                    "gross_emissions_co2e_all_gases__Mg": None,
                    "gross_emissions_co2e_non_co2__Mg": None,
                    "gross_emissions_co2e_co2_only__Mg": None,
                    "interpretation": "Relative October NDVI screening class, not forest degradation, biomass, or carbon flux.",
                },
            }
        )

    document = {
        "type": "FeatureCollection",
        "name": "Okapi Wildlife Reserve October 2026 NDVI relative zones",
        "metadata": {
            "site_id": "124389",
            "boundary_file": BOUNDARY.name,
            "reporting_month": MONTH,
            "source": "Microsoft Planetary Computer Sentinel-2 L2A",
            "source_url": "https://planetarycomputer.microsoft.com/dataset/sentinel-2-l2a",
            "selected_scenes": len(scenes),
            "mgrs_tiles": sorted(
                item["properties"].get("s2:mgrs_tile", "") for item in scenes
            ),
            "pixel_resolution_m": PIXEL_M,
            "zone_resolution_m": ZONE_M,
            "cloud_mask": "Sentinel-2 SCL classes 4 and 5; other classes excluded.",
            "formulas": {
                "NDVI": "(B08 - B04) / (B08 + B04)",
                "EVI": "2.5 * (B08 - B04) / (B08 + 6*B04 - 7.5*B02 + 1)",
            },
            "reflectance_scale_factor": 0.0001,
            "overlap_method": "Selected one least-cloudy scene per MGRS tile; tile overlaps filled in ascending scene-cloud percentage.",
            "grid_cell_method": "2 km square grid in EPSG:32635; geometries clipped to RFO boundary; means use valid clear-land 100 m pixels.",
            "minimum_valid_coverage_pct": 25,
            "classification": {
                "method": "Quartiles across retained 2 km cells in this October 2026 dataset; relative classes, not ecological thresholds.",
                "q25_ndvi": round(float(q25), 6),
                "q50_ndvi": round(float(q50), 6),
                "q75_ndvi": round(float(q75), 6),
                "labels": labels,
            },
            "emissions": "Three gross emissions attributes are null (unknown, not zero); satellite vegetation indices do not measure greenhouse-gas flux.",
            "limitations": [
                "October cloud-free coverage is incomplete and varies among cells.",
                "NDVI/EVI are spectral vegetation-condition proxies and do not estimate biomass stock, growth, deforestation, emissions, or sequestration.",
                "Quartile zones are relative to the retained cells in this month only; do not compare as fixed ecological classes across months.",
                "This is not a validated disturbance, carbon-stock, or emissions map.",
            ],
        },
        "features": features,
    }
    OUTPUT.write_text(json.dumps(document, separators=(",", ":"), ensure_ascii=False) + "\n")
    print(
        json.dumps(
            {
                "output": str(OUTPUT),
                "features": len(features),
                "scenes": len(scenes),
                "quartile_breaks": breaks,
                "mean_valid_coverage_pct": round(
                    float(np.mean(coverage[include])), 2
                ),
            }
        )
    )


if __name__ == "__main__":
    main()
