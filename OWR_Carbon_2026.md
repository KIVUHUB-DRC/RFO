# Okapi Wildlife Reserve
## Carbon and Forest Assessment

**Assessment date:** 4 November 2026
**Reporting period:** 1 January–31 October 2026
**Spatial reference:** the RFO GeoJSON boundary for WDPA site 124389
**Status:** preliminary, boundary-based screening assessment; not a verified forest-carbon inventory

> **Scope limitation.** The supplied research prompt ends mid-sentence after “Clearly distinguish observed 202…”. This assessment addresses the objectives and dates supplied before that cutoff. It does not infer the missing instructions.

## Executive findings

The RFO boundary is a valid polygon for the Okapi Wildlife Reserve. Its WGS84 geodesic area is **13,939.55 km²** (1,393,955 ha), consistent with the GeoJSON `GIS_AREA` attribute. The same feature reports `REP_AREA = 13,726.25 km²`, a 1.55% difference. Spatial calculations below use the polygon as requested, not the smaller reported-area attribute [1].

Sentinel-2 surface-reflectance imagery was retrieved and analyzed for monthly vegetation-condition indices. No plot inventory, biomass raster, soil-carbon layer, or boundary-clipped annual loss/alert series is available. The imagery therefore does not support a defensible observed reserve-wide carbon stock, 2026 emissions total, or net greenhouse-gas balance. The numerical stock and uptake values below are **sensitivity illustrations**, not measurements or creditable removals.

The strongest local evidence is about ecosystem and pressure context: UNESCO describes the reserve as predominantly Ituri forest, including evergreen, semi-evergreen and swamp forests, and identifies agricultural encroachment along roads and artisanal mining among management challenges [2]. Global Forest Watch’s integrated-alert catalogue had a 4 November 2026 version covering “present” alerts, but its spatial query endpoint requires an API key. No alert counts or loss areas are therefore attributed to the reserve in this report [11].

### Key data at a glance

| Indicator | Result | Evidence class and interpretation |
|---|---:|---|
| RFO boundary area | 13,939.55 km² | Geodesic area calculated from the supplied polygon [1] |
| Reported WDPA area | 13,726.25 km² | Attribute in the source feature; 1.55% below the measured polygon area [1] |
| 15 km external buffer | 8,683.79 km² | GIS-derived pressure/leakage screening ring; not a legal buffer boundary |
| Illustrative live aboveground carbon stock | 209–348 Mt C | Uniform 150–250 Mg C/ha assumptions applied to all reserve hectares; not observed biomass or a confidence interval |
| African intact-forest sink reference | 0.66 (95% CI: 0.53–0.79) Mg C ha⁻¹ yr⁻¹ | Mean from 244 plots across 11 African countries for 1985–2015; not OWR-specific [3] |
| Area-scaled gross uptake scenario, annual | 0.92 (0.74–1.10) Mt C yr⁻¹ | Regional sink rate multiplied by all RFO hectares; not a measurement of reserve uptake |
| Area-scaled gross uptake scenario, Jan–Oct | 0.77 (0.62–0.92) Mt C | 304/365 prorating of the regional rate; excludes emissions and other carbon pools |
| Sentinel-2 vegetation-condition indices | Monthly mean NDVI 0.424–0.481; clear-land coverage 23.7–97.3% | 60 selected tile-month scenes, 100 m grid; not biomass or carbon flux [12] |
| Observed OWR 2026 net carbon balance | Not quantified | No complete, boundary-clipped activity data and carbon-pool change estimates available |

Stock values are in metric tonnes of carbon (C); CO₂-equivalent mass is calculated using 44/12. Results should not be read as verified stocks, annual emissions, offset claims, or REDD+ credits.

## Boundary and spatial method

The feature in [`RFO Limit.json`](RFO%20Limit.json) is a valid Polygon with 3,439 exterior-ring coordinates, `SITE_ID = 124389`, and name “Okapi Wildlife Reserve.” Its geometry bounds are approximately 27.985–29.084°E and 0.965–2.478°N.

Area was measured geodesically on the WGS84 ellipsoid. For the requested 15 km leakage-pressure zone, the polygon was projected to UTM zone 35N (EPSG:32635), buffered by 15,000 m, and the reserve itself removed [1]:

