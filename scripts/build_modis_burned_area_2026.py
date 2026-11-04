#!/usr/bin/env python3
"""Summarize NASA MODIS monthly burned-area data over the RFO."""

import csv
import json
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

import numpy as np
import planetary_computer
import rasterio
import requests
from pyproj import Transformer
from rasterio.features import geometry_mask
from rasterio.mask import mask as raster_mask
from shapely.geometry import box, mapping, shape
from shapely.ops import transform as transform_geometry


ROOT = Path(__file__).resolve().parents[1]
BOUNDARY = ROOT / "RFO Limit.json"
OUTPUT = ROOT / "OWR_MODIS_Burned_Area_2026.csv"
RASTER_DIR = ROOT / "data" / "modis_burned_area_2026"
STAC = "https://planetarycomputer.microsoft.com/api/stac/v1"
COLLECTION = "modis-64A1-061"
FIRST_MONTH = date(2026, 1, 1)
LAST_MONTH = date(2026, 10, 1)
QA_LAND_AND_VALID = 0b11


def month_ranges():
    current = FIRST_MONTH
    while current <= LAST_MONTH:
        next_month = (
            date(current.year + 1, 1, 1)
            if current.month == 12
            else date(current.year, current.month + 1, 1)
        )
        yield current, next_month
        current = next_month


