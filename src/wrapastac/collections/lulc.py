from __future__ import annotations

from typing import ClassVar

from wrapastac._base import StaticSTACCollection


class ESRILULC(StaticSTACCollection):
    """ESRI 10 m Annual Land Use / Land Cover (2017–2023).

    Supported providers: "planetary_computer".

    Band names: "data".
    """

    collection_id: ClassVar[str] = "io-lulc-annual-v02"
    default_resolution: ClassVar[int] = 10
    default_dtype: ClassVar[str] = "uint8"
    default_nodata: ClassVar[int] = 0
    default_bands: ClassVar[list[str]] = ["data"]
    _fallback_band_mapping: ClassVar[dict[str, str]] = {"data": "data"}


class RZLULC(StaticSTACCollection):
    """Riparian Zone Land Use / Land Cover (io-lulc-riparian-zones).

    Supported providers: "planetary_computer".

    Band names: "data" (maps to the "rz_lulc" asset).
    """

    collection_id: ClassVar[str] = "io-lulc-riparian-zones"
    default_resolution: ClassVar[int] = 10
    default_dtype: ClassVar[str] = "uint8"
    default_nodata: ClassVar[int] = 0
    default_bands: ClassVar[list[str]] = ["data"]
    _fallback_band_mapping: ClassVar[dict[str, str]] = {"data": "rz_lulc"}
