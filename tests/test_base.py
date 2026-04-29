"""Tests for STACCollection and StaticSTACCollection base classes."""

from __future__ import annotations

import pytest

from tests.conftest import make_item
from wrapastac._base import STACCollection, StaticSTACCollection
from wrapastac._items import ItemCollection
from wrapastac.exceptions import UnknownProviderError
from wrapastac.providers import Element84, PlanetaryComputer

# ---------------------------------------------------------------------------
# Concrete test subclasses
# ---------------------------------------------------------------------------


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
    default_bands = ["elevation"]
    _fallback_band_mapping = {"elevation": "data"}


# ---------------------------------------------------------------------------
# Provider resolution
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Missing required class attributes
# ---------------------------------------------------------------------------


def test_missing_collection_id_raises():
    with pytest.raises(TypeError, match="collection_id"):

        class _Bad(STACCollection):
            default_resolution = 10
            default_dtype = "uint16"
            default_nodata = 0
            default_bands = ["red"]

        _Bad(provider="element84")


def test_missing_default_bands_raises():
    with pytest.raises(TypeError, match="default_bands"):

        class _Bad(STACCollection):
            collection_id = "test"
            default_resolution = 10
            default_dtype = "uint16"
            default_nodata = 0

        _Bad(provider="element84")


# ---------------------------------------------------------------------------
# Band resolution via eo:bands metadata
# ---------------------------------------------------------------------------


def test_resolve_bands_mpc_style(s2_mpc_item):
    """MPC-style items have native asset keys (B04) mapped via eo:bands common_name."""
    col = _TestCollection(provider="element84")
    items = ItemCollection([s2_mpc_item])
    asset_keys, reverse = col._resolve_bands(items, ["red", "nir"])
    assert asset_keys == ["B04", "B08"]
    assert reverse == {"B04": "red", "B08": "nir"}


def test_resolve_bands_e84_style(s2_e84_item):
    """E84-style items already use common names as asset keys — no rename needed."""
    col = _TestCollection(provider="element84")
    items = ItemCollection([s2_e84_item])
    asset_keys, reverse = col._resolve_bands(items, ["red", "nir"])
    assert asset_keys == ["red", "nir"]
    assert reverse == {}


def test_resolve_bands_fallback_mapping(s1_item):
    """SAR items have no eo:bands metadata — fallback to collection _fallback_band_mapping."""
    from wrapastac.collections import Sentinel1

    col = Sentinel1(provider="planetary_computer")
    items = ItemCollection([s1_item])
    asset_keys, reverse = col._resolve_bands(items, ["vv", "vh"])
    assert asset_keys == ["vv", "vh"]
    assert reverse == {}


def test_resolve_bands_unknown_falls_back_to_name(s2_mpc_item):
    """Unknown band name falls back to itself (pass-through to odc-stac)."""
    col = _TestCollection(provider="element84")
    items = ItemCollection([s2_mpc_item])
    asset_keys, _ = col._resolve_bands(items, ["coastal"])
    # coastal maps to B01 via eo:bands; if not in item just returns "coastal"
    assert "coastal" in asset_keys or "B01" in asset_keys


# ---------------------------------------------------------------------------
# EPSG detection
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# load() validates empty ItemCollection
# ---------------------------------------------------------------------------


def test_load_raises_on_empty_items():
    from wrapastac.exceptions import EmptyItemCollectionError

    col = _TestCollection(provider="element84")
    with pytest.raises(EmptyItemCollectionError):
        col.load(ItemCollection([]))
