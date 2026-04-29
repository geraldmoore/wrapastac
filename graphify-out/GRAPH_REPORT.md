# Graph Report - .  (2026-04-29)

## Corpus Check
- Corpus is ~5,348 words - fits in a single context window. You may not need a graph.

## Summary
- 271 nodes · 509 edges · 15 communities detected
- Extraction: 60% EXTRACTED · 40% INFERRED · 0% AMBIGUOUS · INFERRED: 204 edges (avg confidence: 0.66)
- Token cost: 3,200 input · 1,800 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Test Fixtures & Items|Test Fixtures & Items]]
- [[_COMMUNITY_Core Base & Providers|Core Base & Providers]]
- [[_COMMUNITY_Optical Satellite Collections|Optical Satellite Collections]]
- [[_COMMUNITY_Geometry Utilities|Geometry Utilities]]
- [[_COMMUNITY_Provider Interface (ABC)|Provider Interface (ABC)]]
- [[_COMMUNITY_Collection & Item Core|Collection & Item Core]]
- [[_COMMUNITY_Static Collections|Static Collections]]
- [[_COMMUNITY_Element84 Provider|Element84 Provider]]
- [[_COMMUNITY_Collections Public API|Collections Public API]]
- [[_COMMUNITY_CRS & Load Pipeline|CRS & Load Pipeline]]
- [[_COMMUNITY_Dev Tooling & Docs|Dev Tooling & Docs]]
- [[_COMMUNITY_Cloud Filter Queries|Cloud Filter Queries]]
- [[_COMMUNITY_API URL Descriptor|API URL Descriptor]]
- [[_COMMUNITY_Request Modifier Descriptor|Request Modifier Descriptor]]
- [[_COMMUNITY_HTTP Headers Descriptor|HTTP Headers Descriptor]]

## God Nodes (most connected - your core abstractions)
1. `ItemCollection` - 52 edges
2. `STACCollection` - 25 edges
3. `make_item()` - 23 edges
4. `StaticSTACCollection` - 23 edges
5. `EmptyItemCollectionError` - 19 edges
6. `Provider` - 19 edges
7. `_TestCollection` - 15 edges
8. `_CollectionBase` - 13 edges
9. `UnknownProviderError` - 13 edges
10. `Sentinel2` - 10 edges

## Surprising Connections (you probably didn't know these)
- `_collection()` --calls--> `ItemCollection`  [INFERRED]
  tests/test_items.py → src/wrapastac/_items.py
- `Tests for ItemCollection wrapper.` --uses--> `EmptyItemCollectionError`  [INFERRED]
  tests/test_items.py → src/wrapastac/exceptions.py
- `test_sentinel2_element84()` --calls--> `Sentinel2`  [INFERRED]
  tests/test_collections.py → src/wrapastac/collections/sentinel2.py
- `test_sentinel2_planetary_computer()` --calls--> `Sentinel2`  [INFERRED]
  tests/test_collections.py → src/wrapastac/collections/sentinel2.py
- `test_sentinel1_planetary_computer()` --calls--> `Sentinel1`  [INFERRED]
  tests/test_collections.py → src/wrapastac/collections/sentinel1.py

## Hyperedges (group relationships)
- **STAC Search-to-Load Pipeline** — staccollection_class, search_method_stac, itemcollection_class, load_method [EXTRACTED 0.95]
- **Geometry UTM Projection Flow** — point_to_bbox_func, get_utm_epsg_func, geometry_from_epsg_to_epsg_func [EXTRACTED 0.95]
- **Provider Resolution Pattern** — provider_abc, element84_provider, planetarycomputer_provider, resolve_provider_func [EXTRACTED 0.95]
- **StaticSTACCollection subclasses: ESRILULC, RZLULC, LidarEngland** — esrilulc_class, rzlulc_class, lidarengland_class, staticstaccollection_base [EXTRACTED 1.00]
- **HLS cross-calibrated Landsat+Sentinel-2 MGRS harmonisation** — hlslandsat_class, hlssentinel_class, hls_harmonised_grid_concept [EXTRACTED 1.00]
- **Collections implementing eo:cloud_cover query filter** — sentinel2_class, landsat_class, cloud_cover_filter_pattern [EXTRACTED 1.00]

