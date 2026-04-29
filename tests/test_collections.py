"""Tests for built-in collection classes."""

from __future__ import annotations

from wrapastac._base import STACCollection, StaticSTACCollection
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
from wrapastac.providers import Element84, PlanetaryComputer

# ---------------------------------------------------------------------------
# Instantiation
# ---------------------------------------------------------------------------


def test_sentinel2_element84():
    s2 = Sentinel2(provider="element84")
    assert isinstance(s2._provider, Element84)
    assert s2.collection_id == "sentinel-2-l2a"


def test_sentinel2_planetary_computer():
    s2 = Sentinel2(provider="planetary_computer")
    assert isinstance(s2._provider, PlanetaryComputer)


def test_sentinel1_planetary_computer():
    s1 = Sentinel1(provider="planetary_computer")
    assert s1.collection_id == "sentinel-1-rtc"
    assert s1.default_dtype == "float32"


def test_landsat_planetary_computer():
    ls = Landsat(provider="planetary_computer")
    assert ls.collection_id == "landsat-c2-l2"
    assert ls.default_resolution == 30


def test_hls_landsat():
    hls = HLSLandsat(provider="planetary_computer")
    assert hls.collection_id == "hls2-l30"
    assert hls.default_dtype == "int16"


def test_hls_sentinel():
    hls = HLSSentinel(provider="planetary_computer")
    assert hls.collection_id == "hls2-s30"


def test_copdem30_planetary_computer():
    dem = CopDEM30(provider="planetary_computer")
    assert dem.collection_id == "cop-dem-glo-30"
    assert dem.reproject_wgs84_to_utm is False
    assert dem.use_native_resolution is True


def test_esrilulc_planetary_computer():
    lulc = ESRILULC(provider="planetary_computer")
    assert lulc.collection_id == "io-lulc-annual-v02"


def test_rzlulc_planetary_computer():
    lulc = RZLULC(provider="planetary_computer")
    assert lulc._fallback_band_mapping == {"data": "rz_lulc"}


# ---------------------------------------------------------------------------
# Inheritance
# ---------------------------------------------------------------------------


def test_optical_collections_are_stac_collections():
    for cls in (Sentinel2, Sentinel1, Landsat, HLSLandsat, HLSSentinel):
        assert issubclass(cls, STACCollection)


def test_static_collections_are_static_stac_collections():
    for cls in (CopDEM30, ESRILULC, RZLULC, LidarEngland):
        assert issubclass(cls, StaticSTACCollection)


# ---------------------------------------------------------------------------
# Cloud cover query
# ---------------------------------------------------------------------------


def test_sentinel2_builds_cloud_query():
    s2 = Sentinel2(provider="element84")
    query = s2._build_query(cloud_cover=20)
    assert query == {"eo:cloud_cover": {"lt": 20}}


def test_sentinel2_no_cloud_query_when_none():
    s2 = Sentinel2(provider="element84")
    assert s2._build_query(cloud_cover=None) is None


def test_sentinel1_no_cloud_query():
    s1 = Sentinel1(provider="planetary_computer")
    assert s1._build_query(cloud_cover=20) is None


# ---------------------------------------------------------------------------
# Custom collection via subclassing
# ---------------------------------------------------------------------------


def test_custom_stac_collection():
    class MyCollection(STACCollection):
        collection_id = "my-custom-collection"
        default_resolution = 20
        default_dtype = "float32"
        default_nodata = -1.0
        default_bands = ["band1", "band2"]

    col = MyCollection(provider="element84")
    assert col.collection_id == "my-custom-collection"
    assert col.default_resolution == 20


def test_custom_static_collection():
    class MyStaticCollection(StaticSTACCollection):
        collection_id = "my-static"
        default_resolution = 10
        default_dtype = "uint8"
        default_nodata = 255
        default_bands = ["class"]
        _fallback_band_mapping = {"class": "classification"}

    col = MyStaticCollection(provider="element84")
    assert col._fallback_band_mapping == {"class": "classification"}


def test_custom_provider():
    from wrapastac.providers._base import Provider

    class MyProvider(Provider):
        @property
        def api_url(self) -> str:
            return "https://my.custom.stac.api/v1"

    lidar = LidarEngland(provider=MyProvider())
    assert lidar._provider.api_url == "https://my.custom.stac.api/v1"
