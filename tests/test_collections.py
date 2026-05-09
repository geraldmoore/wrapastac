from wrapastac._base import STACCollection
from wrapastac.collections import Sentinel1, Sentinel2


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