## Communities

### Community 0 - "Test Fixtures & Items"
Cohesion: 0.1
Nodes (29): _make_asset(), make_item(), Shared fixtures for wrapastac tests., Build a minimal pystac.Item for unit testing.      Args:         item_id: STAC i, A Sentinel-2 MPC-style item where asset keys are native band names (B04, B08)., A Sentinel-2 E84-style item where asset keys are common names., A Sentinel-1 RTC item with no eo:bands common names., s1_item() (+21 more)

### Community 1 - "Core Base & Providers"
Cohesion: 0.08
Nodes (32): from_geodataframe(), Return the union of all geometries in a GeoDataFrame as a single WGS84 geometry., Resolve a provider name string or Provider instance to a Provider object.      A, resolve_provider(), Tests for STACCollection and StaticSTACCollection base classes., E84-style items already use common names as asset keys — no rename needed., Unknown band name falls back to itself (pass-through to odc-stac)., MPC-style items have native asset keys (B04) mapped via eo:bands common_name. (+24 more)

### Community 2 - "Optical Satellite Collections"
Cohesion: 0.08
Nodes (27): HLSLandsat, HLSSentinel, NASA Harmonized Landsat Sentinel-2 (HLS) — Sentinel-2 component.      Supported, NASA Harmonized Landsat Sentinel-2 (HLS) — Landsat component.      Supported pro, Landsat, Landsat Collection 2 Level-2 surface reflectance and surface temperature.      S, Sentinel-1 RTC (Radiometric Terrain Corrected) SAR backscatter.      Supported p, Sentinel1 (+19 more)

### Community 3 - "Geometry Utilities"
Cohesion: 0.1
Nodes (27): bbox(), point_to_bbox(), point_to_circle(), Geometry utility functions for constructing search and clip geometries.  All fun, Construct a rectangular bounding box geometry from WGS84 coordinates.      Args:, Create a square bounding box around a lat/lon point.      The point is projected, Create a circular polygon around a lat/lon point.      The point is projected to, Tests for geometry utility functions. (+19 more)

### Community 4 - "Provider Interface (ABC)"
Cohesion: 0.14
Nodes (9): ABC, Provider, Abstract base class representing a STAC API provider.      A Provider knows two, _CollectionBase, Load STAC items into a clipped, band-renamed xarray Dataset.          Args:, Search the STAC catalogue for items intersecting a geometry and date range., Search the STAC catalogue for items intersecting a geometry.          Args:, Shared internals for STACCollection and StaticSTACCollection. (+1 more)

### Community 5 - "Collection & Item Core"
Cohesion: 0.16
Nodes (16): ItemCollection._assert_non_empty(), _CollectionBase, make_item() fixture helper, CopDEM30, Element84 Provider, EmptyItemCollectionError, ItemCollection, PlanetaryComputer Provider (+8 more)

### Community 6 - "Static Collections"
Cohesion: 0.16
Nodes (16): CopDEM30, Copernicus Digital Elevation Model at 30 m resolution (GLO-30).      Supported p, LidarEngland, 5 m LiDAR Digital Terrain Model for England.      This collection requires a cus, ESRILULC, Riparian Zone Land Use / Land Cover (io-lulc-riparian-zones).      Supported pro, ESRI 10 m Annual Land Use / Land Cover (2017–2023).      Supported providers: "p, RZLULC (+8 more)

