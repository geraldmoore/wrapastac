"""Geometry utility functions for constructing search and clip geometries.

All functions return Shapely geometries in WGS84 (EPSG:4326), ready to pass
directly to STACCollection.search() and STACCollection.load().
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from shapely import BufferCapStyle
from shapely.geometry import Point, box
from shapely.geometry.base import BaseGeometry

from wrapastac._crs import WGS84_EPSG, geometry_from_epsg_to_epsg, get_utm_epsg

if TYPE_CHECKING:
    import geopandas as gpd


def point_to_bbox(lat: float, lon: float, buffer_m: float) -> BaseGeometry:
    """Create a square bounding box around a lat/lon point.

    The point is projected to its local UTM zone, buffered by ``buffer_m`` metres
    on each side, then returned in WGS84 (EPSG:4326).

    Args:
        lat: Latitude in decimal degrees.
        lon: Longitude in decimal degrees.
        buffer_m: Half-side length of the bounding box in metres.

    Returns:
        Shapely Polygon in WGS84.

    Example:
        >>> geom = point_to_bbox(lat=51.5, lon=-0.1, buffer_m=1000)
        >>> items = Sentinel2(provider="element84").search(geometry=geom, ...)
    """
    utm_epsg = get_utm_epsg(lon=lon, lat=lat)
    point_wgs84 = Point(lon, lat)
    point_utm = geometry_from_epsg_to_epsg(point_wgs84, WGS84_EPSG, utm_epsg)
    bbox_utm = point_utm.buffer(buffer_m, cap_style=BufferCapStyle.square)
    return geometry_from_epsg_to_epsg(bbox_utm, utm_epsg, WGS84_EPSG)


def point_to_circle(lat: float, lon: float, radius_m: float) -> BaseGeometry:
    """Create a circular polygon around a lat/lon point.

    The point is projected to its local UTM zone, buffered by ``radius_m`` metres
    using a circular cap, then returned in WGS84 (EPSG:4326).

    Args:
        lat: Latitude in decimal degrees.
        lon: Longitude in decimal degrees.
        radius_m: Radius of the circle in metres.

    Returns:
        Shapely Polygon in WGS84.
    """
    utm_epsg = get_utm_epsg(lon=lon, lat=lat)
    point_wgs84 = Point(lon, lat)
    point_utm = geometry_from_epsg_to_epsg(point_wgs84, WGS84_EPSG, utm_epsg)
    circle_utm = point_utm.buffer(radius_m)  # default cap_style=1 → round
    return geometry_from_epsg_to_epsg(circle_utm, utm_epsg, WGS84_EPSG)


def from_geodataframe(gdf: gpd.GeoDataFrame) -> BaseGeometry:
    """Return the union of all geometries in a GeoDataFrame as a single WGS84 geometry.

    Reprojects to WGS84 automatically if the GeoDataFrame has a different CRS.

    Args:
        gdf: A GeoDataFrame with at least one geometry.

    Returns:
        Shapely geometry in WGS84 representing the union of all features.

    Raises:
        ValueError: If the GeoDataFrame is empty.
    """
    if gdf.empty:
        raise ValueError("GeoDataFrame is empty — cannot construct a geometry.")

    gdf_wgs84 = (
        gdf.to_crs("EPSG:4326") if gdf.crs is not None and gdf.crs.to_epsg() != WGS84_EPSG else gdf
    )
    return gdf_wgs84.geometry.union_all()


def bbox(
    min_lon: float,
    min_lat: float,
    max_lon: float,
    max_lat: float,
) -> BaseGeometry:
    """Construct a rectangular bounding box geometry from WGS84 coordinates.

    Args:
        min_lon: Western boundary longitude.
        min_lat: Southern boundary latitude.
        max_lon: Eastern boundary longitude.
        max_lat: Northern boundary latitude.

    Returns:
        Shapely Polygon in WGS84.
    """
    return box(min_lon, min_lat, max_lon, max_lat)


__all__ = ["point_to_bbox", "point_to_circle", "from_geodataframe", "bbox"]
