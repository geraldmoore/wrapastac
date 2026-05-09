from shapely.geometry import Point

from wrapastac._crs import get_utm_epsg
from wrapastac.geometry import bbox, point_to_bbox, point_to_circle


def test_point_to_bbox_returns_polygon():
    geom = point_to_bbox(lat=51.5, lon=-0.1, buffer_m=1000)
    assert geom.geom_type == "Polygon"


def test_point_to_bbox_contains_origin():
    geom = point_to_bbox(lat=51.5, lon=-0.1, buffer_m=1000)
    origin = Point(-0.1, 51.5)
    assert geom.contains(origin)


def test_point_to_bbox_approximate_size():
    geom = point_to_bbox(lat=51.5, lon=-0.1, buffer_m=1000)
    bounds = geom.bounds  # (min_lon, min_lat, max_lon, max_lat)
    lat_span_deg = bounds[3] - bounds[1]
    lon_span_deg = bounds[2] - bounds[0]
    # 2 km at 51.5°N latitude ≈ 0.018° lat, ≈ 0.029° lon
    assert 0.01 < lat_span_deg < 0.03
    assert 0.01 < lon_span_deg < 0.05


def test_point_to_circle_returns_polygon():
    geom = point_to_circle(lat=48.8, lon=2.3, radius_m=500)
    assert geom.geom_type == "Polygon"


def test_point_to_circle_contains_origin():
    geom = point_to_circle(lat=48.8, lon=2.3, radius_m=500)
    origin = Point(2.3, 48.8)
    assert geom.contains(origin)


def test_bbox_helper():
    geom = bbox(-1.0, 50.0, 1.0, 52.0)
    assert geom.geom_type == "Polygon"
    assert geom.bounds == (-1.0, 50.0, 1.0, 52.0)


def test_point_to_bbox_southern_hemisphere():
    geom = point_to_bbox(lat=-33.8, lon=151.2, buffer_m=2000)
    assert geom.contains(Point(151.2, -33.8))


def test_get_utm_epsg_northern():
    epsg = get_utm_epsg(lon=10.0, lat=55.0)
    assert epsg == 32632  # UTM zone 32N


def test_get_utm_epsg_southern():
    epsg = get_utm_epsg(lon=151.2, lat=-33.8)
    assert epsg == 32756  # UTM zone 56S


def test_get_utm_epsg_norway_special_zone():
    # Longitude 5°E, latitude 58°N falls in the Norwegian special zone 32
    epsg = get_utm_epsg(lon=5.0, lat=58.0)
    assert epsg == 32632