| Spatial measure | Area |
|---|---:|
| RFO boundary, geodesic | 13,939.55 km² |
| RFO `REP_AREA` attribute | 13,726.25 km² |
| 15 km buffer including reserve | 22,622.01 km² |
| 15 km external ring only | 8,683.79 km² |

The 15 km ring is a computed analysis zone, not an independently supplied or legally designated boundary. UNESCO describes a wider 50 km buffer zone; the two should not be conflated [2]. Sentinel-2 was summarized within the reserve only; the external ring and socioeconomic layers were not analyzed.

## Data inventory and evidence register

This register distinguishes processed pixels, scene/footprint inventories, and regional research. Catalogued scenes or footprint metadata do not imply that their measurement files were downloaded or analyzed.

| Dataset or study | Coverage and role | OWR extraction and limitation |
|---|---|---|
| RFO GeoJSON [1] | WDPA site 124389; reserve polygon and basis for the 15 km external buffer | Polygon validated and measured; Sentinel-2 pixels were also analyzed against this boundary |
| UNESCO site description [2] | Site-level habitat, management context, and documented pressure pathways | Context only; not a 2026 monitoring dataset |
| Hubau et al. [3] | 244 structurally intact African forest plots in 11 countries; 1968–2015 observations; regional live-biomass sink rate | No OWR plot-level estimate; rate used only as a labeled scenario |
| Saatchi et al. [4] | Pantropical early-2000s live-biomass carbon map; 1 km; above- and belowground biomass | Not clipped to RFO boundary; not an OWR stock estimate |
| Spawn et al. [5] | Harmonized global above- and belowground biomass-carbon maps for 2010; 300 m; uncertainty mapped | Not extracted; historical benchmark, not 2026 monitoring |
| Baccini et al. [6] | MODIS-based tropical aboveground biomass change, 2003–2014 | Global/tropical result; cannot be assigned to OWR |
| Hansen et al. [7] | Landsat forest-cover change at 30 m; study period 2000–2012 | Original study does not cover 2015–2025 or 2026 |
| Curtis et al. [8] | Global attribution of forest-loss drivers beginning in 2001 | Broad global attribution; no reserve-specific driver totals |
| SoilGrids 2.0 [9] | Global soil predictions at 250 m, six depth intervals to 200 cm, with uncertainty | No SOC stock extracted; wetland/peat conditions need local checks |
| IPCC AFOLU guidance [10] | National greenhouse-gas inventory methods | Methodological reference, not a local dataset |
| GFW integrated alerts [11] | Catalogue version v20261104; archive described from 2019 to present | Spatial query required an API key; no alert counts or areas used |
| Sentinel-2 L2A [12] | 666 STAC items intersecting the RFO query; six MGRS tiles represented each month | 60 least-cloudy tile-month scenes processed to 100 m NDVI/EVI; vegetation indices only |
| Landsat Collection 2 L2 [13] | 70 STAC items intersecting the RFO query | Acquisition inventory only; no Landsat raster metrics calculated |
| Sentinel-1 RTC [14] | 231 STAC items intersecting the RFO query | Acquisition inventory only; no radar backscatter metrics calculated |
| GEDI L2A V003 [15] | 9 CMR granule footprints intersect the RFO (Jan–Mar) | Footprint metadata only; GEDI HDF5 measurements not analyzed |
| NISAR L2 GCOV provisional [15] | 95 CMR granule footprints intersect the RFO (Jun–Oct) | Footprint metadata only; raster/backscatter data not analyzed |
| OCO-2 / OCO-3 [15] | 315 / 219 granules returned for surrounding-box searches; zero footprint polygons intersected the RFO | No local atmospheric retrievals used; XCO₂ concentration is not reserve-scale carbon flux |
| GOSAT / GOSAT-2 / TanSat [15] | No 2026 CMR granules found for the queried collections and area | No reserve measurements used; the queried TanSat archive ends in 2020 |
| ESA Biomass [16] | Mission data availability opened 26 January 2026 | No reserve acquisition was queried or processed |

For NASA CMR entries, the surrounding-box result was further checked against each returned granule polygon. Scene counts are catalog metadata, not necessarily unique acquisition dates or independent spatial samples.

