# Okapi Wildlife Reserve carbon and satellite assessment

Public, preliminary, boundary-based screening of the Okapi Wildlife Reserve (RFO), Democratic Republic of the Congo. Reporting period: **1 January–31 October 2026**. The project uses the repository boundary `RFO Limit.json` (WDPA site 124389).

## Public project pages

- **[Landing page](https://kivuhub-drc.github.io/RFO/)** — overview, Leaflet reserve map, monthly satellite summary, and carbon-emissions status.
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
| [`OWR_Satellite_Scenes_2026.csv`](OWR_Satellite_Scenes_2026.csv) | Satellite scene and selected NASA CMR granule-footprint inventory. Catalog records do not necessarily represent processed measurements. |
| [`OWR_Mission_Catalog_2026.csv`](OWR_Mission_Catalog_2026.csv) | Mission-specific catalog/footprint counts, processing state, sources, and limitations. |
| [`OWR_Carbon_2026.csv`](OWR_Carbon_2026.csv) | Original monthly carbon-accounting export. Unmeasured fields remain blank. |

### Requested gross-emissions fields

All three fields are in **Mg CO₂e per reporting month and RFO boundary**:

- `gross_emissions_co2e_all_gases__Mg`
- `gross_emissions_co2e_non_co2__Mg`
- `gross_emissions_co2e_co2_only__Mg`

They are blank in every month with `data_status=NOT_QUANTIFIABLE`. Blank/null means **unknown or not measured**, not zero. Available optical/radar observations, canopy indices, atmosphere concentration measurements, and granule-footprint metadata do not constitute a validated gross-emissions inventory. The repository does not report unsupported emissions estimates. See the [metadata](OWR_Emissions_Metadata_2026.json) and [Methods page](https://kivuhub-drc.github.io/RFO/method.html).

## October spatial zones and map legend

The downloadable zone GeoJSON summarizes clear Sentinel-2 L2A observations from October 2026 in 2 km cells clipped to the reserve. It selects one least-cloudy scene per each of six MGRS tiles, aligns red/NIR/blue/SCL bands at 100 m, masks to SCL classes 4 and 5, and computes monthly pixel means. Cells with less than 25% valid clear-land coverage are omitted. Retained cell means are divided into four **data-relative October NDVI quartiles**; the actual breaks are in the GeoJSON `metadata.classification` object. These colors are not fixed forest classes, degradation alerts, biomass estimates, or emissions.

The corresponding reproducible script is [`scripts/build_rfo_zones.py`](scripts/build_rfo_zones.py). It requires Python packages `numpy`, `planetary-computer`, `pyproj`, `rasterio`, `requests`, and `shapely`, plus network access to the Microsoft Planetary Computer STAC service and signed public assets. Run from the repository root:

```bash
python scripts/build_rfo_zones.py
```

It reads `RFO Limit.json` and writes `RFO_Oct2026_NDVI_Zones.geojson`. Cloud availability, public catalogs, and signed URLs can change.

## Database additions

The SQLite database includes separate `satellite_monthly`, `satellite_scene_inventory`, `satellite_mission_catalog`, `satellite_zone_cells`, and `monthly_gross_emissions` tables. `satellite_zone_cells` contains the clipped October grid geometries as GeoJSON text with their NDVI/EVI and quartile attributes. The gross-emissions table retains the requested field names and SQL `NULL` values rather than replacing unknowns with zero. The `metadata` and `sources` tables document units, provenance, scope, and limitations. Existing monthly carbon-accounting values are preserved.

## Evidence and limits

- Sentinel-2 is the only imagery used to calculate spatial vegetation indices in this repository. Landsat and Sentinel-1 were catalogued but not raster-processed.
- GEDI and NISAR records are footprint metadata, not analyzed height/biomass/backscatter observations.
- OCO-2/3 are atmospheric concentration missions; no matching local intersecting footprint polygons were identified in the checked catalog responses. GOSAT/TanSat results and ESA Biomass mission availability do not constitute processed RFO data.
- NDVI/EVI are vegetation-condition proxies, not biomass change, carbon sequestration, or greenhouse-gas flux.
- The reserve boundary is used for the mapped area; a separate 15 km external ring is documented in the assessment and is not included in the reserve zone dataset.
- No local emission factors, verified disturbance activity series, burn-area totals, gas-flux measurements, or pool-specific carbon changes are available in this repository. Therefore gross emissions and net carbon balance are not quantified.

## Scientific sources

The full bibliography is in [`OWR_Carbon_2026.md`](OWR_Carbon_2026.md). Key source catalogs and guidance:

- [Microsoft Planetary Computer Sentinel-2 L2A](https://planetarycomputer.microsoft.com/dataset/sentinel-2-l2a)
- [Microsoft Planetary Computer Landsat Collection 2 L2](https://planetarycomputer.microsoft.com/dataset/landsat-c2-l2)
- [Microsoft Planetary Computer Sentinel-1 RTC](https://planetarycomputer.microsoft.com/dataset/sentinel-1-rtc)
- [NASA Earthdata CMR granule search](https://cmr.earthdata.nasa.gov/search/granules)
- [IPCC 2019 Refinement, AFOLU Volume 4](https://www.ipcc-nggip.iges.or.jp/public/2019rf/vol4.html)
- [UNESCO Okapi Wildlife Reserve](https://whc.unesco.org/en/list/718/)

## Licensing and attribution

Boundary data is retained as provided in the repository. Basemap tiles are from OpenStreetMap contributors; the interactive maps display OSM attribution. Satellite products and catalog records are attributed to their respective providers in the report, metadata, and data tables.
