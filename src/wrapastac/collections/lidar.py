from __future__ import annotations

from typing import ClassVar

from wrapastac._base import StaticSTACCollection


class LidarEngland(StaticSTACCollection):
    """5 m LiDAR Digital Terrain Model for England.

    This collection requires a custom Provider pointing to the STAC endpoint
    that hosts the data. Pass a Provider instance at construction time::

        from wrapastac import LidarEngland
        from wrapastac.providers import Provider


        class MyProvider(Provider):
            @property
            def api_url(self) -> str:
                return "https://my.internal.stac.endpoint"


        lidar = LidarEngland(provider=MyProvider())
        items = lidar.search(geometry=geom)
        ds = lidar.load(items, geometry=geom)

    Band names: "data".
    """

    collection_id: ClassVar[str] = "lidar-5m-england"
    default_resolution: ClassVar[int] = 5
    default_dtype: ClassVar[str] = "float32"
    default_nodata: ClassVar[float] = -32767.0
    default_bands: ClassVar[list[str]] = ["data"]