The [carbon-accounting CSV](OWR_Carbon_2026.csv) and its SQLite table retain blank values for unmeasured carbon quantities. Separate files provide the processed [monthly satellite indices](OWR_Satellite_2026.csv), [scene/granule inventory](OWR_Satellite_Scenes_2026.csv), and [mission catalog status](OWR_Mission_Catalog_2026.csv). The SQLite database stores these in separate satellite tables and does not substitute NDVI/EVI for carbon flux.

## Satellite observations: January–October 2026

Sentinel-2 L2A surface-reflectance assets were queried from the Microsoft Planetary Computer STAC catalog using the RFO geometry. Of 666 returned items, one least-cloudy acquisition was selected for each of the six intersecting MGRS tiles in each month (60 scenes total). The rasters were aligned to a 100 m EPSG:32635 grid; tile overlaps were filled in ascending scene-cloud order so a grid cell was represented once. Reserve coverage is rasterized by grid-cell center. Sentinel-2 Scene Classification Layer classes 4 (vegetation) and 5 (bare soil) were retained; clouds, shadows, water, and other classes were excluded. Nonpositive reflectance, non-finite indices, NDVI outside −1 to 1, and EVI outside −1 to 2 were excluded as invalid. Surface reflectance used the collection scale factor of 0.0001.

NDVI was calculated as `(NIR − red) / (NIR + red)` and EVI as `2.5 × (NIR − red) / (NIR + 6 × red − 7.5 × blue + 1)`, using bands B08, B04, and B02. The coverage column is the share of the reserve’s 100 m grid cells with a valid clear-land observation in that monthly mosaic. Scene cloud cover is the mean catalog cloud percentage of the six selected scenes; it is not the measured cloud fraction over the reserve. Monthly scenes may have different acquisition dates across tiles.

| Month | Scenes | Clear-land coverage | Mean NDVI | Mean EVI |
|---|---:|---:|---:|---:|
| Jan | 6 | 86.185% | 0.433769 | 0.431366 |
| Feb | 6 | 97.268% | 0.448474 | 0.443533 |
| Mar | 6 | 88.606% | 0.423853 | 0.439760 |
| Apr | 6 | 82.734% | 0.474717 | 0.501987 |
| May | 6 | 96.869% | 0.479097 | 0.504465 |
| Jun | 6 | 65.070% | 0.434487 | 0.497680 |
| Jul | 6 | 81.871% | 0.457373 | 0.476656 |
| Aug | 6 | 95.357% | 0.456134 | 0.473179 |
| Sep | 6 | 23.657% | 0.464063 | 0.478540 |
| Oct | 6 | 74.337% | 0.480665 | 0.510248 |

Coverage is especially low in September, so that month’s mean represents a limited subset of the reserve. The monthly index differences should not be interpreted as a trend in biomass, growth, sequestration, or carbon loss: they are affected by cloud masking, acquisition timing, canopy/soil reflectance, and the limited scene selection. NDVI/EVI are vegetation-condition proxies and do not quantify aboveground biomass, soil carbon, or greenhouse-gas flux.

The STAC inventory also contains 70 Landsat Collection 2 Level-2 items and 231 Sentinel-1 RTC items intersecting the RFO query. These were inventoried but not raster-processed. NASA CMR metadata searches identified nine GEDI L2A and 95 provisional NISAR L2 GCOV granule footprints intersecting the boundary; their measurement files were not analyzed. OCO-2 and OCO-3 surrounding-box searches returned 315 and 219 granules, respectively, but none of the returned granule polygons intersected the reserve. No 2026 GOSAT, GOSAT-2, or TanSat granules were found for the queried collections and area; the queried TanSat archive ends in 2020. ESA announced open access to Biomass mission data on 26 January 2026, but no RFO Biomass acquisition was queried or processed. Atmospheric concentration and footprint metadata are not substitutes for reserve-scale carbon flux.

### October spatial screening layer

The downloadable [`RFO_Oct2026_NDVI_Zones.geojson`](RFO_Oct2026_NDVI_Zones.geojson) contains **3,070** retained 2 km grid cells clipped to the RFO polygon. It was generated from one least-cloudy Sentinel-2 L2A scene per MGRS tile for October 2026, with the same 100 m alignment, clear-land SCL mask, and reflectance/index validity filters described above. Each cell reports mean NDVI/EVI and the percentage of reserve grid-cell centers with valid, clear-land observations; cells below 25% valid coverage are omitted. Average valid-cell coverage among included cells was 88.48%.

