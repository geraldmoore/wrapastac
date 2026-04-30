from __future__ import annotations

import logging
from collections.abc import Iterator
from datetime import datetime
from typing import Any

import pandas as pd
import pystac

from wrapastac.exceptions import EmptyItemCollectionError

logger = logging.getLogger(__name__)

_LARGE_RESULT_DEFAULT = 500


class ItemCollection:
    """A searchable, filterable collection of STAC items returned by .search().

    Wraps a list of pystac.Item objects with convenience accessors and a chainable
    .filter() method. Transparent to odc-stac.load() via __iter__ and __getitem__.
    """

    def __init__(
        self,
        items: list[pystac.Item],
        large_result_threshold: int = _LARGE_RESULT_DEFAULT,
    ) -> None:
        self._items = items
        self._large_result_threshold = large_result_threshold
        if len(items) > large_result_threshold:
            logger.warning(
                "Search returned %d items — consider narrowing your date range, "
                "geometry, or cloud cover threshold.",
                len(items),
            )

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[pystac.Item]:
        return iter(self._items)

    def __getitem__(self, idx: int) -> pystac.Item:
        return self._items[idx]

    def __repr__(self) -> str:
        return f"ItemCollection({len(self._items)} items)"

    @property
    def dates(self) -> list[str]:
        """Acquisition dates as YYYY-MM-DD strings, sorted ascending."""
        return [
            item.datetime.strftime("%Y-%m-%d") if item.datetime else "unknown"
            for item in self._items
        ]

    @property
    def cloud_cover(self) -> list[float | None]:
        """Cloud cover percentage for each item, or None if not available."""
        return [item.properties.get("eo:cloud_cover") for item in self._items]

    def to_dataframe(self) -> pd.DataFrame:
        """Summarise the collection as a DataFrame with id, date, cloud_cover, collection."""
        rows: list[dict[str, Any]] = []
        for item in self._items:
            rows.append(
                {
                    "id": item.id,
                    "date": item.datetime,
                    "cloud_cover": item.properties.get("eo:cloud_cover"),
                    "collection": item.collection_id,
                }
            )
        return pd.DataFrame(rows)

    def filter(
        self,
        cloud_cover_lt: float | None = None,
        before: str | datetime | None = None,
        after: str | datetime | None = None,
        tile: str | None = None,
    ) -> ItemCollection:
        """Return a new ItemCollection with items matching all given criteria.

        Args:
            cloud_cover_lt: Keep only items with cloud cover strictly below this value.
            before: Keep only items acquired strictly before this date (YYYY-MM-DD or datetime).
            after: Keep only items acquired on or after this date (YYYY-MM-DD or datetime).
            tile: Keep only items belonging to this tile. Matches against ``s2:mgrs_tile``
                (e.g. ``"32UMF"``), ``grid:code`` (e.g. ``"MGRS-32UMF"``), or Landsat
                path/row expressed as ``"path/row"`` (e.g. ``"200/30"``).
        """
        items = list(self._items)

        if cloud_cover_lt is not None:
            items = [
                item
                for item in items
                if (cc := item.properties.get("eo:cloud_cover")) is not None and cc < cloud_cover_lt
            ]

        if before is not None:
            cutoff = _parse_dt(before)
            items = [
                item
                for item in items
                if item.datetime and item.datetime.replace(tzinfo=None) < cutoff
            ]

        if after is not None:
            floor = _parse_dt(after)
            items = [
                item
                for item in items
                if item.datetime and item.datetime.replace(tzinfo=None) >= floor
            ]

        if tile is not None:
            items = [item for item in items if _matches_tile(item, tile)]

        return ItemCollection(items, large_result_threshold=self._large_result_threshold)

    def sort_by_cloud_cover(self) -> ItemCollection:
        """Return a new ItemCollection sorted by ascending cloud cover.

        Items with no cloud cover data (None) are placed last.
        """

        def _key(item: pystac.Item) -> float:
            cc = item.properties.get("eo:cloud_cover")
            return cc if cc is not None else float("inf")

        return ItemCollection(
            sorted(self._items, key=_key),
            large_result_threshold=self._large_result_threshold,
        )

    def unique_dates(self) -> ItemCollection:
        """Return one item per calendar date, keeping the least cloudy item for each date.

        When multiple items share the same acquisition date, the item with the lowest
        ``eo:cloud_cover`` is kept. If no items have cloud cover data, the first item
        for that date is kept. The result is sorted ascending by date.
        """
        by_date: dict[str, list[pystac.Item]] = {}
        for item in self._items:
            if item.datetime:
                key = item.datetime.strftime("%Y-%m-%d")
                by_date.setdefault(key, []).append(item)

        result: list[pystac.Item] = []
        for date_key in sorted(by_date):
            candidates = by_date[date_key]
            best = min(
                candidates,
                key=lambda i: (
                    i.properties.get("eo:cloud_cover") is None,
                    i.properties.get("eo:cloud_cover") or float("inf"),
                ),
            )
            result.append(best)

        return ItemCollection(result, large_result_threshold=self._large_result_threshold)

    def _assert_non_empty(self) -> None:
        if not self._items:
            raise EmptyItemCollectionError(
                "Cannot load from an empty ItemCollection. "
                "Check your date range, geometry, and cloud cover threshold."
            )


def _parse_dt(value: str | datetime) -> datetime:
    if isinstance(value, datetime):
        return value.replace(tzinfo=None)
    return datetime.fromisoformat(value)


def _matches_tile(item: pystac.Item, tile: str) -> bool:
    props = item.properties
    if props.get("s2:mgrs_tile") == tile:
        return True
    grid_code = props.get("grid:code", "")
    if grid_code == tile or grid_code.endswith(f"-{tile}"):
        return True
    if "/" in tile:
        path_str, row_str = tile.split("/", 1)
        if (
            str(props.get("landsat:wrs_path", "")) == path_str
            and str(props.get("landsat:wrs_row", "")) == row_str
        ):
            return True
    return False
