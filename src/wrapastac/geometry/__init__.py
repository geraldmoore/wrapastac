from shapely import BufferCapStyle
from shapely.geometry import Point, box
from shapely.geometry.base import BaseGeometry

from wrapastac._crs import WGS84_EPSG, geometry_from_epsg_to_epsg, get_utm_epsg


def point_to_bbox(lat: float, lon: float, buffer_m: float) -> BaseGeometry:
    """Buffer point to a square bounding box around a point, in UTM and returned in WGS84."""
    utm_epsg = get_utm_epsg(lon=lon, lat=lat)
    point_wgs84 = Point(lon, lat)
    point_utm = geometry_from_epsg_to_epsg(point_wgs84, WGS84_EPSG, utm_epsg)
    bbox_utm = point_utm.buffer(buffer_m, cap_style=BufferCapStyle.square)
    return geometry_from_epsg_to_epsg(bbox_utm, utm_epsg, WGS84_EPSG)


def point_to_circle(lat: float, lon: float, radius_m: float) -> BaseGeometry:
    """Buffer a point to a circular polygon, in UTM and returned in WGS84."""
    utm_epsg = get_utm_epsg(lon=lon, lat=lat)
    point_wgs84 = Point(lon, lat)
    point_utm = geometry_from_epsg_to_epsg(point_wgs84, WGS84_EPSG, utm_epsg)
    circle_utm = point_utm.buffer(radius_m)
    return geometry_from_epsg_to_epsg(circle_utm, utm_epsg, WGS84_EPSG)


def bbox(
    min_lon: float,
    min_lat: float,
    max_lon: float,
    max_lat: float,
) -> BaseGeometry:
    return box(min_lon, min_lat, max_lon, max_lat)


__all__ = ["point_to_bbox", "point_to_circle", "bbox"]