For cartographic screening only, included cell NDVI means were divided into four **relative October quartiles**, with thresholds at 0.468411, 0.484149, and 0.496819. These are sample-relative bins, not ecological thresholds or validated forest-condition classes. The map uses four distinct colors and a legend with the numeric breaks; missing/low-coverage cells are not assigned a class. A zone is not a deforestation, degradation, biomass, or emissions determination. The feature collection metadata contains the processing definitions, source, thresholds, and caveats; [`scripts/build_rfo_zones.py`](scripts/build_rfo_zones.py) reproduces the layer from the RFO boundary and public STAC assets.

## Gross greenhouse-gas emissions requested

The requested monthly fields—`gross_emissions_co2e_all_gases__Mg`, `gross_emissions_co2e_non_co2__Mg`, and `gross_emissions_co2e_co2_only__Mg`—are **not quantifiable from the satellite evidence assembled**. The monthly values are deliberately blank in the CSV and SQL table; blank means unknown/not measured, **not zero**. A satellite acquisition count, canopy index, or atmospheric CO₂ concentration is not an emitted mass.

| Month (2026) | All gases (Mg CO₂e) | Non-CO₂ gases (Mg CO₂e) | CO₂ only (Mg CO₂e) | Status |
|---|---:|---:|---:|---|
| Jan | — | — | — | Not quantifiable |
| Feb | — | — | — | Not quantifiable |
| Mar | — | — | — | Not quantifiable |
| Apr | — | — | — | Not quantifiable |
| May | — | — | — | Not quantifiable |
| Jun | — | — | — | Not quantifiable |
| Jul | — | — | — | Not quantifiable |
| Aug | — | — | — | Not quantifiable |
| Sep | — | — | — | Not quantifiable |
| Oct | — | — | — | Not quantifiable |

Sentinel-2 NDVI/EVI can help screen vegetation condition but do not by themselves establish land conversion, affected biomass, or flux. Landsat and Sentinel-1 scenes and GEDI/NISAR granules were inventoried but not processed into disturbance areas or stock changes. OCO-2/3 are not reserve-scale emission-flux instruments; no intersecting footprint polygons were identified in the metadata query. GOSAT/TanSat and ESA Biomass did not yield processed reserve-specific observations for these fields. No validated fire/burn area, disturbance activity data, reserve-specific carbon pools, CH₄/N₂O fluxes, or applicable local emission factors were assembled.

Quantification would require validated monthly activity data (including land-use transitions and fire), pre-event carbon stocks by pool, documented emission factors, applicable CH₄/N₂O factors and CO₂e conversion basis, and uncertainty/quality controls. Gross all-gases emissions must have a defined gas/accounting boundary and reconcile CO₂-only and non-CO₂ components without double-counting. Until those inputs exist, reporting a numerical emissions value would imply unsupported precision.

The accompanying [`OWR_Emissions_2026.csv`](OWR_Emissions_2026.csv) preserves all ten requested months and satellite-coverage context. [`OWR_Emissions_Metadata_2026.json`](OWR_Emissions_Metadata_2026.json) defines the requested fields, units, measurement status, per-mission data availability, limitations, and requirements for a future quantification. The corresponding SQLite table is `monthly_gross_emissions`; it is separate from carbon-accounting records.

## Carbon stocks

### What is and is not known

No reserve-specific estimate of aboveground biomass, belowground biomass, deadwood, litter, or soil organic carbon can be verified from the local data. The Sentinel-2 vegetation indices reported above do not estimate these carbon pools. The reserve’s swamp forests and other wet areas make soil and wetland carbon particularly important; they also mean that an aboveground-tree-only estimate would not represent total ecosystem carbon. There are no local soil cores, peat-depth measurements, or mapped soil-carbon results in the evidence reviewed. SoilGrids 2.0 offers global soil organic carbon predictions at 250 m and six depth intervals, but these data have not been clipped to the boundary and would require wetland-specific validation [9].

Pantropical biomass maps such as Saatchi et al. (2011) demonstrate how live biomass carbon can be estimated by combining plot inventories, lidar and satellite imagery [4]. Spawn et al. later harmonized above- and belowground biomass-carbon products globally at 300 m for 2010 and reported spatial uncertainty [5]. These are potential inputs for a boundary-clipped analysis, but neither publication’s regional totals nor unprocessed map values are an estimate for this reserve. A raster must actually be intersected with the RFO polygon and its uncertainty propagated before reporting an OWR stock.