### Community 7 - "Element84 Provider"
Cohesion: 0.14
Nodes (7): Provider, Element84, Element84 Earth Search STAC API (https://earth-search.aws.element84.com/v1)., PlanetaryComputer, Microsoft Planetary Computer STAC API.      Assets are access-controlled. Items, Tests for the top-level wrapastac package imports., test_providers_subpackage_imports()

### Community 8 - "Collections Public API"
Cohesion: 0.34
Nodes (14): collections __init__ (public API surface), ESRILULC, _fallback_band_mapping pattern (common_name -> asset_key), HLS MGRS tiling grid harmonisation concept, HLSLandsat, HLSSentinel, Landsat, LidarEngland (+6 more)

### Community 9 - "CRS & Load Pipeline"
Cohesion: 0.26
Nodes (9): geometry_from_epsg_to_epsg(), _CollectionBase._get_epsg(), get_utm_epsg(), _CollectionBase.load(), maybe_harmonise_s2(), point_to_bbox(), point_to_circle(), Sentinel2._maybe_harmonise (+1 more)

### Community 10 - "Dev Tooling & Docs"
Cohesion: 0.6
Nodes (5): just command runner, prek pre-commit hook manager, WrapASTAC README, uv package manager, WrapASTAC — Python SDK to wrap STAC satellite endpoints

### Community 11 - "Cloud Filter Queries"
Cohesion: 1.0
Nodes (3): eo:cloud_cover STAC query filter pattern, Landsat._build_query, Sentinel2._build_query

### Community 13 - "API URL Descriptor"
Cohesion: 1.0
Nodes (1): The root URL of the STAC API.

### Community 14 - "Request Modifier Descriptor"
Cohesion: 1.0
Nodes (1): Optional callable passed to pystac_client.Client.open() to sign/modify requests.

### Community 15 - "HTTP Headers Descriptor"
Cohesion: 1.0
Nodes (1): Optional HTTP headers to include with every request.

## Knowledge Gaps
- **30 isolated node(s):** `Shared fixtures for wrapastac tests.`, `Build a minimal pystac.Item for unit testing.      Args:         item_id: STAC i`, `A Sentinel-2 MPC-style item where asset keys are native band names (B04, B08).`, `A Sentinel-2 E84-style item where asset keys are common names.`, `A Sentinel-1 RTC item with no eo:bands common names.` (+25 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `API URL Descriptor`** (1 nodes): `The root URL of the STAC API.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Request Modifier Descriptor`** (1 nodes): `Optional callable passed to pystac_client.Client.open() to sign/modify requests.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `HTTP Headers Descriptor`** (1 nodes): `Optional HTTP headers to include with every request.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ItemCollection` connect `Test Fixtures & Items` to `Core Base & Providers`, `Optical Satellite Collections`, `Provider Interface (ABC)`, `Static Collections`?**
  _High betweenness centrality (0.207) - this node is a cross-community bridge._
- **Why does `STACCollection` connect `Optical Satellite Collections` to `Test Fixtures & Items`, `Core Base & Providers`, `Provider Interface (ABC)`, `Static Collections`?**
  _High betweenness centrality (0.142) - this node is a cross-community bridge._
- **Why does `Provider` connect `Provider Interface (ABC)` to `Core Base & Providers`, `Optical Satellite Collections`, `Static Collections`, `Element84 Provider`?**
  _High betweenness centrality (0.112) - this node is a cross-community bridge._
- **Are the 42 inferred relationships involving `ItemCollection` (e.g. with `Tests for ItemCollection wrapper.` and `_TestCollection`) actually correct?**
  _`ItemCollection` has 42 INFERRED edges - model-reasoned connections that need verification._
- **Are the 21 inferred relationships involving `STACCollection` (e.g. with `Tests for built-in collection classes.` and `_TestCollection`) actually correct?**
  _`STACCollection` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `make_item()` (e.g. with `test_len()` and `test_iter()`) actually correct?**
  _`make_item()` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `StaticSTACCollection` (e.g. with `Tests for built-in collection classes.` and `_TestCollection`) actually correct?**
  _`StaticSTACCollection` has 19 INFERRED edges - model-reasoned connections that need verification._