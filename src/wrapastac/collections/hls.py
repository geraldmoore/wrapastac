from typing import ClassVar

from wrapastac._base import STACCollection


class HLSLandsat(STACCollection):
    """HLS Landsat 30m."""

    collection_id: ClassVar[str] = "hls2-l30"
    default_resolution: ClassVar[int] = 30
    default_dtype: ClassVar[str] = "int16"
    default_nodata: ClassVar[int] = -9999
    default_bands: ClassVar[list[str]] = ["B04", "B03", "B02", "B05"]


class HLSSentinel(STACCollection):
    """HLS Sentinel-2 30m."""

    collection_id: ClassVar[str] = "hls2-s30"
    default_resolution: ClassVar[int] = 30
    default_dtype: ClassVar[str] = "int16"
    default_nodata: ClassVar[int] = -9999
    default_bands: ClassVar[list[str]] = ["B04", "B03", "B02", "B08"]
