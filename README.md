# WrapASTAC

A Python SDK to wrap STAC satellite endpoints.

## Installation

```bash
pip install -e .
```

With [`uv`](https://docs.astral.sh/uv/):

```bash
uv sync
```

## Usage

Search for Sentinel-2 imagery over a location and load it as an `xarray.Dataset`:

```python
from wrapastac import Sentinel2
from wrapastac.geometry import point_to_bbox

# Define an area of interest (5 km buffer around a point)
geom = point_to_bbox(lat=51.5, lon=-0.1, buffer_m=5000)

# Search for scenes with less than 20% cloud cover
s2 = Sentinel2(provider="planetary_computer")
items = s2.search(geometry=geom, start="2024-06-01", end="2024-08-31", cloud_cover=20)
print(items)  # ItemCollection(14 items)
print(items.dates)  # ['2024-06-03', '2024-06-08', ...]

# Load selected bands as an xarray Dataset
ds = s2.load(items, geometry=geom, bands=["red", "green", "blue", "nir"])
```

Use `Element84` as an alternative provider:

```python
from wrapastac import Sentinel2, Element84

s2 = Sentinel2(provider=Element84())  # or simply use provider="element84"
items = s2.search(geometry=geom, start="2024-06-01", end="2024-08-31", cloud_cover=20)
```

Other available collections: `Sentinel1`, `Landsat`, `HLSSentinel`, `HLSLandsat`, `CopDEM30`, `ESRILULC`, `RZLULC`, `LidarEngland`.

## Adding a new satellite source

Subclass `STACCollection` for time-varying data (optical, SAR) or `StaticSTACCollection` for static data (DEMs, land cover). Define the five required class attributes and you're done:

```python
from typing import ClassVar
from wrapastac._base import STACCollection

class MyOptical(STACCollection):
    collection_id: ClassVar[str] = "my-collection-id"   # STAC collection name
    default_resolution: ClassVar[int] = 10               # metres
    default_dtype: ClassVar[str] = "uint16"
    default_nodata: ClassVar[int] = 0
    default_bands: ClassVar[list[str]] = ["red", "green", "blue", "nir"]

col = MyOptical(provider="element84")
items = col.search(geometry=geom, start="2024-01-01", end="2024-06-01")
ds = col.load(items, geometry=geom)
```

**Cloud cover filtering** — override `_build_query` to enable the `cloud_cover` parameter in `.search()`:

```python
def _build_query(self, cloud_cover: int | None) -> dict | None:
    if cloud_cover is None:
        return None
    return {"eo:cloud_cover": {"lt": cloud_cover}}
```

**Band name aliases** — if the STAC asset keys don't match `eo:common_name` values, add a `_fallback_band_mapping` to map friendly names to the actual asset keys:

```python
_fallback_band_mapping: ClassVar[dict[str, str]] = {"elevation": "data", "ndvi": "NDVI"}
```

**Static collections** (no time dimension — DEMs, LULC, etc.) — use `StaticSTACCollection` instead. Its `.search()` takes only a geometry:

```python
from wrapastac._base import StaticSTACCollection

class MyDEM(StaticSTACCollection):
    collection_id: ClassVar[str] = "my-dem"
    default_resolution: ClassVar[int] = 30
    default_dtype: ClassVar[str] = "float32"
    default_nodata: ClassVar[float] = -9999.0
    default_bands: ClassVar[list[str]] = ["elevation"]
    _fallback_band_mapping: ClassVar[dict[str, str]] = {"elevation": "data"}

items = MyDEM(provider="planetary_computer").search(geometry=geom)
```

Two optional flags control reprojection behaviour for static collections:

| Flag | Default | Effect |
| --- | --- | --- |
| `reproject_wgs84_to_utm` | `True` | Re-projects WGS84 assets to UTM for accurate metre-scale clipping |
| `use_native_resolution` | `False` | Ignores `default_resolution` and loads at the COG's native pixel size |

## Development

This project uses [`just`](https://github.com/casey/just) as a command runner. Run `just` to see all 
available commands:

```bash
just               # list available commands
just check         # run all checks (lint, typecheck, test)
just format        # Format code with ruff (applies fixes)
just format-check  # Run ruff formatter check (without fixes)
just install       # Install dependencies and prek hooks
just lint          # Run ruff linter
just prek          # Run all prek hooks
just prek-install  # Install prek git hooks
just test *args    # Run tests
just test-cov      # Run tests with coverage
just typecheck     # Run ty type checker
```

The project also uses [`prek`](https://prek.j178.dev/) for pre-commit hook management. These hooks 
automatically apply format and type checks on `git` commits only (not on the entire codebase). This 
ensures all committed code follows pre-defined standards, whilst the rest of the codebase can maintain
development flexibility. 

If you prefer to keep everything up to standard, use `just check` or the individual `just format` or 
`just lint` commands to run on the entire codebase.