### Scale illustration—not a reserve estimate

To make the area-to-stock scaling explicit, the table below applies hypothetical uniform aboveground carbon densities to the full RFO polygon. The density values are sensitivity inputs only; they are not extracted from a local map or validated inventory. The calculation excludes belowground biomass, deadwood, litter, soil, wetlands, and non-forest portions of the boundary.

| Assumed aboveground carbon density | Illustrative stock across full polygon | CO₂ mass equivalent* |
|---:|---:|---:|
| 150 Mg C/ha | 209 Mt C | 767 Mt CO₂ |
| 200 Mg C/ha | 279 Mt C | 1,022 Mt CO₂ |
| 250 Mg C/ha | 348 Mt C | 1,278 Mt CO₂ |

These are not confidence limits, verified bounds, or creditable carbon. They would be scaled down to the actual forested area and replaced with pixel-level biomass estimates. The conversion is `CO₂ = C × 44/12`; the resulting CO₂-equivalent mass describes stored carbon, not annual emissions avoided.

## Uptake and sequestration potential

Hubau et al. (2020) reported a long-term aboveground live-biomass sink for structurally intact African tropical forests of **0.66 Mg C ha⁻¹ yr⁻¹** (95% CI: 0.53–0.79) over the three decades to 2015, based on 244 plots across 11 countries [3]. The authors also report evidence of increased carbon losses after 2010. This is a regional historical reference—not a measured 2026 rate for OWR, and not an estimate of soil-carbon change or all greenhouse gases.

If that rate and its reported confidence interval were applied uniformly to every hectare of the RFO polygon, the resulting screening scenario would be:

- **0.92 Mt C/year** (range **0.74–1.10 Mt C/year**; about **3.37 Mt CO₂/year** at the mean) across the full polygon; and
- **0.77 Mt C** (range **0.62–0.92 Mt C**; about **2.81 Mt CO₂** at the mean) prorated over the 304 days from 1 January through 31 October 2026.

This is a gross, area-scaled scenario only. It assumes all polygon area behaves like the study’s sampled African tropical forests, ignores local forest cover and disturbance, and cannot be described as observed 2026 sequestration. The range propagates the study’s reported confidence interval but does not include uncertainty in applying that rate to OWR. Actual net ecosystem uptake could be lower or temporarily reversed by mortality, drought, degradation, clearing, or fire. Satellite biomass-flux studies also show that gains and losses can reverse the net balance at broad tropical scales, reinforcing the need to measure both [6]. A measured reserve rate would require repeat biomass measurements or an appropriate time series and explicit treatment of all relevant carbon pools [10].

## Deforestation, degradation, emissions, and 2026 observations

UNESCO identifies road-corridor agricultural encroachment, immigration pressure, and artisanal mining as management concerns. It also describes the broader Ituri forest as among the better-preserved parts of the Congo Basin [2]. These are credible context and risk indicators, but they do **not** establish the location, area, timing, or carbon emissions of disturbance during January–October 2026. Global studies classify loss drivers such as commodity production, forestry, agriculture, wildfire, and urbanization, but these broad categories cannot be treated as evidence of a particular OWR event [8].

The GFW Data API catalogue lists `gfw_integrated_alerts` version `v20261104`, updated 4 November 2026, with a content-date range ending 4 November 2026 and a description of alerts from 2019 to the present [11]. The product is potentially relevant to the requested reporting period. However, the API returned “Request is missing valid API key” for a direct, read-only spatial query using the RFO geometry. Accordingly:

- no alert pixels, disturbed hectares, confidence classes, or 2026 loss totals are reported;
- an alert is a monitoring signal, not by itself a verified deforestation event or a carbon-emission measurement; and
- the 2019–2026 alert feed does not, by itself, provide the full 2015–2025 historical reference requested.

Plausible direct emission pathways to assess with spatial data and field validation are (1) forest conversion for cultivation and settlement, especially along established roads; (2) artisanal mining and associated access/clearing; (3) selective logging and other canopy degradation; and (4) forest fire or biomass burning. These should be treated as **risk pathways**, not confirmed 2026 events. Swamp and wetland disturbance may also change methane and soil-carbon fluxes. No local activity data or CH₄/N₂O measurements were available, so these fluxes are unquantified. IPCC inventory guidance calls for consistent land representation, activity data, and locally appropriate stock-change or emission factors; those reserve-specific inputs are not assembled here [10].

