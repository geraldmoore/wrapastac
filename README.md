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

s2 = Sentinel2(provider=Element84())  # or provider="element84"
items = s2.search(geometry=geom, start="2024-06-01", end="2024-08-31", cloud_cover=20)
```

Other available collections: `Sentinel1`, `Landsat`, `HLSSentinel`, `HLSLandsat`, `CopDEM30`, `ESRILULC`, `RZLULC`, `LidarEngland`.

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
