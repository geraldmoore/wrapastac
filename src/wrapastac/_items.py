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
    ) -> ItemCollection:
        """Return a new ItemCollection with items matching all given criteria.

        Args:
            cloud_cover_lt: Keep only items with cloud cover strictly below this value.
            before: Keep only items acquired strictly before this date (YYYY-MM-DD or datetime).
            after: Keep only items acquired on or after this date (YYYY-MM-DD or datetime).
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

        return ItemCollection(items, large_result_threshold=_LARGE_RESULT_DEFAULT)

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
