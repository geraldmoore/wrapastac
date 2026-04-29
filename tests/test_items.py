"""Tests for ItemCollection wrapper."""

from __future__ import annotations

import pytest

from tests.conftest import make_item
from wrapastac._items import ItemCollection
from wrapastac.exceptions import EmptyItemCollectionError


def _collection(*args, **kwargs) -> ItemCollection:
    return ItemCollection(list(args), **kwargs)


def test_len():
    items = [make_item(item_id=f"item-{i}") for i in range(5)]
    assert len(ItemCollection(items)) == 5


def test_iter():
    items = [make_item(item_id=f"item-{i}") for i in range(3)]
    col = ItemCollection(items)
    assert list(col) == items


def test_getitem():
    items = [make_item(item_id=f"item-{i}") for i in range(3)]
    col = ItemCollection(items)
    assert col[0].id == "item-0"
    assert col[2].id == "item-2"


def test_repr():
    items = [make_item() for _ in range(7)]
    assert "7" in repr(ItemCollection(items))


def test_dates():
    items = [
        make_item(item_id="a", dt="2024-01-10T00:00:00Z"),
        make_item(item_id="b", dt="2024-03-05T00:00:00Z"),
    ]
    col = ItemCollection(items)
    assert col.dates == ["2024-01-10", "2024-03-05"]


def test_cloud_cover():
    items = [
        make_item(item_id="a", cloud_cover=5.0),
        make_item(item_id="b", cloud_cover=None),
        make_item(item_id="c", cloud_cover=80.0),
    ]
    col = ItemCollection(items)
    assert col.cloud_cover == [5.0, None, 80.0]


def test_to_dataframe():
    items = [make_item(item_id="a", cloud_cover=10.0), make_item(item_id="b", cloud_cover=20.0)]
    df = ItemCollection(items).to_dataframe()
    assert list(df.columns) == ["id", "date", "cloud_cover", "collection"]
    assert list(df["id"]) == ["a", "b"]
    assert list(df["cloud_cover"]) == [10.0, 20.0]


def test_filter_cloud_cover():
    items = [
        make_item(item_id="low", cloud_cover=5.0),
        make_item(item_id="high", cloud_cover=80.0),
        make_item(item_id="none", cloud_cover=None),
    ]
    col = ItemCollection(items)
    filtered = col.filter(cloud_cover_lt=20.0)
    assert len(filtered) == 1
    assert filtered[0].id == "low"


def test_filter_before():
    items = [
        make_item(item_id="early", dt="2023-06-01T00:00:00Z"),
        make_item(item_id="late", dt="2024-06-01T00:00:00Z"),
    ]
    col = ItemCollection(items)
    filtered = col.filter(before="2024-01-01")
    assert len(filtered) == 1
    assert filtered[0].id == "early"


def test_filter_after():
    items = [
        make_item(item_id="early", dt="2023-06-01T00:00:00Z"),
        make_item(item_id="late", dt="2024-06-01T00:00:00Z"),
    ]
    col = ItemCollection(items)
    filtered = col.filter(after="2024-01-01")
    assert len(filtered) == 1
    assert filtered[0].id == "late"


def test_filter_chaining():
    items = [
        make_item(item_id="a", dt="2024-03-01T00:00:00Z", cloud_cover=5.0),
        make_item(item_id="b", dt="2024-03-15T00:00:00Z", cloud_cover=50.0),
        make_item(item_id="c", dt="2024-05-01T00:00:00Z", cloud_cover=5.0),
    ]
    col = ItemCollection(items)
    filtered = col.filter(cloud_cover_lt=20.0).filter(before="2024-04-01")
    assert len(filtered) == 1
    assert filtered[0].id == "a"


def test_assert_non_empty_raises_on_empty():
    col = ItemCollection([])
    with pytest.raises(EmptyItemCollectionError):
        col._assert_non_empty()


def test_assert_non_empty_passes_on_non_empty():
    col = ItemCollection([make_item()])
    col._assert_non_empty()  # should not raise


def test_large_result_warning(caplog):
    import logging

    items = [make_item(item_id=f"item-{i}") for i in range(501)]
    with caplog.at_level(logging.WARNING, logger="wrapastac._items"):
        ItemCollection(items, large_result_threshold=500)
    assert "501" in caplog.text


def test_no_warning_under_threshold(caplog):
    import logging

    items = [make_item(item_id=f"item-{i}") for i in range(10)]
    with caplog.at_level(logging.WARNING, logger="wrapastac._items"):
        ItemCollection(items, large_result_threshold=500)
    assert caplog.text == ""
