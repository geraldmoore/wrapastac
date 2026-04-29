# Graph Report - .  (2026-04-29)

## Corpus Check
- Corpus is ~6,744 words - fits in a single context window. You may not need a graph.

## Summary
- 283 nodes · 511 edges · 17 communities detected
- Extraction: 57% EXTRACTED · 43% INFERRED · 0% AMBIGUOUS · INFERRED: 220 edges (avg confidence: 0.65)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_HLS & Landsat Collections|HLS & Landsat Collections]]
- [[_COMMUNITY_Item Collection & Tests|Item Collection & Tests]]
- [[_COMMUNITY_Provider Abstractions|Provider Abstractions]]
- [[_COMMUNITY_Static Collections (DEMLULC)|Static Collections (DEM/LULC)]]
- [[_COMMUNITY_Geometry Utilities|Geometry Utilities]]
- [[_COMMUNITY_Base Class Tests|Base Class Tests]]
- [[_COMMUNITY_Core Base Classes|Core Base Classes]]
- [[_COMMUNITY_Collection Registry|Collection Registry]]
- [[_COMMUNITY_Test Fixtures|Test Fixtures]]
- [[_COMMUNITY_CRS & Projection|CRS & Projection]]
- [[_COMMUNITY_SDK Documentation|SDK Documentation]]
- [[_COMMUNITY_Provider Rationale|Provider Rationale]]
- [[_COMMUNITY_Provider Rationale|Provider Rationale]]
- [[_COMMUNITY_Provider Rationale|Provider Rationale]]
- [[_COMMUNITY_Provider Rationale|Provider Rationale]]
- [[_COMMUNITY_Planetary Computer Provider|Planetary Computer Provider]]
- [[_COMMUNITY_Landsat Query Builder|Landsat Query Builder]]

## God Nodes (most connected - your core abstractions)
1. `ItemCollection` - 55 edges
2. `STACCollection` - 25 edges
3. `Provider` - 25 edges
4. `make_item()` - 23 edges
5. `StaticSTACCollection` - 23 edges
6. `EmptyItemCollectionError` - 21 edges
7. `_TestCollection` - 15 edges
8. `UnknownProviderError` - 14 edges
9. `_CollectionBase` - 13 edges
10. `CopernicusDataSpaceEcosystem` - 10 edges

## Surprising Connections (you probably didn't know these)
- `CopernicusDataSpaceEcosystem` --conceptually_related_to--> `CQL2-JSON Filter`  [INFERRED]
  src/wrapastac/providers/copernicus_dataspace.py → README.md
- `test_esrilulc_planetary_computer()` --calls--> `ESRILULC`  [INFERRED]
  tests/test_collections.py → src/wrapastac/collections/lulc.py
- `_query_to_cql2` --conceptually_related_to--> `CQL2-JSON Filter`  [INFERRED]
  src/wrapastac/_base.py → README.md
- `Provider` --conceptually_related_to--> `Provider Pattern`  [INFERRED]
  src/wrapastac/providers/_base.py → README.md
- `_collection()` --calls--> `ItemCollection`  [INFERRED]
  tests/test_items.py → src/wrapastac/_items.py

## Hyperedges (group relationships)
- **Geometry UTM Projection Flow** — point_to_bbox_func, get_utm_epsg_func, geometry_from_epsg_to_epsg_func [EXTRACTED 0.95]
- **StaticSTACCollection subclasses: ESRILULC, RZLULC, LidarEngland** — esrilulc_class, rzlulc_class, lidarengland_class, staticstaccollection_base [EXTRACTED 1.00]
- **HLS cross-calibrated Landsat+Sentinel-2 MGRS harmonisation** — hlslandsat_class, hlssentinel_class, hls_harmonised_grid_concept [EXTRACTED 1.00]
- **STAC Provider Implementations** — providers__base_provider, element84_element84, copernicus_dataspace_copernicusdataspaceecosystem [EXTRACTED 0.95]
- **Collection Class Hierarchy** — _base_collectionbase, _base_staccollection, _base_staticstaccollection, sentinel2_sentinel2 [EXTRACTED 0.95]

## Communities

### Community 0 - "HLS & Landsat Collections"
Cohesion: 0.06
Nodes (32): HLSLandsat, HLSSentinel, NASA Harmonized Landsat Sentinel-2 (HLS) — Sentinel-2 component.      Supported, NASA Harmonized Landsat Sentinel-2 (HLS) — Landsat component.      Supported pro, Landsat, Landsat Collection 2 Level-2 surface reflectance and surface temperature.      S, Sentinel-1 RTC (Radiometric Terrain Corrected) SAR backscatter.      Supported p, Sentinel1 (+24 more)

### Community 1 - "Item Collection & Tests"
Cohesion: 0.08
Nodes (32): _make_asset(), make_item(), Shared fixtures for wrapastac tests., Build a minimal pystac.Item for unit testing.      Args:         item_id: STAC i, A Sentinel-2 MPC-style item where asset keys are native band names (B04, B08)., A Sentinel-2 E84-style item where asset keys are common names., A Sentinel-1 RTC item with no eo:bands common names., s1_item() (+24 more)

