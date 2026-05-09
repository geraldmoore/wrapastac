import logging
from collections.abc import Iterator
from datetime import datetime
from typing import Any

import pandas as pd
import pystac

from wrapastac.exceptions import EmptyItemCollectionError

logger = logging.getLogger(__name__)

_MAX_NUMBER_OF_RESULTS = 500


class ItemCollection:
    """Collection of STAC items."""

    def __init__(
        self,
        items: list[pystac.Item],
        max_number_of_results: int = _MAX_NUMBER_OF_RESULTS,
    ) -> None:
        """Create an ItemCollection from a list of STAC items.

        Args:
            items (list[pystac.Item]): The STAC items to wrap.
            max_number_of_results (int): Item count above which a warning is logged.
        """
        self._items = items
        self._max_number_of_results = max_number_of_results
        if len(items) > max_number_of_results:
            logger.warning(
                "Search returned %d items. Consider narrowing your date range, "
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
        """Acquisition dates as YYYY-MM-DD strings."""
        return [
            item.datetime.strftime("%Y-%m-%d") if item.datetime else "unknown"
            for item in self._items
        ]

    @property
    def cloud_cover(self) -> list[float | None]:
        """Cloud cover percentage for each item, or None if not available."""
        return [item.properties.get("eo:cloud_cover") for item in self._items]

    def to_dataframe(self) -> pd.DataFrame:
        """Summarise the collection as a DataFrame.

        Returns:
            pd.DataFrame: One row per item with id, date, cloud_cover, and collection columns.
        """
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
    ) -> "ItemCollection":
        """Return a filtered subset of the collection.

        Args:
            cloud_cover_lt (float | None): Keep items with cloud cover below this percentage. Optional, defaults to None.
            before (str | datetime | None): Keep items acquired before this date. Optional, defaults to None.
            after (str | datetime | None): Keep items acquired on or after this date. Optional, defaults to None.
            tile (str | None): Matches s2:mgrs_tile, grid:code, or Landsat path/row format. Optional, defaults to None.

        Returns:
            ItemCollection: A new ItemCollection containing only the matching items.
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

        return ItemCollection(items, max_number_of_results=self._max_number_of_results)

    def sort_by_cloud_cover(self) -> "ItemCollection":
        """Sort by ascending cloud cover.

        Returns:
            ItemCollection: A new ItemCollection sorted from least to most cloudy.
        """

        def _key(item: pystac.Item) -> float:
            cc = item.properties.get("eo:cloud_cover")
            return cc if cc is not None else float("inf")

        return ItemCollection(
            sorted(self._items, key=_key),
            max_number_of_results=self._max_number_of_results,
        )

    def unique_dates(self) -> "ItemCollection":
        """Get one item per date prioritising the least cloudy.

        Returns:
            ItemCollection: A new ItemCollection with at most one item per acquisition date.
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

        return ItemCollection(result, max_number_of_results=self._max_number_of_results)

    def _assert_non_empty(self) -> None:
        if not self._items:
            raise EmptyItemCollectionError(
                "Cannot load from an empty ItemCollection. "
                "Check your date range, geometry, and cloud cover threshold."
            )


def _parse_dt(value: str | datetime) -> datetime:
    """Parse a date value into a naive datetime.

    Args:
        value (str | datetime): An ISO format date string or datetime object.

    Returns:
        datetime: A timezone-naive datetime.
    """
    if isinstance(value, datetime):
        return value.replace(tzinfo=None)
    return datetime.fromisoformat(value)


def _matches_tile(item: pystac.Item, tile: str) -> bool:
    """Check whether a STAC item matches a given tile identifier.

    Args:
        item (pystac.Item): The STAC item to check.
        tile (str): A tile identifier in MGRS, grid code, or Landsat path/row format.

    Returns:
        bool: True if the item matches the tile, False otherwise.
    """
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
