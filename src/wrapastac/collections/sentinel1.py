from typing import ClassVar

from wrapastac._base import STACCollection


class Sentinel1(STACCollection):
    """Sentinel-1 RTC."""

    collection_id: ClassVar[str] = "sentinel-1-rtc"
    default_resolution: ClassVar[int] = 10
    default_dtype: ClassVar[str] = "float32"
    default_nodata: ClassVar[float] = -32768.0
    default_bands: ClassVar[list[str]] = ["vv", "vh"]
