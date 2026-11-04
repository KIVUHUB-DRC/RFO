# RFO 2026 data dictionary

## Reporting scope

- **Reserve:** Okapi Wildlife Reserve, WDPA site 124389.
- **Boundary:** `RFO Limit.json`; area used in the assessment is approximately 13,939.55 km².
- **Reporting period:** 1 January–31 October 2026.
- **Units:** gross emissions are Mg CO₂e. NDVI/EVI are dimensionless.
- **Null policy:** blank CSV values and SQL `NULL` are unknown/not quantified, never zero unless an explicit zero was measured.

## `OWR_Emissions_2026.csv`

| Column | Type / unit | Definition |
|---|---|---|
| `month` | `YYYY-MM` | Monthly reporting key. |
| `gross_emissions_co2e_all_gases__Mg` | Numeric or blank; Mg CO₂e | Gross emissions from all included gases, for the month and RFO. Blank because no validated monthly greenhouse-gas inventory was available. |
| `gross_emissions_co2e_non_co2__Mg` | Numeric or blank; Mg CO₂e | Non-CO₂ gases such as CH₄/N₂O on a documented CO₂e basis. Blank because local activity/gas fluxes and factors are unavailable. |
| `gross_emissions_co2e_co2_only__Mg` | Numeric or blank; Mg CO₂e | Gross CO₂ emissions only. Blank because verified disturbance/burn area and associated carbon-pool loss are unavailable. |
| `data_status` | Category | `NOT_QUANTIFIABLE` for every reporting month in the current dataset. |
| `reason` | Text | Explains why the emissions fields remain blank. |
| `sentinel2_clear_land_coverage_pct` | Percent | Share of the 100 m reserve grid with a valid clear-land Sentinel-2 observation in that month’s mosaic. |
| `sentinel2_ndvi_mean`, `sentinel2_evi_mean` | Dimensionless | Area-aggregated monthly vegetation-condition indices; not biomass or gas flux. |
| `landsat_scene_count`, `sentinel1_scene_count` | Count | Catalog items returned for the monthly RFO-intersection query; raster metrics were not processed. |
| `gedi_intersecting_granule_count`, `nisar_intersecting_granule_count` | Count | CMR granule metadata footprints intersecting RFO in the month; measurement files were not analyzed. |
| `boundary_site_id`, `boundary_file` | Text | Site identifier and boundary filename applied. |
| `reporting_period_start`, `reporting_period_end` | ISO date | Inclusive month start and end. |
| `source_metadata` | Filename | Companion machine-readable metadata JSON. |

## `RFO_Oct2026_NDVI_Zones.geojson`

Each feature is a reserve-clipped 2 km grid cell with at least 25% valid clear-land pixel coverage in October 2026. Projected processing is in EPSG:32635; delivered coordinates are WGS84 GeoJSON.

| Property | Definition |
|---|---|
| `zone_id` | Stable row/column identifier for the 2 km grid. |
| `month` | `2026-10`. |
| `ndvi_mean`, `evi_mean` | Mean of valid clear-land 100 m pixels within the clipped zone. |
| `valid_coverage_pct` | Valid clear-land pixel centers divided by reserve pixel centers in the cell. |
| `valid_100m_pixels`, `reserve_100m_pixels` | Counts used to calculate coverage. |
| `ndvi_quartile` | Relative October NDVI quartile, 1–4, among retained zones. |
| `zone_label` | Text label for the relative quartile; not a fixed ecological class. |
| `emissions_status` | `NOT_QUANTIFIABLE`. |
| `gross_emissions_co2e_all_gases__Mg`, `gross_emissions_co2e_non_co2__Mg`, `gross_emissions_co2e_co2_only__Mg` | JSON `null`; no zone-level emissions amount is available. |
| `interpretation` | Explicit warning that the zone class is not a disturbance or carbon-flux result. |

The top-level `metadata.classification` object records numeric quartile thresholds. The map uses dark green (Q1/lower relative NDVI), light green (Q2), amber (Q3), and deep green (Q4/highest relative NDVI). Cells below the coverage threshold are not drawn. These month-specific relative bins are for cartographic screening only.

## SQLite tables

`monthly_gross_emissions` stores the three emissions fields as SQL `NULL`, the status/reason, monthly sensor indicators, boundary reference, and metadata filename. `satellite_zone_cells` stores the clipped October cell attributes and GeoJSON geometry text. Other satellite tables are `satellite_monthly`, `satellite_scene_inventory`, and `satellite_mission_catalog`. `monthly_accounting` remains the original carbon-accounting export and is not overwritten by satellite indices.

## Interpretation and limitations

Optical reflectance, radar scenes, lidar footprints, or atmospheric concentration measurements do not directly equal gross emissions. An emissions estimate needs validated monthly activity data, affected carbon pools/stocks, gas-specific emission factors and CO₂e conversion rules, a clear accounting boundary, and uncertainty/quality controls. See [`method.html`](method.html), [`OWR_Emissions_Metadata_2026.json`](OWR_Emissions_Metadata_2026.json), and [`OWR_Carbon_2026.md`](OWR_Carbon_2026.md).
