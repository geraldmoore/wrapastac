from __future__ import annotations

from typing import ClassVar

from wrapastac._base import STACCollection


class HLSLandsat(STACCollection):
    """NASA Harmonized Landsat Sentinel-2 (HLS) — Landsat component.

    Supported providers: "planetary_computer".

    HLS provides cross-calibrated, 30 m surface reflectance from Landsat 8/9
    and Sentinel-2, resampled to a common MGRS tiling grid.

    Band names: B01–B07, B09–B12, QA.
    """

    collection_id: ClassVar[str] = "hls2-l30"
    default_resolution: ClassVar[int] = 30
    default_dtype: ClassVar[str] = "int16"
    default_nodata: ClassVar[int] = -9999
    default_bands: ClassVar[list[str]] = ["red", "green", "blue", "nir"]
    _fallback_band_mapping: ClassVar[dict[str, str]] = {
        "coastal": "B01",
        "blue": "B02",
        "green": "B03",
        "red": "B04",
        "nir": "B05",
        "swir16": "B06",
        "swir22": "B07",
        "cirrus": "B09",
        "swir12": "B10",
        "swir22b": "B11",
        "nir08": "B08",
    }


class HLSSentinel(STACCollection):
    """NASA Harmonized Landsat Sentinel-2 (HLS) — Sentinel-2 component.

    Supported providers: "planetary_computer".

    Band names: B01–B12, B8A, QA.
    """

    collection_id: ClassVar[str] = "hls2-s30"
    default_resolution: ClassVar[int] = 30
    default_dtype: ClassVar[str] = "int16"
    default_nodata: ClassVar[int] = -9999
    default_bands: ClassVar[list[str]] = ["red", "green", "blue", "nir"]
    _fallback_band_mapping: ClassVar[dict[str, str]] = {
        "coastal": "B01",
        "blue": "B02",
        "green": "B03",
        "red": "B04",
        "rededge1": "B05",
        "rededge2": "B06",
        "rededge3": "B07",
        "nir": "B08",
        "nir08": "B8A",
        "nir09": "B09",
        "cirrus": "B10",
        "swir16": "B11",
        "swir22": "B12",
    }
