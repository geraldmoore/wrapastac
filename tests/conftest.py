"""Shared fixtures for wrapastac tests."""


from datetime import datetime

import pystac


def _make_asset(common_name: str | None, asset_key: str) -> pystac.Asset:
    extra: dict = {}
    if common_name:
        extra["eo:bands"] = [{"name": asset_key, "common_name": common_name}]
    return pystac.Asset(href=f"https://example.com/{asset_key}.tif", extra_fields=extra)


def make_item(
    item_id: str = "test-item",
    dt: str = "2024-06-15T10:00:00Z",
    cloud_cover: float | None = 10.0,
    epsg: int = 32632,
    assets: dict[str, tuple[str | None, str]] | None = None,
) -> pystac.Item:
    """Build a minimal pystac.Item for unit testing.

    Args:
        item_id: STAC item ID.
        dt: ISO 8601 datetime string.
        cloud_cover: eo:cloud_cover value, or None.
        epsg: proj:epsg value in item properties.
        assets: Mapping of asset_key → (common_name, asset_key). If common_name is None
                the asset has no eo:bands metadata (simulates SAR/DEM assets).
    """
    props: dict = {"datetime": dt, "proj:epsg": epsg}
    if cloud_cover is not None:
        props["eo:cloud_cover"] = cloud_cover

    parsed_dt = datetime.fromisoformat(dt.replace("Z", "+00:00"))

    item = pystac.Item(
        id=item_id,
        geometry={"type": "Polygon", "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]},
        bbox=[0.0, 0.0, 1.0, 1.0],
        datetime=parsed_dt,
        properties=props,
    )

    if assets:
        for key, (common_name, _) in assets.items():
            item.add_asset(key, _make_asset(common_name, key))

    return item

