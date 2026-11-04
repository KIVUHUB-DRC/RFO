# Okapi Wildlife Reserve carbon and satellite assessment

Public, preliminary, boundary-based screening of the Okapi Wildlife Reserve (RFO), Democratic Republic of the Congo. Reporting period: **1 January–31 October 2026**. The project uses the repository boundary `RFO Limit.json` (WDPA site 124389).

## Public project pages

- **[Landing page](https://kivuhub-drc.github.io/RFO/)** — overview, Leaflet reserve map, monthly satellite summary, and carbon-emissions status.
- **[Map-focused landing page](https://kivuhub-drc.github.io/RFO/landing.html)** — full-screen reserve boundary and October relative-NDVI zone map, with a dated emissions-source status.
- **[Carbon-emissions section](https://kivuhub-drc.github.io/RFO/#emissions)** — monthly all-gases, non-CO₂, and CO₂-only data status.
- **[Methods](https://kivuhub-drc.github.io/RFO/method.html)** — plain-language and scientific description of boundary handling, remote-sensing processing, emissions-data limits, and zone interpretation.
- **[Interactive map and downloads](https://kivuhub-drc.github.io/RFO/data.html)** — October 2026 NDVI relative-quartile map and repository data downloads.
- **[Data dictionary](DATA_DICTIONARY.md)** — CSV/GeoJSON column definitions, SQLite tables, units, map classes, and null semantics.
- **[Full assessment](OWR_Carbon_2026.md)** — detailed evidence synthesis, references, assumptions, and limitations.
- [Word report](OWR_Carbon_2026.docx) · [SQLite database](OWR_Carbon_2026.sqlite)

## Downloadable data

| File | Contents |
|---|---|
| [`RFO Limit.json`](RFO%20Limit.json) | Source reserve polygon and WDPA properties. |
| [`RFO_Oct2026_NDVI_Zones.geojson`](RFO_Oct2026_NDVI_Zones.geojson) | 2 km grid clipped to the RFO, with October NDVI/EVI, clear-pixel coverage, and relative NDVI quartile class. Emission fields are not inferred from NDVI. |
| [`OWR_Emissions_2026.csv`](OWR_Emissions_2026.csv) | Ten monthly records with the requested gross emissions fields, status, satellite coverage, and reporting dates. |
| [`OWR_Emissions_Metadata_2026.json`](OWR_Emissions_Metadata_2026.json) | Data dictionary, units, spatial/time scope, source inventory, limitations, and requirements for future emission estimates. |
| [`OWR_Satellite_2026.csv`](OWR_Satellite_2026.csv) | Monthly Sentinel-2 NDVI/EVI and clear-pixel coverage; Landsat/Sentinel-1 scene counts and GEDI/NISAR footprint counts. |
| [`OWR_MODIS_Carbon_2026.csv`](OWR_MODIS_Carbon_2026.csv) | NASA Terra MODIS 500 m eight-day GPP and net-photosynthesis estimates, valid-area coverage, and observed dates. October is available only through 15 October. |
| [`OWR_Satellite_Scenes_2026.csv`](OWR_Satellite_Scenes_2026.csv) | Satellite scene and selected NASA CMR granule-footprint inventory. Catalog records do not necessarily represent processed measurements. |
| [`OWR_Mission_Catalog_2026.csv`](OWR_Mission_Catalog_2026.csv) | Mission-specific catalog/footprint counts, processing state, sources, and limitations. |
| [`OWR_Carbon_2026.csv`](OWR_Carbon_2026.csv) | Monthly accounting export with separate MODIS uptake indicators; unmeasured stock, sequestration, emissions, and balance fields remain blank. |

### Requested gross-emissions fields

All three fields are in **Mg CO₂e per reporting month and RFO boundary**:

- `gross_emissions_co2e_all_gases__Mg`
- `gross_emissions_co2e_non_co2__Mg`
- `gross_emissions_co2e_co2_only__Mg`

They are blank in every month with `data_status=NOT_QUANTIFIABLE`. Blank/null means **unknown or not measured**, not zero. A 4 November 2026 open-data review identified CAMS GFAS v1.4.2 as a candidate 2026 daily/hourly, 0.1° fire-emissions model with CO₂, CH₄, and N₂O variables. Its API requires a CDS/ADS account, personal access token, and manual acceptance of dataset terms; no token was configured, so no model values were retrieved. Moreover, GFAS is fire-only and cannot by itself quantify all-source reserve gross emissions. The monthly CSV and SQLite record this assessment and retrieval status without substituting fire emissions for the requested totals. See the [metadata](OWR_Emissions_Metadata_2026.json), [Methods page](https://kivuhub-drc.github.io/RFO/method.html), [CAMS GFAS dataset](https://ads.atmosphere.copernicus.eu/datasets/cams-global-fire-emissions-gfas), and [API access instructions](https://cds.climate.copernicus.eu/how-to-api).

## October spatial zones and map legend

The downloadable zone GeoJSON summarizes clear Sentinel-2 L2A observations from October 2026 in 2 km cells clipped to the reserve. It selects one least-cloudy scene per each of six MGRS tiles, aligns red/NIR/blue/SCL bands at 100 m, masks to SCL classes 4 and 5, and computes monthly pixel means. Cells with less than 25% valid clear-land coverage are omitted. Retained cell means are divided into four **data-relative October NDVI quartiles**; the actual breaks are in the GeoJSON `metadata.classification` object. These colors are not fixed forest classes, degradation alerts, biomass estimates, or emissions.

The corresponding reproducible script is [`scripts/build_rfo_zones.py`](scripts/build_rfo_zones.py). It requires Python packages `numpy`, `planetary-computer`, `pyproj`, `rasterio`, `requests`, and `shapely`, plus network access to the Microsoft Planetary Computer STAC service and signed public assets. Run from the repository root:

```bash
python scripts/build_rfo_zones.py
```

It reads `RFO Limit.json` and writes `RFO_Oct2026_NDVI_Zones.geojson`. Cloud availability, public catalogs, and signed URLs can change.

## Database additions

The SQLite database includes separate `satellite_monthly`, `satellite_scene_inventory`, `satellite_mission_catalog`, `satellite_zone_cells`, `modis_carbon_monthly`, `monthly_gross_emissions`, and `emissions_source_audit` tables. `satellite_zone_cells` contains clipped October grid geometries with NDVI/EVI and quartile attributes. `modis_carbon_monthly` records NASA MODIS modelled GPP and net photosynthesis with QA/date coverage; these are not net sequestration or emissions. The gross-emissions table retains the requested fields as SQL `NULL` rather than replacing unknowns with zero and records the dated CAMS GFAS candidate-source status. `emissions_source_audit`, `metadata`, and `sources` document provenance and limitations.

## Evidence and limits

- Sentinel-2 is the only imagery used to calculate spatial vegetation indices in this repository. Landsat and Sentinel-1 were catalogued but not raster-processed.
- NASA Terra MOD17A2H.061 500 m GPP and net-photosynthesis composites were raster-processed. These are modelled photosynthetic uptake indicators, not carbon stocks, net ecosystem sequestration, or emissions; October data end on 15 October and spatial QA coverage is variable. [`scripts/build_modis_carbon_2026.py`](scripts/build_modis_carbon_2026.py) reproduces the calculation:

  ```bash
  python scripts/build_modis_carbon_2026.py
  ```

- GEDI and NISAR records are footprint metadata, not analyzed height/biomass/backscatter observations.
- OCO-2/3 are atmospheric concentration missions; no matching local intersecting footprint polygons were identified in the checked catalog responses. GOSAT/TanSat results and ESA Biomass mission availability do not constitute processed RFO data.
- CAMS GFAS v1.4.2 is a promising 2026 fire-only model, but no files were retrieved because authenticated CDS/ADS API access and manual terms acceptance are needed. It would not measure all-source gross emissions even if obtained.
- Other open products were checked: NASA FIRMS active-fire API requires a MAP_KEY and reports detections, not emissions; ESA FireCCI51 ends in 2020; Hansen Global Forest Change v1.13 covers annual loss through 2025; and the previously checked Global Forest Watch alerts API required a key. None provided retrieved RFO monthly emissions for 2026.
- NDVI/EVI are vegetation-condition proxies, not biomass change, carbon sequestration, or greenhouse-gas flux.
- The reserve boundary is used for the mapped area; a separate 15 km external ring is documented in the assessment and is not included in the reserve zone dataset.
- No local emission factors, verified disturbance activity series, burn-area totals, gas-flux measurements, or pool-specific carbon changes are available in this repository. Therefore gross emissions and net carbon balance are not quantified.

## Scientific sources

The full bibliography is in [`OWR_Carbon_2026.md`](OWR_Carbon_2026.md). Key source catalogs and guidance:

- [Microsoft Planetary Computer Sentinel-2 L2A](https://planetarycomputer.microsoft.com/dataset/sentinel-2-l2a)
- [NASA Terra MODIS MOD17A2H.061 collection](https://planetarycomputer.microsoft.com/api/stac/v1/collections/modis-17A2H-061)
- [Microsoft Planetary Computer Landsat Collection 2 L2](https://planetarycomputer.microsoft.com/dataset/landsat-c2-l2)
- [Microsoft Planetary Computer Sentinel-1 RTC](https://planetarycomputer.microsoft.com/dataset/sentinel-1-rtc)
- [NASA Earthdata CMR granule search](https://cmr.earthdata.nasa.gov/search/granules)
- [IPCC 2019 Refinement, AFOLU Volume 4](https://www.ipcc-nggip.iges.or.jp/public/2019rf/vol4.html)
- [UNESCO Okapi Wildlife Reserve](https://whc.unesco.org/en/list/718/)

## Licensing and attribution

Boundary data is retained as provided in the repository. Basemap tiles are from OpenStreetMap contributors; the interactive maps display OSM attribution. Satellite products and catalog records are attributed to their respective providers in the report, metadata, and data tables.
