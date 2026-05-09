from typing import ClassVar

import pystac
import xarray

from wrapastac._base import STACCollection
from wrapastac._harmonise import harmonise_s2


class Sentinel2(STACCollection):
    """Sentinel-2 L2A."""

    collection_id: ClassVar[str] = "sentinel-2-l2a"
    default_resolution: ClassVar[int] = 10
    default_dtype: ClassVar[str] = "uint16"
    default_nodata: ClassVar[int] = 0
    default_bands: ClassVar[list[str]] = ["blue", "green", "red", "nir", "SCL"]

    def _build_query(self, cloud_cover: int | None) -> dict | None:
        if cloud_cover is None:
            return None
        return {"eo:cloud_cover": {"lt": cloud_cover}}

    def _maybe_harmonise(self, ds: xarray.Dataset, items: list[pystac.Item]) -> xarray.Dataset:
        return harmonise_s2(ds, items)
