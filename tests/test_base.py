import pytest

from tests.conftest import make_item
from wrapastac._base import STACCollection, StaticSTACCollection
from wrapastac._items import ItemCollection
from wrapastac.exceptions import UnknownProviderError
from wrapastac.providers import Element84, PlanetaryComputer


class _TestCollection(STACCollection):
    collection_id = "test-collection"
    default_resolution = 10
    default_dtype = "uint16"
    default_nodata = 0
    default_bands = ["red", "nir"]


class _TestStaticCollection(StaticSTACCollection):
    collection_id = "test-static"
    default_resolution = 30
    default_dtype = "float32"
    default_nodata = -9999.0
    default_bands = ["data"]


def test_provider_string_element84():
    col = _TestCollection(provider="element84")
    assert isinstance(col._provider, Element84)


def test_provider_string_planetary_computer():
    col = _TestCollection(provider="planetary_computer")
    assert isinstance(col._provider, PlanetaryComputer)


def test_provider_instance_passed_directly():
    provider = Element84()
    col = _TestCollection(provider=provider)
    assert col._provider is provider


def test_unknown_provider_string_raises():
    with pytest.raises(UnknownProviderError, match="Unknown provider"):
        _TestCollection(provider="nonexistent_provider")


def test_get_epsg_from_proj_epsg():
    item = make_item(epsg=32632)
    epsg = _TestCollection._get_epsg([item])
    assert epsg == 32632


def test_get_epsg_most_common():
    items = [
        make_item(item_id="a", epsg=32632),
        make_item(item_id="b", epsg=32632),
        make_item(item_id="c", epsg=32633),
    ]
    epsg = _TestCollection._get_epsg(items)
    assert epsg == 32632


def test_get_epsg_defaults_to_wgs84_when_missing():
    from wrapastac._crs import WGS84_EPSG

    item = make_item()
    item.properties.pop("proj:epsg", None)
    epsg = _TestCollection._get_epsg([item])
    assert epsg == WGS84_EPSG


def test_load_raises_on_empty_items():
    from wrapastac.exceptions import EmptyItemCollectionError

    col = _TestCollection(provider="element84")
    with pytest.raises(EmptyItemCollectionError):
        col.load(ItemCollection([]))
