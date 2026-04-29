from __future__ import annotations

import logging
from collections import Counter
from datetime import date, datetime
from typing import Any, ClassVar

import numpy as np
import odc.stac
import pystac
import rioxarray  # noqa: F401  — registers .rio accessor on xarray objects
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

_REQUIRED_ATTRS = (
    "collection_id",
    "default_resolution",
    "default_dtype",
    "default_nodata",
    "default_bands",
)


class _CollectionBase:
    """Shared internals for STACCollection and StaticSTACCollection."""

    collection_id: ClassVar[str]
    default_resolution: ClassVar[int]
    default_dtype: ClassVar[str]
    default_nodata: ClassVar[float | int]
    default_bands: ClassVar[list[str]]

    _fallback_band_mapping: ClassVar[dict[str, str]] = {}
    _large_result_threshold: ClassVar[int] = 500
    reproject_wgs84_to_utm: ClassVar[bool] = True
    use_native_resolution: ClassVar[bool] = False

    def __init__(self, provider: str | Provider) -> None:
        for attr in _REQUIRED_ATTRS:
            if not hasattr(self, attr):
                raise TypeError(
                    f"{type(self).__name__} must define the class attribute {attr!r}. "
                    "See STACCollection or StaticSTACCollection for examples."
                )
        self._provider: Provider = resolve_provider(provider)

    def _open_client(self) -> Client:
        try:
            return Client.open(self._provider.api_url, modifier=self._provider.modifier)
        except Exception as e:
            raise ConnectionError(
                f"Failed to connect to STAC API at {self._provider.api_url}"
            ) from e

    def _paginate(self, client: Client, **search_params: Any) -> list[pystac.Item]:
        search = client.search(**search_params)
        items = list(search.items())
        items.sort(key=lambda x: x.datetime or datetime.min)
        return items

    def _build_query(self, cloud_cover: int | None) -> dict | None:
        return None

    def _maybe_harmonise(self, ds: xarray.Dataset, items: list[pystac.Item]) -> xarray.Dataset:
        return ds

    def _resolve_bands(
        self, items: ItemCollection, bands: list[str]
    ) -> tuple[list[str], dict[str, str]]:
        """Map common band names to provider asset keys using eo:bands metadata.

        Returns (asset_keys, reverse_mapping) where reverse_mapping maps
        asset_key → common_name for post-load renaming.
        """
        first_item = items[0]
        common_to_asset: dict[str, str] = {}

        for asset_key, asset in first_item.assets.items():
            for band_info in asset.extra_fields.get("eo:bands", []):
                common_name = band_info.get("common_name")
                if common_name and common_name not in common_to_asset:
                    common_to_asset[common_name] = asset_key

        for common_name, asset_key in self._fallback_band_mapping.items():
            if common_name not in common_to_asset:
                common_to_asset[common_name] = asset_key

        asset_keys: list[str] = []
        reverse_mapping: dict[str, str] = {}
        for band in bands:
            asset_key = common_to_asset.get(band, band)
            asset_keys.append(asset_key)
            if asset_key != band:
                reverse_mapping[asset_key] = band

        return asset_keys, reverse_mapping

    @staticmethod
    def _get_epsg(items: list[pystac.Item]) -> int:
        epsg_values: list[int] = []
        for item in items:
            code = item.properties.get("proj:epsg") or item.properties.get("proj:code")
            if code:
                if isinstance(code, str) and code.upper().startswith("EPSG:"):
                    code = code.split(":")[-1]
                epsg_values.append(int(code))
        return Counter(epsg_values).most_common(1)[0][0] if epsg_values else WGS84_EPSG

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
    ) -> xarray.Dataset:
        """Load STAC items into a clipped, band-renamed xarray Dataset.

        Args:
            items: ItemCollection returned by .search().
            geometry: Shapely geometry in WGS84 to clip the output. If None, no clipping
                is applied and the full item extents are loaded.
            bands: Common band names to load. Defaults to the collection's default_bands.
            resolution: Output resolution in metres. Defaults to the collection default.
            dtype: Output NumPy dtype string (e.g. "float32"). Defaults to collection default.
            nodata: Fill value for missing pixels. Defaults to collection default.
            resampling: Resampling method name understood by rasterio. Defaults to "nearest".
            groupby: odc-stac groupby argument (e.g. "solar_day"). Defaults to None.

        Returns:
            xarray.Dataset with one variable per band, named using common band names.
        """
        items._assert_non_empty()

        bands = bands or list(self.default_bands)
        resolution = resolution or self.default_resolution
        dtype_np = np.dtype(dtype or self.default_dtype)
        nodata_val: float | int = dtype_np.type(
            nodata if nodata is not None else self.default_nodata
        )

        asset_keys, reverse_mapping = self._resolve_bands(items, bands)

        native_epsg = self._get_epsg(list(items))
        epsg = native_epsg

        if native_epsg == WGS84_EPSG and geometry is not None and self.reproject_wgs84_to_utm:
            epsg = get_utm_epsg(lon=geometry.centroid.x, lat=geometry.centroid.y)
            logger.warning(
                "Collection assets are in EPSG:%d. Re-projecting to EPSG:%d for clipping.",
                WGS84_EPSG,
                epsg,
            )

        crs = None if epsg == native_epsg else f"EPSG:{epsg}"
        load_resolution = None if self.use_native_resolution else resolution

        clip_geom_proj: BaseGeometry | None = None
        if geometry is not None:
            clip_geom_proj = geometry_from_epsg_to_epsg(geometry, WGS84_EPSG, epsg)

        out = odc.stac.load(
            list(items),
            asset_keys,
            crs=crs,
            resolution=load_resolution,
            geopolygon=geometry,
            resampling=resampling,
            dtype=dtype_np,
            fail_on_error=False,
            groupby=groupby,
            nodata=nodata_val,
            chunks={"x": 1024, "y": 1024},
            anchor="floating",
        )

        if clip_geom_proj is not None:
            out = out.rio.clip([clip_geom_proj])

        out = self._maybe_harmonise(out, list(items))

        if isinstance(out, xarray.DataArray):
            out = out.to_dataset(dim="band")

        if reverse_mapping:
            rename = {k: v for k, v in reverse_mapping.items() if k in out.data_vars}
            if rename:
                out = out.rename(rename)

        return out


