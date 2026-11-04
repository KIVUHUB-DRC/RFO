#!/usr/bin/env python3
"""Summarize NASA Terra MODIS 8-day photosynthesis products over the RFO."""

import csv
import json
from collections import defaultdict
from datetime import date, datetime, timedelta
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
BOUNDARY = ROOT / "data" / "raw" / "RFO Limit.json"
OUTPUT = ROOT / "data" / "processed" / "OWR_MODIS_Carbon_2026.csv"
STAC = "https://planetarycomputer.microsoft.com/api/stac/v1"
DATA_CUTOFF = "2026-11-04T23:59:59Z"
FIRST_MONTH = date(2026, 1, 1)
LAST_MONTH = date(2026, 10, 1)
SCALE_FACTOR = 0.0001
MODLAND_QC_GOOD = 0


def fetch_items(reserve):
    session = requests.Session()
    body = {
        "collections": ["modis-17A2H-061"],
        "intersects": mapping(reserve.simplify(0.002, preserve_topology=True)),
        "datetime": f"{FIRST_MONTH.isoformat()}T00:00:00Z/{DATA_CUTOFF}",
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

    terra = {}
    for item in items:
        item_id = item.get("id", "")
        if not item_id.startswith("MOD17A2H."):
            continue
        props = item.get("properties", {})
        tile = item_id.split(".")[2]
        key = (props.get("start_datetime"), tile)
        if key not in terra or item_id > terra[key]["id"]:
            terra[key] = item
    return sorted(terra.values(), key=lambda item: item["id"])


def read_clipped_asset(url, reserve_projected):
    with rasterio.open(planetary_computer.sign_url(url)) as dataset:
        clipped = reserve_projected.intersection(box(*dataset.bounds))
        if clipped.is_empty:
            return None
        values, transform = raster_mask(
            dataset, [mapping(clipped)], crop=True, filled=False
        )
        return values[0], transform, dataset.transform.a**2


def get_period(item):
    props = item["properties"]
    start = datetime.fromisoformat(props["start_datetime"].replace("Z", "+00:00"))
    end = datetime.fromisoformat(props["end_datetime"].replace("Z", "+00:00"))
    return start.date(), end.date() + timedelta(days=1)


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


def count_union_days(intervals, start, end):
    clipped = sorted(
        (max(a, start), min(b, end))
        for a, b in intervals
        if max(a, start) < min(b, end)
    )
    total = 0
    current_start = current_end = None
    for a, b in clipped:
        if current_end is None or a > current_end:
            if current_end is not None:
                total += (current_end - current_start).days
            current_start, current_end = a, b
        elif b > current_end:
            current_end = b
    if current_end is not None:
        total += (current_end - current_start).days
    return total


def main():
    boundary = json.loads(BOUNDARY.read_text())
    reserve = shape(boundary["features"][0]["geometry"])
    monthly = defaultdict(
        lambda: {
            "gpp_valid_mg_c": 0.0,
            "psn_valid_mg_c": 0.0,
            "gpp_expanded_mg_c": 0.0,
            "psn_expanded_mg_c": 0.0,
            "gpp_valid_area_days": 0.0,
            "psn_valid_area_days": 0.0,
            "intervals": [],
            "granules": set(),
        }
    )
    reserve_pixels_by_tile = {}
    composites = {}
    pixel_area_m2 = None
    to_modis = None
    items = fetch_items(reserve)
    if not items:
        raise RuntimeError("No Terra MODIS MOD17A2H items found for the RFO.")

    for item in items:
        tile = item["id"].split(".")[2]
        if tile in reserve_pixels_by_tile:
            continue
        url = planetary_computer.sign_url(item["assets"]["Gpp_500m"]["href"])
        with rasterio.open(url) as ds:
            if to_modis is None:
                to_modis = Transformer.from_crs(
                    "EPSG:4326", ds.crs, always_xy=True
                ).transform
            reserve_projected = transform_geometry(to_modis, reserve)
            tile_geom = reserve_projected.intersection(box(*ds.bounds))
            if tile_geom.is_empty:
                continue
            gpp_ma, transform = raster_mask(
                ds, [mapping(tile_geom)], crop=True, filled=False
            )
            pixel_area_m2 = ds.transform.a**2
        inside = geometry_mask(
            [mapping(tile_geom)],
            out_shape=gpp_ma[0].shape,
            transform=transform,
            invert=True,
        )
        reserve_pixels_by_tile[tile] = int(inside.sum())
    total_reserve_pixels = sum(reserve_pixels_by_tile.values())
    if total_reserve_pixels <= 0:
        raise RuntimeError("The MODIS raster grid does not cover the RFO.")

    for item in items:
        assets = item.get("assets", {})
        required = ("Gpp_500m", "PsnNet_500m", "Psn_QC_500m")
        if any(name not in assets for name in required):
            raise RuntimeError(f"Missing MODIS measurement or QA asset: {item['id']}")

        with rasterio.open(planetary_computer.sign_url(assets["Gpp_500m"]["href"])) as ds:
            if to_modis is None:
                to_modis = Transformer.from_crs(
                    "EPSG:4326", ds.crs, always_xy=True
                ).transform
            reserve_projected = transform_geometry(to_modis, reserve)
            tile_geom = reserve_projected.intersection(box(*ds.bounds))
            if tile_geom.is_empty:
                continue
            gpp_ma, transform = raster_mask(
                ds, [mapping(tile_geom)], crop=True, filled=False
            )
            gpp = np.asarray(gpp_ma[0].data)
            gpp_masked = np.ma.getmaskarray(gpp_ma[0])
            pixel_area_m2 = ds.transform.a**2

        inside = geometry_mask(
            [mapping(tile_geom)],
            out_shape=gpp.shape,
            transform=transform,
            invert=True,
        )
        tile = item["id"].split(".")[2]
        reserve_pixels = int(inside.sum())
        if reserve_pixels_by_tile[tile] != reserve_pixels:
            raise RuntimeError(f"RFO pixel mask changed for MODIS tile {tile}.")

        psn_read = read_clipped_asset(assets["PsnNet_500m"]["href"], reserve_projected)
        qc_read = read_clipped_asset(assets["Psn_QC_500m"]["href"], reserve_projected)
        if psn_read is None or qc_read is None:
            raise RuntimeError(f"Missing clipped MODIS data for {item['id']}.")
        psn_ma, psn_transform, psn_pixel_area = psn_read
        qc_ma, qc_transform, qc_pixel_area = qc_read
        if (
            transform != psn_transform
            or transform != qc_transform
            or pixel_area_m2 != psn_pixel_area
            or pixel_area_m2 != qc_pixel_area
            or gpp.shape != psn_ma.shape
            or gpp.shape != qc_ma.shape
        ):
            raise RuntimeError(f"MODIS bands are not aligned for {item['id']}.")

        psn = np.asarray(psn_ma.data)
        qc = np.asarray(qc_ma.data)
        qc_valid = (
            ~np.ma.getmaskarray(qc_ma)
            & ((qc.astype(np.uint16) & 1) == MODLAND_QC_GOOD)
        )
        gpp_valid = (
            inside
            & ~gpp_masked
            & qc_valid
            & (gpp >= 0)
            & (gpp <= 30000)
        )
        psn_valid = (
            inside
            & ~np.ma.getmaskarray(psn_ma)
            & qc_valid
            & (psn >= -30000)
            & (psn <= 30000)
        )

        period_start, period_end = get_period(item)
        period_days = (period_end - period_start).days
        if period_days <= 0:
            raise RuntimeError(f"Invalid MODIS composite period: {item['id']}")
        key = (period_start, period_end)
        composite = composites.setdefault(
            key,
            {
                "gpp_mg_c": 0.0,
                "psn_mg_c": 0.0,
                "gpp_valid_pixels": 0,
                "psn_valid_pixels": 0,
                "granules": set(),
            },
        )
        composite["gpp_mg_c"] += (
            float(gpp[gpp_valid].sum()) * SCALE_FACTOR * pixel_area_m2 / 1000
        )
        composite["psn_mg_c"] += (
            float(psn[psn_valid].sum()) * SCALE_FACTOR * pixel_area_m2 / 1000
        )
        composite["gpp_valid_pixels"] += int(gpp_valid.sum())
        composite["psn_valid_pixels"] += int(psn_valid.sum())
        composite["granules"].add(item["id"])

    for (period_start, period_end), composite in sorted(composites.items()):
        period_days = (period_end - period_start).days
        gpp_coverage = composite["gpp_valid_pixels"] / total_reserve_pixels
        psn_coverage = composite["psn_valid_pixels"] / total_reserve_pixels
        for month_start, month_end in month_ranges():
            overlap_start = max(period_start, month_start)
            overlap_end = min(period_end, month_end)
            overlap_days = (overlap_end - overlap_start).days
            if overlap_days <= 0:
                continue
            row = monthly[month_start.isoformat()[:7]]
            fraction = overlap_days / period_days
            row["gpp_valid_mg_c"] += composite["gpp_mg_c"] * fraction
            row["psn_valid_mg_c"] += composite["psn_mg_c"] * fraction
            if gpp_coverage:
                row["gpp_expanded_mg_c"] += (
                    composite["gpp_mg_c"] * fraction / gpp_coverage
                )
            if psn_coverage:
                row["psn_expanded_mg_c"] += (
                    composite["psn_mg_c"] * fraction / psn_coverage
                )
            row["gpp_valid_area_days"] += gpp_coverage * overlap_days
            row["psn_valid_area_days"] += psn_coverage * overlap_days
            row["intervals"].append((overlap_start, overlap_end))
            row["granules"].update(composite["granules"])

    output_fields = [
        "month",
        "reporting_period_start",
        "reporting_period_end",
        "observed_data_start",
        "observed_data_end",
        "observed_days",
        "days_with_data_pct",
        "modis_gpp_valid_pixel_sum_Mg_C",
        "modis_gpp_area_expanded_Mg_C_observed_days",
        "modis_psn_valid_pixel_sum_Mg_C",
        "modis_psn_area_expanded_Mg_C_observed_days",
        "gpp_valid_area_coverage_pct_observed_days",
        "psn_valid_area_coverage_pct_observed_days",
        "gpp_spatiotemporal_coverage_pct_full_month",
        "psn_spatiotemporal_coverage_pct_full_month",
        "granule_count",
        "product",
        "source_url",
        "method",
    ]
    with OUTPUT.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=output_fields)
        writer.writeheader()
        for month_start, month_end in month_ranges():
            month = month_start.isoformat()[:7]
            row = monthly[month]
            days_in_month = (month_end - month_start).days
            observed_days = count_union_days(row["intervals"], month_start, month_end)
            intervals = sorted(row["intervals"])
            observed_start = min((a for a, _ in intervals), default=None)
            observed_end = max((b for _, b in intervals), default=None)
            area_day_denominator = days_in_month
            gpp_area_coverage = (
                100 * row["gpp_valid_area_days"] / observed_days
                if observed_days
                else None
            )
            psn_area_coverage = (
                100 * row["psn_valid_area_days"] / observed_days
                if observed_days
                else None
            )
            writer.writerow(
                {
                    "month": month,
                    "reporting_period_start": month_start.isoformat(),
                    "reporting_period_end": (month_end - timedelta(days=1)).isoformat(),
                    "observed_data_start": observed_start.isoformat() if observed_start else "",
                    "observed_data_end": (observed_end - timedelta(days=1)).isoformat()
                    if observed_end
                    else "",
                    "observed_days": observed_days,
                    "days_with_data_pct": round(100 * observed_days / days_in_month, 3),
                    "modis_gpp_valid_pixel_sum_Mg_C": round(row["gpp_valid_mg_c"], 3)
                    if row["granules"]
                    else "",
                    "modis_gpp_area_expanded_Mg_C_observed_days": round(
                        row["gpp_expanded_mg_c"], 3
                    )
                    if row["granules"]
                    else "",
                    "modis_psn_valid_pixel_sum_Mg_C": round(row["psn_valid_mg_c"], 3)
                    if row["granules"]
                    else "",
                    "modis_psn_area_expanded_Mg_C_observed_days": round(
                        row["psn_expanded_mg_c"], 3
                    )
                    if row["granules"]
                    else "",
                    "gpp_valid_area_coverage_pct_observed_days": round(
                        gpp_area_coverage, 3
                    )
                    if gpp_area_coverage is not None
                    else "",
                    "psn_valid_area_coverage_pct_observed_days": round(
                        psn_area_coverage, 3
                    )
                    if psn_area_coverage is not None
                    else "",
                    "gpp_spatiotemporal_coverage_pct_full_month": round(
                        100 * row["gpp_valid_area_days"] / area_day_denominator, 3
                    )
                    if area_day_denominator
                    else "",
                    "psn_spatiotemporal_coverage_pct_full_month": round(
                        100 * row["psn_valid_area_days"] / area_day_denominator, 3
                    )
                    if area_day_denominator
                    else "",
                    "granule_count": len(row["granules"]),
                    "product": "NASA Terra MOD17A2H.061",
                    "source_url": "https://planetarycomputer.microsoft.com/api/stac/v1/collections/modis-17A2H-061",
                    "method": (
                        "500 m cumulative 8-day MODIS GPP and net photosynthesis; "
                        "scale factor 0.0001 kg C m-2; MODLAND QC bit 0 = good; "
                        "valid-range values only; pixel-center RFO mask in equal-area "
                        "MODIS sinusoidal grid. Composite totals are apportioned by "
                        "overlap days at a uniform daily rate. Valid-pixel sums are "
                        "not spatially expanded; area-expanded values divide each "
                        "composite sum by its valid-area fraction and remain model "
                        "estimates, not net ecosystem sequestration or emissions."
                    ),
                }
            )

    print(f"Wrote {OUTPUT} ({len(list(month_ranges()))} months).")


if __name__ == "__main__":
    main()
