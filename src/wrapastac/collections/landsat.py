from __future__ import annotations

from typing import ClassVar

from wrapastac._base import STACCollection


class Landsat(STACCollection):
    """Landsat Collection 2 Level-2 surface reflectance and surface temperature.

    Supported providers: "planetary_computer".

    Band names follow STAC eo:common_name conventions:
    coastal, blue, green, red, nir08, swir16, swir22, lwir11, qa_pixel.
    """

    collection_id: ClassVar[str] = "landsat-c2-l2"
    default_resolution: ClassVar[int] = 30
    default_dtype: ClassVar[str] = "uint16"
    default_nodata: ClassVar[int] = 0
    default_bands: ClassVar[list[str]] = ["red", "green", "blue", "nir08"]

    def _build_query(self, cloud_cover: int | None) -> dict | None:
        if cloud_cover is None:
            return None
        return {"eo:cloud_cover": {"lt": cloud_cover}}
