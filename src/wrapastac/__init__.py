"""wrapastac — a simple, professional wrapper around public STAC catalogues.

Typical usage::

    from wrapastac import Sentinel2, PlanetaryComputer
    from wrapastac.geometry import point_to_bbox

    geom = point_to_bbox(lat=51.5, lon=-0.1, buffer_m=5000)

    s2 = Sentinel2(provider="planetary_computer")
    items = s2.search(geometry=geom, start="2024-06-01", end="2024-08-31", cloud_cover=20)
    print(items)  # ItemCollection(14 items)
    print(items.dates)  # ['2024-06-03', '2024-06-08', ...]

    ds = s2.load(items, geometry=geom, bands=["red", "nir"])
"""

from wrapastac._base import STACCollection, StaticSTACCollection
from wrapastac._items import ItemCollection
from wrapastac.collections import (
    ESRILULC,
    RZLULC,
    CopDEM30,
    HLSLandsat,
    HLSSentinel,
    Landsat,
    LidarEngland,
    Sentinel1,
    Sentinel2,
)
from wrapastac.exceptions import EmptyItemCollectionError, UnknownProviderError
from wrapastac.providers import Element84, PlanetaryComputer, resolve_provider

__all__ = [
    # Base classes — for building custom collections
    "STACCollection",
    "StaticSTACCollection",
    # Built-in collections
    "Sentinel2",
    "Sentinel1",
    "Landsat",
    "HLSLandsat",
    "HLSSentinel",
    "CopDEM30",
    "ESRILULC",
    "RZLULC",
    "LidarEngland",
    # Providers
    "Element84",
    "PlanetaryComputer",
    "resolve_provider",
    # Core types
    "ItemCollection",
    # Exceptions
    "EmptyItemCollectionError",
    "UnknownProviderError",
]
