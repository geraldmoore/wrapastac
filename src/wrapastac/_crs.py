from __future__ import annotations

from functools import lru_cache

import pyproj
from shapely.geometry.base import BaseGeometry
from shapely.ops import transform

WGS84_EPSG = 4326
_WGS84_PROJ4 = "+proj=longlat +datum=WGS84 +no_defs +type=crs"


@lru_cache(maxsize=16)
def _get_transformer(in_epsg: int, out_epsg: int) -> pyproj.Transformer:
    crs_from = pyproj.CRS(in_epsg) if in_epsg != WGS84_EPSG else _WGS84_PROJ4
    crs_to = pyproj.CRS(out_epsg) if out_epsg != WGS84_EPSG else _WGS84_PROJ4
    return pyproj.Transformer.from_crs(crs_from, crs_to)


def geometry_from_epsg_to_epsg(geometry: BaseGeometry, in_epsg: int, out_epsg: int) -> BaseGeometry:
    """Reproject a Shapely geometry from one EPSG to another."""
    if in_epsg == out_epsg:
        return geometry
    transformer = _get_transformer(in_epsg, out_epsg)
    return transform(lambda x, y, z=None: transformer.transform(x, y, errcheck=True), geometry)


def get_utm_epsg(lon: float, lat: float) -> int:
    """Return the UTM EPSG code for a given longitude/latitude, including Norwegian special zones."""
    zone = int((lon + 180) / 6) + 1

    # Special zones for Norway (zone 32) and Svalbard
    if 56.0 <= lat < 64.0 and 3.0 <= lon < 12.0:
        zone = 32
    elif 72.0 <= lat <= 84.0:
        if lon < 9.0:
            zone = 31
        elif lon < 21.0:
            zone = 33
        elif lon < 33.0:
            zone = 35
        elif lon < 42.0:
            zone = 37

    base = 32600 if lat >= 0 else 32700
    return base + zone
