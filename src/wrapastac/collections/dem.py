from typing import ClassVar

from wrapastac._base import StaticSTACCollection


class CopDEM30(StaticSTACCollection):
    """CopDEM GLO-30."""

    collection_id: ClassVar[str] = "cop-dem-glo-30"
    default_resolution: ClassVar[int] = 30
    default_dtype: ClassVar[str] = "float32"
    default_nodata: ClassVar[float] = -32767.0
    default_bands: ClassVar[list[str]] = ["data"]

    reproject_wgs84_to_utm: ClassVar[bool] = False
    use_native_resolution: ClassVar[bool] = True