The likely high-stock zones are contiguous, mature, closed-canopy forest, while accessible road corridors and known development/mining areas are priority disturbance-screening zones. Without a biomass map, disturbance time series, and mapped management/ecological zones, no defensible hotspot ranking or zone-level stock estimate can be assigned. UNESCO’s published core (282,000 ha), traditional-use (950,000 ha), and development (18,000 ha) areas provide useful management context, but their geometries were not supplied and their published areas do not sum to the full boundary.

## Net balance and conclusions

The observed January–October 2026 net carbon balance is **not quantifiable from the reviewed data**. The necessary terms—changes in live biomass, dead organic matter and soil carbon; emissions from land conversion and degradation; fire; and relevant non-CO₂ fluxes—are not all measured. The 0.77 Mt C scenario above is an extrapolated gross uptake reference, not a net balance, and cannot be offset against an unmeasured loss estimate.

The reserve’s large area and intact Ituri forest make it important for maintaining Congo Basin carbon stocks and the long-term forest sink. The reserve’s mitigation value depends on persistence: preventing forest conversion and degradation avoids releases of existing biomass and soil carbon while retaining future uptake. That conservation value is not equivalent to a quantified REDD+ credit; a crediting claim would additionally need a defensible baseline, leakage and permanence treatment, safeguards, monitoring, reporting, verification, and applicable DRC authorization.

### Evidence needed to complete a quantitative assessment

1. Intersect the RFO polygon and computed 15 km ring with annual forest-cover/loss data for 2015–2025 and alerts dated through 31 October 2026; validate disturbance classes using the retrieved Sentinel-2 imagery, Landsat time series, and local monitoring [7, 8, 11–14].
2. Clip a biomass-carbon map to the same geometry; compare a historical benchmark such as the 2010 harmonized product with newer observations, and report forest area, pool definitions, resolution, uncertainty, and area-weighted totals [4, 5].
3. Add soil organic-carbon and wetland/peat information, with field sampling where product uncertainty or wetland extent is material [9].
4. Obtain geometries for the reserve’s management zones and analyze them separately; distinguish road-accessible/development areas from intact forest interiors.
5. Estimate emissions and removals using an IPCC-consistent land representation, activity data, locally appropriate emission factors, and uncertainty ranges. Include fire and non-CO₂ fluxes where material [10].

## Scientific sources and technical references