### Community 2 - "Provider Abstractions"
Cohesion: 0.07
Nodes (19): ABC, Provider, Provider, Abstract base class representing a STAC API provider.      A Provider knows two, CopernicusDataSpaceEcosystem, modifier(), Copernicus Data Space Ecosystem STAC API (https://stac.dataspace.copernicus.eu)., Fetch or return cached OAuth2 token. (+11 more)

### Community 3 - "Static Collections (DEM/LULC)"
Cohesion: 0.09
Nodes (31): CopDEM30, Copernicus Digital Elevation Model at 30 m resolution (GLO-30).      Supported p, LidarEngland, 5 m LiDAR Digital Terrain Model for England.      This collection requires a cus, ESRILULC, Riparian Zone Land Use / Land Cover (io-lulc-riparian-zones).      Supported pro, ESRI 10 m Annual Land Use / Land Cover (2017–2023).      Supported providers: "p, RZLULC (+23 more)

### Community 4 - "Geometry Utilities"
Cohesion: 0.09
Nodes (29): bbox(), from_geodataframe(), point_to_bbox(), point_to_circle(), Geometry utility functions for constructing search and clip geometries.  All fun, Construct a rectangular bounding box geometry from WGS84 coordinates.      Args:, Create a square bounding box around a lat/lon point.      The point is projected, Create a circular polygon around a lat/lon point.      The point is projected to (+21 more)

### Community 5 - "Base Class Tests"
Cohesion: 0.16
Nodes (16): test_get_epsg_defaults_to_wgs84_when_missing(), test_get_epsg_from_proj_epsg(), test_get_epsg_most_common(), test_load_raises_on_empty_items(), test_provider_instance_passed_directly(), test_provider_string_element84(), test_provider_string_planetary_computer(), test_resolve_bands_e84_style() (+8 more)

### Community 6 - "Core Base Classes"
Cohesion: 0.19
Nodes (13): _CollectionBase, _query_to_cql2, STACCollection, StaticSTACCollection, ItemCollection, CopernicusDataSpaceEcosystem, Element84, get_cdse_provider (+5 more)

### Community 7 - "Collection Registry"
Cohesion: 0.38
Nodes (11): collections __init__ (public API surface), ESRILULC, _fallback_band_mapping pattern (common_name -> asset_key), HLS MGRS tiling grid harmonisation concept, HLSLandsat, HLSSentinel, Landsat, LidarEngland (+3 more)

### Community 8 - "Test Fixtures"
Cohesion: 0.31
Nodes (6): make_item() fixture helper, CopDEM30, EmptyItemCollectionError, Sentinel1, UnknownProviderError, wrapastac package __init__

### Community 9 - "CRS & Projection"
Cohesion: 0.48
Nodes (5): geometry_from_epsg_to_epsg(), get_utm_epsg(), point_to_bbox(), point_to_circle(), WGS84_EPSG constant

### Community 10 - "SDK Documentation"
Cohesion: 1.0
Nodes (2): STAC Satellite Endpoint, WrapASTAC SDK

### Community 12 - "Provider Rationale"
Cohesion: 1.0
Nodes (1): The root URL of the STAC API.

### Community 13 - "Provider Rationale"
Cohesion: 1.0
Nodes (1): Optional callable passed to pystac_client.Client.open() to sign/modify requests.

### Community 14 - "Provider Rationale"
Cohesion: 1.0
Nodes (1): Optional HTTP headers to include with every request.

### Community 15 - "Provider Rationale"
Cohesion: 1.0
Nodes (1): Whether this provider prefers CQL2-JSON for STAC query filters.          When Tr

### Community 19 - "Planetary Computer Provider"
Cohesion: 1.0
Nodes (1): PlanetaryComputer Provider

### Community 21 - "Landsat Query Builder"
Cohesion: 1.0
Nodes (1): Landsat._build_query

## Knowledge Gaps
- **39 isolated node(s):** `Shared fixtures for wrapastac tests.`, `Build a minimal pystac.Item for unit testing.      Args:         item_id: STAC i`, `A Sentinel-2 MPC-style item where asset keys are native band names (B04, B08).`, `A Sentinel-2 E84-style item where asset keys are common names.`, `A Sentinel-1 RTC item with no eo:bands common names.` (+34 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `SDK Documentation`** (2 nodes): `STAC Satellite Endpoint`, `WrapASTAC SDK`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Provider Rationale`** (1 nodes): `The root URL of the STAC API.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Provider Rationale`** (1 nodes): `Optional callable passed to pystac_client.Client.open() to sign/modify requests.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Provider Rationale`** (1 nodes): `Optional HTTP headers to include with every request.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Provider Rationale`** (1 nodes): `Whether this provider prefers CQL2-JSON for STAC query filters.          When Tr`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Planetary Computer Provider`** (1 nodes): `PlanetaryComputer Provider`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Landsat Query Builder`** (1 nodes): `Landsat._build_query`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ItemCollection` connect `Item Collection & Tests` to `HLS & Landsat Collections`, `Static Collections (DEM/LULC)`, `Base Class Tests`?**
  _High betweenness centrality (0.231) - this node is a cross-community bridge._
- **Why does `Provider` connect `Provider Abstractions` to `HLS & Landsat Collections`, `Static Collections (DEM/LULC)`, `Base Class Tests`?**
  _High betweenness centrality (0.171) - this node is a cross-community bridge._
- **Why does `STACCollection` connect `HLS & Landsat Collections` to `Item Collection & Tests`, `Provider Abstractions`, `Static Collections (DEM/LULC)`, `Base Class Tests`?**
  _High betweenness centrality (0.149) - this node is a cross-community bridge._
- **Are the 43 inferred relationships involving `ItemCollection` (e.g. with `Tests for ItemCollection wrapper.` and `_TestCollection`) actually correct?**
  _`ItemCollection` has 43 INFERRED edges - model-reasoned connections that need verification._
- **Are the 21 inferred relationships involving `STACCollection` (e.g. with `Tests for built-in collection classes.` and `_TestCollection`) actually correct?**
  _`STACCollection` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 21 inferred relationships involving `Provider` (e.g. with `Tests for built-in collection classes.` and `_CollectionBase`) actually correct?**
  _`Provider` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `make_item()` (e.g. with `test_len()` and `test_iter()`) actually correct?**
  _`make_item()` has 17 INFERRED edges - model-reasoned connections that need verification._