class STACCollection(_CollectionBase):
    """Base class for time-varying STAC collections (optical, SAR, etc.).

    Subclass this and define the required class attributes to add a new collection::

        class MyCollection(STACCollection):
            collection_id = "my-stac-collection"
            default_resolution = 10
            default_dtype = "uint16"
            default_nodata = 0
            default_bands = ["red", "nir"]

    Then use it::

        col = MyCollection(provider="element84")
        items = col.search(geometry=geom, start="2024-01-01", end="2024-06-01")
        ds = col.load(items, geometry=geom)
    """

    def search(
        self,
        geometry: BaseGeometry,
        start: str | date,
        end: str | date,
        cloud_cover: int | None = None,
    ) -> ItemCollection:
        """Search the STAC catalogue for items intersecting a geometry and date range.

        Args:
            geometry: Shapely geometry in WGS84 (EPSG:4326) to intersect.
            start: Start date as "YYYY-MM-DD" string or date object (inclusive).
            end: End date as "YYYY-MM-DD" string or date object (inclusive).
            cloud_cover: Maximum cloud cover percentage (0–100). Only applied to
                collections that support the eo:cloud_cover query field.

        Returns:
            ItemCollection of matching STAC items, sorted by acquisition date.
        """
        client = self._open_client()
        query = self._build_query(cloud_cover=cloud_cover)
        search_params: dict = {
            "collections": [self.collection_id],
            "intersects": geometry.__geo_interface__,
            "datetime": f"{start}/{end}",
        }
        if query:
            search_params["query"] = query

        items = self._paginate(client, **search_params)
        return ItemCollection(items, large_result_threshold=self._large_result_threshold)


class StaticSTACCollection(_CollectionBase):
    """Base class for static STAC collections with no time dimension (DEMs, LULC, etc.).

    Subclass this for collections where a date range is meaningless::

        class MyDEM(StaticSTACCollection):
            collection_id = "my-dem"
            default_resolution = 30
            default_dtype = "float32"
            default_nodata = -9999.0
            default_bands = ["elevation"]
            _fallback_band_mapping = {"elevation": "data"}
    """

    def search(self, geometry: BaseGeometry) -> ItemCollection:
        """Search the STAC catalogue for items intersecting a geometry.

        Args:
            geometry: Shapely geometry in WGS84 (EPSG:4326) to intersect.

        Returns:
            ItemCollection of matching STAC items.
        """
        client = self._open_client()
        search_params: dict = {
            "collections": [self.collection_id],
            "intersects": geometry.__geo_interface__,
        }
        items = self._paginate(client, **search_params)
        return ItemCollection(items, large_result_threshold=self._large_result_threshold)