1. **Reserve boundary.** WDPA site 124389, RFO GeoJSON, [`RFO Limit.json`](RFO%20Limit.json) (local repository source; boundary geometry and feature attributes).
2. **UNESCO World Heritage Centre.** “Okapi Wildlife Reserve,” World Heritage List site 718. Site description and management context. [https://whc.unesco.org/en/list/718/](https://whc.unesco.org/en/list/718/).
3. **Hubau, W., et al. (2020).** “Asynchronous carbon sink saturation in African and Amazonian tropical forests.” *Nature*, 579(7797), 80–87. African plot-network estimate of aboveground live-biomass sink and its historical trend; regional, not reserve-specific. [https://doi.org/10.1038/s41586-020-2035-0](https://doi.org/10.1038/s41586-020-2035-0).
4. **Saatchi, S. S., et al. (2011).** “Benchmark map of forest carbon stocks in tropical regions across three continents.” *Proceedings of the National Academy of Sciences*, 108(24), 9899–9904. Early-2000s pantropical live-biomass map combining plots, lidar, and satellite imagery. [https://doi.org/10.1073/pnas.1019576108](https://doi.org/10.1073/pnas.1019576108).
5. **Spawn, S. A., et al. (2020).** “Harmonized global maps of above and belowground biomass carbon density in the year 2010.” *Scientific Data*, 7, Article 112. 300 m harmonized biomass-carbon maps with uncertainty. [https://doi.org/10.1038/s41597-020-0444-4](https://doi.org/10.1038/s41597-020-0444-4).
6. **Baccini, A., et al. (2017).** “Tropical forests are a net carbon source based on aboveground measurements of gain and loss.” *Science*, 358(6360), 230–234. MODIS-based analysis of tropical aboveground biomass changes; demonstrates the importance of accounting for both gains and losses. [https://doi.org/10.1126/science.aam5962](https://doi.org/10.1126/science.aam5962).
7. **Hansen, M. C., et al. (2013).** “High-Resolution Global Maps of 21st-Century Forest Cover Change.” *Science*, 342(6160), 850–853. Landsat-based global forest-change mapping at 30 m for 2000–2012. [https://doi.org/10.1126/science.1244693](https://doi.org/10.1126/science.1244693).
8. **Curtis, P. G., et al. (2018).** “Classifying drivers of global forest loss.” *Science*, 361(6407), 1108–1111. Global forest-loss driver classification; useful as a framework, not as local OWR attribution. [https://doi.org/10.1126/science.aau3445](https://doi.org/10.1126/science.aau3445).
9. **Poggio, L., et al. (2021).** “SoilGrids 2.0: producing soil information for the globe with quantified spatial uncertainty.” *SOIL*, 7, 217–240. Global soil-property predictions at 250 m and six depths to 200 cm, including soil organic carbon. [https://doi.org/10.5194/soil-7-217-2021](https://doi.org/10.5194/soil-7-217-2021).
10. **IPCC (2019).** *2019 Refinement to the 2006 IPCC Guidelines for National Greenhouse Gas Inventories, Volume 4: Agriculture, Forestry and Other Land Use.* Inventory methods, land representation, and uncertainty treatment. [https://www.ipcc-nggip.iges.or.jp/public/2019rf/vol4.html](https://www.ipcc-nggip.iges.or.jp/public/2019rf/vol4.html).
11. **Global Forest Watch Data API.** Integrated alerts dataset, version `v20261104`; catalogue metadata and API documentation. The dataset metadata describes an alert archive from 2019 to present; spatial query access requires an API key. [Dataset](https://data-api.globalforestwatch.org/dataset/gfw_integrated_alerts/v20261104); [API documentation](https://data-api.globalforestwatch.org/docs).
12. **Microsoft Planetary Computer.** Sentinel-2 Level-2A collection catalogue and STAC assets. Scene discovery and the 2026 clipped surface-reflectance analysis described above. [https://planetarycomputer.microsoft.com/dataset/sentinel-2-l2a](https://planetarycomputer.microsoft.com/dataset/sentinel-2-l2a).
13. **Microsoft Planetary Computer.** Landsat Collection 2 Level-2 catalogue. Scene-inventory source; no reserve reflectance indices calculated. [https://planetarycomputer.microsoft.com/dataset/landsat-c2-l2](https://planetarycomputer.microsoft.com/dataset/landsat-c2-l2).
14. **Microsoft Planetary Computer.** Sentinel-1 RTC catalogue. Scene-inventory source; no reserve backscatter metrics calculated. [https://planetarycomputer.microsoft.com/dataset/sentinel-1-rtc](https://planetarycomputer.microsoft.com/dataset/sentinel-1-rtc).
15. **NASA Earthdata Common Metadata Repository (CMR).** Granule and collection metadata searches for GEDI, NISAR, OCO-2, OCO-3, GOSAT, GOSAT-2, and TanSat. Search-result polygons were checked against the RFO boundary; metadata footprints are not measurement values. [Granule search API](https://cmr.earthdata.nasa.gov/search/granules); [collection search API](https://cmr.earthdata.nasa.gov/search/collections).
16. **European Space Agency.** “Biomass mission.” Mission description and data-access announcement; mission availability alone does not establish an RFO observation. [https://www.esa.int/Applications/Observing_the_Earth/FutureEO/Biomass](https://www.esa.int/Applications/Observing_the_Earth/FutureEO/Biomass).
17. **OWR monthly emissions data and metadata.** `OWR_Emissions_2026.csv` and `OWR_Emissions_Metadata_2026.json` (repository files). Ten monthly rows with all requested emissions quantities explicitly unquantified; the files record satellite coverage and explain the missing activity data, emission factors, and gas-flux measurements.

**Citation and interpretation note.** Peer-reviewed regional studies and global products provide methods, historical context, or candidate inputs; none is represented here as an OWR measurement unless explicitly stated. All reserve-wide derived figures are calculated from the local RFO geometry. The screening scenarios are not a substitute for an IPCC-consistent inventory or project-level measurement, reporting, and verification.
