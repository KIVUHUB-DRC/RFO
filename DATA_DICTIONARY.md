# RFO 2026 data dictionary

## Reporting scope

- **Reserve:** Okapi Wildlife Reserve, WDPA site 124389.
- **Boundary:** `RFO Limit.json`; area used in the assessment is approximately 13,939.55 km².
- **Reporting period:** 1 January–31 October 2026.
- **Units:** gross emissions are Mg CO₂e; MODIS photosynthesis values are Mg C. NDVI/EVI are dimensionless.
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
| `source_metadata` | Filename(s) | Semicolon-separated companion metadata/data files, including MODIS uptake details. |
| `candidate_fire_emissions_source` | Text | Open-data candidate reviewed for fire-only modeling; currently `CAMS GFAS v1.4.2`. |
| `candidate_fire_emissions_status` | Category | Retrieval status for the candidate model. `NOT_RETRIEVED_AUTHENTICATION_AND_TERMS_ACCEPTANCE_REQUIRED` means no model estimate was downloaded or calculated; it does not mean zero emissions. |
| `source_review_date_utc` | ISO date | Date the open-data candidate and access requirements were checked. |
| `modis_observed_days`, `modis_days_with_data_pct` | Days; percent | Calendar days and share with available NASA Terra MODIS composites. October coverage is through 15 October only. |
| `modis_gpp_area_expanded_Mg_C_observed_days`, `modis_psn_area_expanded_Mg_C_observed_days` | Mg C | Area-expanded GPP and PSN estimates for available dates. These are modelled photosynthetic uptake indicators, not emissions or net sequestration. |
| `modis_gpp_valid_area_coverage_pct_observed_days`, `modis_psn_valid_area_coverage_pct_observed_days` | Percent | Quality-screened reserve area represented on observed dates. |
| `modis_gpp_spatiotemporal_coverage_pct_full_month`, `modis_psn_spatiotemporal_coverage_pct_full_month` | Percent | Quality-screened area-days as a share of the full month. |

## `OWR_MODIS_Carbon_2026.csv`

NASA Terra MOD17A2H.061 500 m eight-day GPP and net-photosynthesis data summarized over the RFO. These are modelled photosynthetic carbon-uptake indicators, not carbon stocks, net ecosystem sequestration, emissions, or CO₂e removals.

| Column | Type / unit | Definition |
|---|---|---|
| `month` | `YYYY-MM` | Calendar reporting month. |
| `reporting_period_start`, `reporting_period_end` | ISO date | Full inclusive calendar month. |
| `observed_data_start`, `observed_data_end` | ISO date | First and last days of available RFO-intersecting Terra composites in the month. October data end on 15 October. |
| `observed_days`, `days_with_data_pct` | Days; percent | Calendar days overlapped by available composites, counted once. October has 15 of 31 days. |
| `modis_gpp_valid_pixel_sum_Mg_C` | Mg C | Eight-day GPP sum integrated over RFO pixel centers passing MODLAND quality and product valid-range filters; not expanded to pixels without valid data. |
| `modis_gpp_area_expanded_Mg_C_observed_days` | Mg C | Per-composite GPP sum divided by its valid-area fraction, then apportioned to the observed calendar days. This spatial extrapolation assumes valid pixels represent the rest of the reserve; it is not a validated gap-filling model. |
| `modis_psn_valid_pixel_sum_Mg_C` | Mg C | Unexpanded net-photosynthesis sum over valid pixels. PSN is GPP minus maintenance respiration. |
| `modis_psn_area_expanded_Mg_C_observed_days` | Mg C | PSN area-expanded over the full RFO for the observed days, with the same spatial extrapolation caveat. |
| `gpp_valid_area_coverage_pct_observed_days`, `psn_valid_area_coverage_pct_observed_days` | Percent | Mean quality-screened spatial coverage during dates with composites. |
| `gpp_spatiotemporal_coverage_pct_full_month`, `psn_spatiotemporal_coverage_pct_full_month` | Percent | Valid area-days divided by the full reserve area-days for the calendar month. October combines 15/31 date coverage with valid-area coverage. |
| `granule_count` | Count | Number of RFO-intersecting Terra composites contributing to that month; a composite crossing a month boundary can appear in both monthly counts. |
| `product`, `source_url`, `method` | Text | Product provenance and calculation/interpretation caveats. |

The eight-day data are assigned to calendar months in proportion to overlapping days, assuming a uniform daily rate within each composite. Values use the product scale factor 0.0001 kg C m⁻² and MODIS sinusoidal equal-area pixel area. No confidence interval is provided. Coverage ranges widely; September is especially incomplete, and October is partial.

## `OWR_Carbon_2026.csv`

The original monthly accounting fields for aboveground carbon stock, gross biomass sequestration, biomass emissions, and net carbon balance remain blank because these values were not measured or defensibly estimated. Additional `modis_*` columns carry the corresponding NASA MODIS GPP/PSN values, coverage dates, quality coverage, and status. These photosynthesis estimates must not be interpreted as any of the original accounting fields; `modis_source_id` identifies `NASA_MOD17A2H_061`.

### Open 2026 fire-emissions source assessment

CAMS GFAS v1.4.2 advertises hourly/daily modelled biomass-burning emissions from 2026 onward at 0.1° resolution, including CO₂, CH₄, and N₂O flux variables. It is an experimental candidate for fire-only emissions, not total gross reserve emissions. Data retrieval requires a Copernicus CDS/ADS account, personal API token, and manual acceptance of the dataset terms. No token was configured for the 4 November 2026 assessment, so no RFO-clipped values were calculated. See the `open_data_assessment` object in `OWR_Emissions_Metadata_2026.json` and the `emissions_source_audit` SQLite table.

Other sources checked: NASA FIRMS active-fire API retrieval requires a MAP_KEY and detections are not emission masses; ESA CCI FireCCI51 ends in 2020; Hansen/UMD Global Forest Change v1.13 covers annual loss through 2025; and the previously checked Global Forest Watch alerts API required a key. None yielded retrieved 2026 RFO gross-emission amounts.

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

`modis_carbon_monthly` stores the NASA MODIS GPP/PSN values, coverage, periods, and method. `monthly_accounting` and `monthly_gross_emissions` carry matching MODIS summary fields for convenient monthly joins; the original carbon-stock, sequestration, emissions, and net-balance fields remain `NULL`. `monthly_gross_emissions` also stores the three requested emissions fields as SQL `NULL`, the status/reason, monthly sensor indicators, boundary reference, metadata filename, and dated GFAS candidate-source status. `emissions_source_audit` records the CAMS GFAS product, variables, coverage, retrieval status, and fire-only scope. `satellite_zone_cells` stores the clipped October cell attributes and GeoJSON geometry text. Other satellite tables are `satellite_monthly`, `satellite_scene_inventory`, and `satellite_mission_catalog`.

## Interpretation and limitations

Optical reflectance, radar scenes, lidar footprints, or atmospheric concentration measurements do not directly equal gross emissions. An emissions estimate needs validated monthly activity data, affected carbon pools/stocks, gas-specific emission factors and CO₂e conversion rules, a clear accounting boundary, and uncertainty/quality controls. See [`method.html`](method.html), [`OWR_Emissions_Metadata_2026.json`](OWR_Emissions_Metadata_2026.json), and [`OWR_Carbon_2026.md`](OWR_Carbon_2026.md).