def fetch_items(reserve):
    session = requests.Session()
    body = {
        "collections": [COLLECTION],
        "intersects": mapping(reserve.simplify(0.002, preserve_topology=True)),
        "datetime": "2026-01-01T00:00:00Z/2026-10-31T23:59:59Z",
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

    latest_by_month_tile = {}
    for item in items:
        props = item.get("properties", {})
        start = props.get("start_datetime")
        if not start:
            raise RuntimeError(f"Missing MODIS period start: {item.get('id')}")
        month = datetime.fromisoformat(start.replace("Z", "+00:00")).date().replace(day=1)
        tile = item["id"].split(".")[2]
        key = (month, tile)
        if key not in latest_by_month_tile or item["id"] > latest_by_month_tile[key]["id"]:
            latest_by_month_tile[key] = item
    return latest_by_month_tile


def clip_asset(url, reserve):
    with rasterio.open(planetary_computer.sign_url(url)) as dataset:
        to_raster = Transformer.from_crs(
            "EPSG:4326", dataset.crs, always_xy=True
        ).transform
        reserve_projected = transform_geometry(to_raster, reserve)
        clipped_geometry = reserve_projected.intersection(box(*dataset.bounds))
        if clipped_geometry.is_empty:
            return None
        values, transform = raster_mask(
            dataset,
            [mapping(clipped_geometry)],
            crop=True,
            filled=False,
        )
        pixel_area_m2 = abs(dataset.transform.a * dataset.transform.e)
        profile = dataset.profile.copy()
        profile.update(crs=dataset.crs)

    inside = geometry_mask(
        [mapping(clipped_geometry)],
        out_shape=values[0].shape,
        transform=transform,
        invert=True,
    )
    return values[0], inside, transform, pixel_area_m2, profile


def write_clip(item, tile, burn_date, qa, inside, transform, profile, month):
    RASTER_DIR.mkdir(parents=True, exist_ok=True)
    output = RASTER_DIR / f"MCD64A1_{month}_{tile}_RFO.tif"
    burn = np.where(inside, burn_date, -9999).astype(np.int16)
    qa_values = np.where(inside, qa.astype(np.int16), -9999)
    out_profile = profile.copy()
    out_profile.update(
        driver="GTiff",
        transform=transform,
        width=burn.shape[1],
        height=burn.shape[0],
        count=2,
        dtype="int16",
        nodata=-9999,
        compress="DEFLATE",
    )
    with rasterio.open(output, "w", **out_profile) as dataset:
        dataset.write(burn, 1)
        dataset.write(qa_values, 2)
        dataset.set_band_description(1, "Burn_Date (ordinal day; 0=unburned)")
        dataset.set_band_description(2, "QA (bits 0-1: land and valid observation)")
        dataset.update_tags(
            source_item=item["id"],
            source_collection=COLLECTION,
            source_url=item["assets"]["Burn_Date"]["href"],
            boundary_file=BOUNDARY.name,
            method="RFO-clipped MODIS Burn_Date and QA; pixels outside boundary set to -9999",
        )
    return output.relative_to(ROOT).as_posix()


def main():
    boundary = json.loads(BOUNDARY.read_text(encoding="utf-8"))
    reserve = shape(boundary["features"][0]["geometry"])
    items = fetch_items(reserve)
    monthly = defaultdict(
        lambda: {
            "burned_pixels": 0,
            "valid_pixels": 0,
            "reserve_pixels": 0,
            "area_ha": 0.0,
            "tiles": [],
            "granules": [],
            "rasters": [],
        }
    )

    for (month_start, tile), item in sorted(items.items()):
        assets = item.get("assets", {})
        if "Burn_Date" not in assets or "QA" not in assets:
            raise RuntimeError(f"Missing Burn_Date or QA asset: {item['id']}")

        burn_read = clip_asset(assets["Burn_Date"]["href"], reserve)
        qa_read = clip_asset(assets["QA"]["href"], reserve)
        if burn_read is None or qa_read is None:
            raise RuntimeError(f"MODIS item does not cover the RFO: {item['id']}")
        burn_ma, inside, transform, pixel_area_m2, profile = burn_read
        qa_ma, qa_inside, qa_transform, qa_area_m2, _ = qa_read
        if (
            not np.array_equal(inside, qa_inside)
            or transform != qa_transform
            or pixel_area_m2 != qa_area_m2
            or burn_ma.shape != qa_ma.shape
        ):
            raise RuntimeError(f"MODIS Burn_Date and QA assets are misaligned: {item['id']}")

        burn_date = np.asarray(burn_ma.data)
        qa = np.asarray(qa_ma.data).astype(np.uint8)
        valid = (
            inside
            & ~np.ma.getmaskarray(burn_ma)
            & ~np.ma.getmaskarray(qa_ma)
            & ((qa & QA_LAND_AND_VALID) == QA_LAND_AND_VALID)
            & (burn_date >= 0)
            & (burn_date <= 366)
        )
        burned = valid & (burn_date >= 1)
        month = month_start.isoformat()[:7]
        result = monthly[month]
        result["burned_pixels"] += int(burned.sum())
        result["valid_pixels"] += int(valid.sum())
        result["reserve_pixels"] += int(inside.sum())
        result["area_ha"] += int(burned.sum()) * pixel_area_m2 / 10_000
        result["tiles"].append(tile)
        result["granules"].append(item["id"])
        result["rasters"].append(
            write_clip(
                item,
                tile,
                burn_date,
                qa,
                inside,
                transform,
                profile,
                month,
            )
        )

    fields = [
        "month",
        "reporting_period_start",
        "reporting_period_end",
        "product_status",
        "modis_burned_area_ha",
        "burned_pixel_count",
        "qa_valid_land_pixel_count",
        "rfo_pixel_count",
        "valid_area_coverage_pct",
        "tiles",
        "granule_ids",
        "rfo_clipped_rasters",
        "product",
        "source_url",
        "method",
    ]
    with OUTPUT.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for month_start, month_end in month_ranges():
            month = month_start.isoformat()[:7]
            result = monthly.get(month)
            if result is None:
                status = "NOT_PUBLISHED_IN_CATALOG_AS_OF_2026-11-04"
                burned_area = burned_pixels = valid_pixels = reserve_pixels = coverage = ""
                tiles = granules = rasters = ""
            else:
                status = "PROCESSED_MODIS_500M_QA_SCREENED"
                burned_area = round(result["area_ha"], 3)
                burned_pixels = result["burned_pixels"]
                valid_pixels = result["valid_pixels"]
                reserve_pixels = result["reserve_pixels"]
                coverage = round(
                    100 * valid_pixels / reserve_pixels, 3
                ) if reserve_pixels else ""
                tiles = ";".join(sorted(set(result["tiles"])))
                granules = ";".join(sorted(result["granules"]))
                rasters = ";".join(sorted(result["rasters"]))
            writer.writerow(
                {
                    "month": month,
                    "reporting_period_start": month_start.isoformat(),
                    "reporting_period_end": (month_end - date.resolution).isoformat(),
                    "product_status": status,
                    "modis_burned_area_ha": burned_area,
                    "burned_pixel_count": burned_pixels,
                    "qa_valid_land_pixel_count": valid_pixels,
                    "rfo_pixel_count": reserve_pixels,
                    "valid_area_coverage_pct": coverage,
                    "tiles": tiles,
                    "granule_ids": granules,
                    "rfo_clipped_rasters": rasters,
                    "product": "NASA/USGS MCD64A1.061",
                    "source_url": f"https://planetarycomputer.microsoft.com/api/stac/v1/collections/{COLLECTION}",
                    "method": (
                        "Monthly MODIS 500 m Burn_Date COG clipped to RFO pixel centers. "
                        "Burned pixels have Burn_Date 1-366 and QA land and valid-data "
                        "bits both set; area is burned-pixel count times equal-area "
                        "sinusoidal grid-cell area. No extrapolation. This is a coarse "
                        "satellite burned-area estimate, not burned biomass or emissions."
                    ),
                }
            )
    print(f"Wrote {OUTPUT} ({len(list(month_ranges()))} months).")


if __name__ == "__main__":
    main()
