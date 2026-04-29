from __future__ import annotations

from typing import ClassVar

from wrapastac._base import StaticSTACCollection


class CopDEM30(StaticSTACCollection):
    """Copernicus Digital Elevation Model at 30 m resolution (GLO-30).

    Supported providers: "planetary_computer".

    Band names: "elevation" (maps to the "data" asset).

    Assets are stored in EPSG:4326, so reprojection to UTM is disabled to avoid
    precision loss. Native COG resolution is used instead of a fixed metre value.
    """

    collection_id: ClassVar[str] = "cop-dem-glo-30"
    default_resolution: ClassVar[int] = 30
    default_dtype: ClassVar[str] = "float32"
    default_nodata: ClassVar[float] = -32767.0
    default_bands: ClassVar[list[str]] = ["elevation"]
    _fallback_band_mapping: ClassVar[dict[str, str]] = {"elevation": "data"}

    reproject_wgs84_to_utm: ClassVar[bool] = False
    use_native_resolution: ClassVar[bool] = True
