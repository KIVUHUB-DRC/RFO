# Okapi Wildlife Reserve: carbon assessment, January–October 2026

**Assessment date:** 4 November 2026
**Reporting period:** 1 January–31 October 2026
**Spatial reference:** the RFO GeoJSON boundary for WDPA site 124389
**Status:** preliminary, boundary-based screening assessment; not a verified forest-carbon inventory

> **Scope limitation.** The supplied research prompt ends mid-sentence after “Clearly distinguish observed 202…”. This assessment addresses the objectives and dates supplied before that cutoff. It does not infer the missing instructions.

## Executive findings

The RFO boundary is a valid polygon for the Okapi Wildlife Reserve. Its WGS84 geodesic area is **13,939.55 km²** (1,393,955 ha), matching the GeoJSON `GIS_AREA` attribute. The same feature reports `REP_AREA = 13,726.25 km²`, a 1.55% difference. Spatial calculations below use the polygon as requested, not the smaller reported-area attribute.

No plot inventory, biomass raster, soil-carbon layer, or boundary-clipped annual loss/alert series is included in the repository. Consequently, a defensible observed reserve-wide carbon stock, 2026 emissions total, or net greenhouse-gas balance cannot be calculated from the evidence available here. The numerical stock and uptake values below are **sensitivity illustrations**, not measurements or creditable removals.

The strongest local evidence is about ecosystem and pressure context: UNESCO describes the reserve as predominantly Ituri forest, including evergreen, semi-evergreen and swamp forests, and identifies agricultural encroachment along roads and artisanal mining among management challenges. Global Forest Watch’s integrated-alert catalogue had a 4 November 2026 version covering “present” alerts, but its spatial query endpoint requires an API key. No alert counts or loss areas are therefore attributed to the reserve in this report.

## Boundary and spatial method

The feature in [`RFO_WDOECM_Nov2026_Public_124389_shp-polygons.json`](RFO_WDOECM_Nov2026_Public_124389_shp-polygons.json) is a valid Polygon with 3,439 exterior-ring coordinates, `SITE_ID = 124389`, and name “Okapi Wildlife Reserve.” Its geometry bounds are approximately 27.985–29.084°E and 0.965–2.478°N.

Area was measured geodesically on the WGS84 ellipsoid. For the requested 15 km leakage-pressure zone, the polygon was projected to UTM zone 35N (EPSG:32635), buffered by 15,000 m, and the reserve itself removed:

| Spatial measure | Area |
|---|---:|
| RFO boundary, geodesic | 13,939.55 km² |
| RFO `REP_AREA` attribute | 13,726.25 km² |
| 15 km buffer including reserve | 22,622.01 km² |
| 15 km external ring only | 8,683.79 km² |

The 15 km ring is a computed analysis zone, not an independently supplied or legally designated boundary. UNESCO describes a wider 50 km buffer zone; the two should not be conflated. No satellite or socioeconomic layer was spatially summarized within either the reserve or external ring.

## Carbon stocks

### What is and is not known

No reserve-specific estimate of aboveground biomass, belowground biomass, deadwood, litter, or soil organic carbon can be verified from the local data. The reserve’s swamp forests and other wet areas make soil and wetland carbon particularly important; they also mean that an aboveground-tree-only estimate would not represent total ecosystem carbon. There are no local soil cores, peat-depth measurements, or mapped soil-carbon results in the evidence reviewed.

Pantropical biomass maps such as Saatchi et al. (2011) demonstrate how live biomass carbon can be estimated by combining plot inventories, lidar and satellite imagery. They are useful inputs for a boundary-clipped analysis, but the publication’s regional totals are **not** an estimate for this reserve. A raster must actually be intersected with the RFO polygon and its uncertainty propagated before reporting an OWR stock.

### Scale illustration—not a reserve estimate

To make the area-to-stock scaling explicit, the table below applies hypothetical uniform aboveground carbon densities to the full RFO polygon. The density values are sensitivity inputs only; they are not extracted from a local map or validated inventory. The calculation excludes belowground biomass, deadwood, litter, soil, wetlands, and non-forest portions of the boundary.

| Assumed aboveground carbon density | Illustrative stock across full polygon | CO₂ mass equivalent* |
|---:|---:|---:|
| 150 Mg C/ha | 209 Mt C | 767 Mt CO₂ |
| 200 Mg C/ha | 279 Mt C | 1,022 Mt CO₂ |
| 250 Mg C/ha | 348 Mt C | 1,278 Mt CO₂ |

These are not confidence limits, verified bounds, or creditable carbon. They would be scaled down to the actual forested area and replaced with pixel-level biomass estimates. The conversion is `CO₂ = C × 44/12`; the resulting CO₂-equivalent mass describes stored carbon, not annual emissions avoided.

## Uptake and sequestration potential

Hubau et al. (2020) reported a long-term aboveground biomass sink for African tropical forests of approximately **0.66 Mg C ha⁻¹ yr⁻¹** over 1985–2015. This is a regional historical reference—not a measured 2026 rate for OWR, and not an estimate of soil-carbon change or all greenhouse gases.

If that rate were applied uniformly to every hectare of the RFO polygon, the resulting screening scenario would be:

- **0.92 Mt C/year** (about **3.37 Mt CO₂/year**) across the full polygon; and
- **0.77 Mt C** (about **2.81 Mt CO₂**) prorated over the 304 days from 1 January through 31 October 2026.

