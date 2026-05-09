import logging
from collections import Counter
from datetime import date, datetime
from typing import Any, ClassVar, Literal

import numpy as np
import odc.stac
import pystac
import rioxarray  # noqa: F401
import xarray
from odc.stac import configure_rio
from pystac_client import Client
from shapely.geometry.base import BaseGeometry

from wrapastac._crs import WGS84_EPSG, geometry_from_epsg_to_epsg, get_utm_epsg
from wrapastac._items import ItemCollection
from wrapastac.providers import resolve_provider
from wrapastac.providers._base import Provider

configure_rio(cloud_defaults=True)

logger = logging.getLogger(__name__)


class _CollectionBase:
    """Base Collection."""

    collection_id: ClassVar[str]
    default_resolution: ClassVar[int]
    default_dtype: ClassVar[str]
    default_nodata: ClassVar[float | int]
    default_bands: ClassVar[list[str]]

    _max_number_of_results: ClassVar[int] = 500
    reproject_wgs84_to_utm: ClassVar[bool] = True
    use_native_resolution: ClassVar[bool] = False

    def __init__(self, provider: str | Provider) -> None:
        """Initialise with a STAC API provider.

        Args:
            provider (str | Provider): A provider instance or a string shorthand like "element84".
        """
        self._provider: Provider = resolve_provider(provider)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(provider={self._provider!r})"

    def _open_client(self) -> Client:
        """Open a pystac_client Client connected to the provider's API.

        Returns:
            Client: An authenticated client ready for searching.
        """
        return Client.open(
            self._provider.api_url,
            modifier=self._provider.modifier,
            headers=self._provider.headers,
        )

    def _paginate(self, client: Client, **search_params: Any) -> list[pystac.Item]:
        """Fetch all pages of search results and return items sorted by datetime.

        Args:
            client (Client): An open pystac_client Client.
            **search_params (Any): Keyword arguments forwarded to client.search.

        Returns:
            list[pystac.Item]: All matching items sorted by acquisition datetime.
        """
        search = client.search(**search_params)
        items = list(search.items())
        items.sort(key=lambda x: x.datetime or datetime.min)
        return items

    def _build_query(self, cloud_cover: int | None) -> dict | None:
        """Build a CQL2 filter dict for the given search constraints.

        Args:
            cloud_cover (int | None): Maximum cloud cover percentage. Optional, defaults to None.

        Returns:
            dict | None: A CQL2 filter dict, or None if no filter is needed.
        """
        return None

    def _maybe_harmonise(self, ds: xarray.Dataset, items: list[pystac.Item]) -> xarray.Dataset:
        """Apply any collection-specific post-load harmonisation to the dataset.

        Args:
            ds (xarray.Dataset): The loaded dataset.
            items (list[pystac.Item]): The STAC items that were loaded.

        Returns:
            xarray.Dataset: The dataset after harmonisation, unchanged by default.
        """
        return ds

    @staticmethod
    def _get_epsg(items: list[pystac.Item]) -> int:
        """Determine the output EPSG code from item properties.

        Args:
            items (list[pystac.Item]): The STAC items to inspect.

        Returns:
            int: The most common EPSG code across the items, or WGS84 if none is found.
        """
        epsg_values: list[int] = []
        for item in items:
            code = item.properties.get("proj:epsg") or item.properties.get("proj:code")
            if code:
                if isinstance(code, str) and code.upper().startswith("EPSG:"):
                    code = code.split(":")[-1]
                epsg_values.append(int(code))
        if not epsg_values:
            return WGS84_EPSG
        counts = Counter(epsg_values)
        most_common_epsg = counts.most_common(1)[0][0]
        if len(counts) > 1:
            logger.warning(
                "Items span multiple EPSG codes %s. Using the most common (EPSG:%d).",
                sorted(counts),
                most_common_epsg,
            )
        return most_common_epsg

    def load(
        self,
        items: ItemCollection,
        geometry: BaseGeometry | None = None,
        bands: list[str] | None = None,
        resolution: int | None = None,
        dtype: str | None = None,
        nodata: float | int | None = None,
        resampling: str = "nearest",
        groupby: str | None = None,
        chunks: dict[str, int | Literal["auto"]] | None = None,
    ) -> xarray.Dataset:
        """Load items into a clipped xarray Dataset.

        Args:
            items (ItemCollection): The items to load.
            geometry (BaseGeometry | None): Clip geometry in WGS84. Optional, defaults to None.
            bands (list[str] | None): Band names to load. Optional, defaults to None.
            resolution (int | None): Output resolution in metres. Optional, defaults to None.
            dtype (str | None): Output NumPy dtype string. Optional, defaults to None.
            nodata (float | int | None): Nodata fill value. Optional, defaults to None.
            resampling (str): Resampling method passed to odc.stac.
            groupby (str | None): Groupby dimension passed to odc.stac. Optional, defaults to None.
            chunks (dict[str, int | Literal["auto"]] | None): Dask chunk sizes passed to odc.stac. Optional, defaults to None.

        Returns:
            xarray.Dataset: The loaded and optionally clipped dataset.
        """
        if chunks is None:
            chunks = {"x": 1024, "y": 1024}

        items._assert_non_empty()
        item_list = list(items)

        bands = bands or list(self.default_bands)
        resolution = resolution or self.default_resolution
        dtype_np = np.dtype(dtype or self.default_dtype)
        nodata_val: float | int = dtype_np.type(
            nodata if nodata is not None else self.default_nodata
        )

        native_epsg = self._get_epsg(item_list)
        epsg = native_epsg

        if native_epsg == WGS84_EPSG and geometry is not None and self.reproject_wgs84_to_utm:
            epsg = get_utm_epsg(lon=geometry.centroid.x, lat=geometry.centroid.y)
            logger.warning(
                "Collection assets are in EPSG:%d. Re-projecting to EPSG:%d for clipping.",
                WGS84_EPSG,
                epsg,
            )

        crs = None if epsg == native_epsg else f"EPSG:{epsg}"

        if self.use_native_resolution and resolution != self.default_resolution:
            logger.warning(
                "%s uses native COG resolution, ignoring the supplied resolution=%d.",
                type(self).__name__,
                resolution,
            )
        load_resolution = None if self.use_native_resolution else resolution

        clip_geom_proj: BaseGeometry | None = None
        if geometry is not None:
            clip_geom_proj = geometry_from_epsg_to_epsg(geometry, WGS84_EPSG, epsg)

        out = odc.stac.load(
            item_list,
            bands,
            crs=crs,
            resolution=load_resolution,
            geopolygon=geometry,
            resampling=resampling,
            dtype=dtype_np,
            fail_on_error=False,
            groupby=groupby,
            nodata=nodata_val,
            chunks=chunks,
            anchor="floating",
        )

        if clip_geom_proj is not None:
            out = out.rio.clip([clip_geom_proj])

        out = self._maybe_harmonise(out, item_list)

        # Convert DataArray to Dataset
        if isinstance(out, xarray.DataArray):
            out = out.to_dataset(dim="band")

        return out


