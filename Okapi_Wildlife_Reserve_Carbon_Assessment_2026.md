# Okapi Wildlife Reserve
## Carbon and Forest Assessment

**Assessment date:** 4 November 2026
**Reporting period:** 1 January–31 October 2026
**Spatial reference:** the RFO GeoJSON boundary for WDPA site 124389
**Status:** preliminary, boundary-based screening assessment; not a verified forest-carbon inventory

> **Scope limitation.** The supplied research prompt ends mid-sentence after “Clearly distinguish observed 202…”. This assessment addresses the objectives and dates supplied before that cutoff. It does not infer the missing instructions.

## Executive findings

The RFO boundary is a valid polygon for the Okapi Wildlife Reserve. Its WGS84 geodesic area is **13,939.55 km²** (1,393,955 ha), consistent with the GeoJSON `GIS_AREA` attribute. The same feature reports `REP_AREA = 13,726.25 km²`, a 1.55% difference. Spatial calculations below use the polygon as requested, not the smaller reported-area attribute [1].

No plot inventory, biomass raster, soil-carbon layer, or boundary-clipped annual loss/alert series is included in the repository. Consequently, a defensible observed reserve-wide carbon stock, 2026 emissions total, or net greenhouse-gas balance cannot be calculated from the evidence available here. The numerical stock and uptake values below are **sensitivity illustrations**, not measurements or creditable removals.

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
| Observed OWR 2026 net carbon balance | Not quantified | No complete, boundary-clipped activity data and carbon-pool change estimates available |

Stock values are in metric tonnes of carbon (C); CO₂-equivalent mass is calculated using 44/12. Results should not be read as verified stocks, annual emissions, offset claims, or REDD+ credits.

## Boundary and spatial method

The feature in [`RFO_WDOECM_Nov2026_Public_124389_shp-polygons.json`](RFO_WDOECM_Nov2026_Public_124389_shp-polygons.json) is a valid Polygon with 3,439 exterior-ring coordinates, `SITE_ID = 124389`, and name “Okapi Wildlife Reserve.” Its geometry bounds are approximately 27.985–29.084°E and 0.965–2.478°N.

Area was measured geodesically on the WGS84 ellipsoid. For the requested 15 km leakage-pressure zone, the polygon was projected to UTM zone 35N (EPSG:32635), buffered by 15,000 m, and the reserve itself removed [1]:

| Spatial measure | Area |
|---|---:|
| RFO boundary, geodesic | 13,939.55 km² |
| RFO `REP_AREA` attribute | 13,726.25 km² |
| 15 km buffer including reserve | 22,622.01 km² |
| 15 km external ring only | 8,683.79 km² |

The 15 km ring is a computed analysis zone, not an independently supplied or legally designated boundary. UNESCO describes a wider 50 km buffer zone; the two should not be conflated [2]. No satellite or socioeconomic layer was spatially summarized within either the reserve or external ring.

## Data inventory and evidence register

This register distinguishes data products and regional research from results actually measured for the reserve. “Not extracted” means the source was reviewed or identified but its pixels or observations were not analyzed against the RFO polygon.

| Dataset or study | Coverage and role | OWR extraction and limitation |
|---|---|---|
| RFO GeoJSON [1] | WDPA site 124389; reserve polygon and basis for the 15 km external buffer | Polygon validated and measured; this is the sole spatial layer analyzed |
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

The source resolutions and study extents above describe the cited products/publications, not a completed OWR raster analysis. A product’s global availability does not establish that its estimate is accurate at the reserve scale.

## Carbon stocks

### What is and is not known

No reserve-specific estimate of aboveground biomass, belowground biomass, deadwood, litter, or soil organic carbon can be verified from the local data. The reserve’s swamp forests and other wet areas make soil and wetland carbon particularly important; they also mean that an aboveground-tree-only estimate would not represent total ecosystem carbon. There are no local soil cores, peat-depth measurements, or mapped soil-carbon results in the evidence reviewed. SoilGrids 2.0 offers global soil organic carbon predictions at 250 m and six depth intervals, but these data have not been clipped to the boundary and would require wetland-specific validation [9].

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

1. Intersect the RFO polygon and computed 15 km ring with annual forest-cover/loss data for 2015–2025 and alerts dated through 31 October 2026; validate disturbance classes using Sentinel-2/Landsat imagery and local monitoring [7, 8, 11].
2. Clip a biomass-carbon map to the same geometry; compare a historical benchmark such as the 2010 harmonized product with newer observations, and report forest area, pool definitions, resolution, uncertainty, and area-weighted totals [4, 5].
3. Add soil organic-carbon and wetland/peat information, with field sampling where product uncertainty or wetland extent is material [9].
4. Obtain geometries for the reserve’s management zones and analyze them separately; distinguish road-accessible/development areas from intact forest interiors.
5. Estimate emissions and removals using an IPCC-consistent land representation, activity data, locally appropriate emission factors, and uncertainty ranges. Include fire and non-CO₂ fluxes where material [10].

## Scientific sources and technical references

1. **Reserve boundary.** WDPA site 124389, RFO GeoJSON, `RFO_WDOECM_Nov2026_Public_124389_shp-polygons.json` (local repository source; boundary geometry and feature attributes).
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

**Citation and interpretation note.** Peer-reviewed regional studies and global products provide methods, historical context, or candidate inputs; none is represented here as an OWR measurement unless explicitly stated. All reserve-wide derived figures are calculated from the local RFO geometry. The screening scenarios are not a substitute for an IPCC-consistent inventory or project-level measurement, reporting, and verification.