This is a gross, area-scaled scenario only. It assumes all polygon area behaves like the study’s sampled African tropical forests, ignores local forest cover and disturbance, and cannot be described as observed 2026 sequestration. Actual net ecosystem uptake could be lower or temporarily reversed by mortality, drought, degradation, clearing, or fire. A measured reserve rate would require repeat biomass measurements or an appropriate time series and explicit treatment of all relevant carbon pools.

## Deforestation, degradation, emissions, and 2026 observations

UNESCO identifies road-corridor agricultural encroachment, immigration pressure, and artisanal mining as management concerns. It also describes the broader Ituri forest as among the better-preserved parts of the Congo Basin. These are credible context and risk indicators, but they do **not** establish the location, area, timing, or carbon emissions of disturbance during January–October 2026.

The GFW Data API catalogue lists `gfw_integrated_alerts` version `v20261104`, updated 4 November 2026, with a content-date range ending 4 November 2026 and a description of alerts from 2019 to the present. The product is potentially relevant to the requested reporting period. However, the API returned “Request is missing valid API key” for a direct, read-only spatial query using the RFO geometry. Accordingly:

- no alert pixels, disturbed hectares, confidence classes, or 2026 loss totals are reported;
- an alert is a monitoring signal, not by itself a verified deforestation event or a carbon-emission measurement; and
- the 2019–2026 alert feed does not, by itself, provide the full 2015–2025 historical reference requested.

Plausible direct emission pathways to assess with spatial data and field validation are (1) forest conversion for cultivation and settlement, especially along established roads; (2) artisanal mining and associated access/clearing; (3) selective logging and other canopy degradation; and (4) forest fire or biomass burning. These should be treated as **risk pathways**, not confirmed 2026 events. Swamp and wetland disturbance may also change methane and soil-carbon fluxes. No local activity data or CH₄/N₂O measurements were available, so these fluxes are unquantified.

The likely high-stock zones are contiguous, mature, closed-canopy forest, while accessible road corridors and known development/mining areas are priority disturbance-screening zones. Without a biomass map, disturbance time series, and mapped management/ecological zones, no defensible hotspot ranking or zone-level stock estimate can be assigned. UNESCO’s published core (282,000 ha), traditional-use (950,000 ha), and development (18,000 ha) areas provide useful management context, but their geometries were not supplied and their published areas do not sum to the full boundary.

## Net balance and conclusions

The observed January–October 2026 net carbon balance is **not quantifiable from the reviewed data**. The necessary terms—changes in live biomass, dead organic matter and soil carbon; emissions from land conversion and degradation; fire; and relevant non-CO₂ fluxes—are not all measured. The 0.77 Mt C scenario above is an extrapolated gross uptake reference, not a net balance, and cannot be offset against an unmeasured loss estimate.

The reserve’s large area and intact Ituri forest make it important for maintaining Congo Basin carbon stocks and the long-term forest sink. The reserve’s mitigation value depends on persistence: preventing forest conversion and degradation avoids releases of existing biomass and soil carbon while retaining future uptake. That conservation value is not equivalent to a quantified REDD+ credit; a crediting claim would additionally need a defensible baseline, leakage and permanence treatment, safeguards, monitoring, reporting, verification, and applicable DRC authorization.

### Evidence needed to complete a quantitative assessment

1. Intersect the RFO polygon and computed 15 km ring with annual forest-cover/loss data for 2015–2025 and alerts dated through 31 October 2026; validate disturbance classes using Sentinel-2/Landsat imagery and local monitoring.
2. Clip a current biomass-carbon map (and preferably repeat biomass estimates) to the same geometry; report forest area, pool definitions, resolution, uncertainty, and area-weighted totals.
3. Add soil organic-carbon and wetland/peat information, with field sampling where product uncertainty or wetland extent is material.
4. Obtain geometries for the reserve’s management zones and analyze them separately; distinguish road-accessible/development areas from intact forest interiors.
5. Estimate emissions and removals using an IPCC-consistent land representation, activity data, locally appropriate emission factors, and uncertainty ranges. Include fire and non-CO₂ fluxes where material.

## Sources

1. **RFO boundary:** `RFO_WDOECM_Nov2026_Public_124389_shp-polygons.json`, WDPA site 124389 (local repository file; geometry and attributes used in this assessment).
2. **UNESCO World Heritage Centre, Okapi Wildlife Reserve (site 718):** [https://whc.unesco.org/en/list/718/](https://whc.unesco.org/en/list/718/).
3. **Hubau et al. (2020), “Asynchronous carbon sink saturation in African and Amazonian tropical forests,” Nature 579, 80–87:** [https://doi.org/10.1038/s41586-020-2035-0](https://doi.org/10.1038/s41586-020-2035-0).
4. **Saatchi et al. (2011), “Benchmark map of forest carbon stocks in tropical regions across three continents,” PNAS 108, 9899–9904:** [https://doi.org/10.1073/pnas.1019576108](https://doi.org/10.1073/pnas.1019576108).
5. **IPCC, 2019 Refinement to the 2006 Guidelines, Volume 4 (AFOLU):** [https://www.ipcc-nggip.iges.or.jp/public/2019rf/vol4.html](https://www.ipcc-nggip.iges.or.jp/public/2019rf/vol4.html).
6. **Global Forest Watch Data API, integrated alerts v20261104:** [dataset metadata](https://data-api.globalforestwatch.org/dataset/gfw_integrated_alerts/v20261104); [API documentation](https://data-api.globalforestwatch.org/docs).
7. **Hansen et al. (2013), “High-Resolution Global Maps of 21st-Century Forest Cover Change,” Science 342, 850–853:** [https://doi.org/10.1126/science.1244693](https://doi.org/10.1126/science.1244693).