class STACCollection(_CollectionBase):
    """Non-static STAC collections."""

    def search(
        self,
        geometry: BaseGeometry,
        start: str | date,
        end: str | date,
        cloud_cover: int | None = None,
    ) -> ItemCollection:
        """Search for items intersecting a geometry and date range.

        Args:
            geometry (BaseGeometry): Search geometry in WGS84.
            start (str | date): Start date of the search range.
            end (str | date): End date of the search range.
            cloud_cover (int | None): Maximum cloud cover percentage to filter by. Optional, defaults to None.

        Returns:
            ItemCollection: Matching items sorted by datetime.
        """
        client = self._open_client()
        search_params: dict = {
            "collections": [self.collection_id],
            "intersects": geometry.__geo_interface__,
            "datetime": f"{start}/{end}",
        }
        query = self._build_query(cloud_cover=cloud_cover)
        if query:
            args = []
            for prop, conditions in query.items():
                for op, value in conditions.items():
                    args.append({"op": op, "args": [{"property": prop}, value]})
            search_params["filter"] = args[0] if len(args) == 1 else {"op": "and", "args": args}
            search_params["filter_lang"] = "cql2-json"

        items = self._paginate(client, **search_params)
        return ItemCollection(items, max_number_of_results=self._max_number_of_results)


class StaticSTACCollection(_CollectionBase):
    """Static (no time dimension) STAC collections."""

    def search(self, geometry: BaseGeometry) -> ItemCollection:
        """Search for items intersecting a geometry.

        Args:
            geometry (BaseGeometry): Search geometry in WGS84.

        Returns:
            ItemCollection: Matching items.
        """
        client = self._open_client()
        search_params: dict = {
            "collections": [self.collection_id],
            "intersects": geometry.__geo_interface__,
        }
        items = self._paginate(client, **search_params)
        return ItemCollection(items, max_number_of_results=self._max_number_of_results)
