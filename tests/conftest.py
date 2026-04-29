"""Shared fixtures for wrapastac tests."""

from __future__ import annotations

from datetime import datetime

import pystac
import pytest


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


@pytest.fixture
def s2_mpc_item() -> pystac.Item:
    """A Sentinel-2 MPC-style item where asset keys are native band names (B04, B08)."""
    return make_item(
        item_id="S2B_32ULD_20240615_0_L2A",
        assets={
            "B02": ("blue", "B02"),
            "B03": ("green", "B03"),
            "B04": ("red", "B04"),
            "B08": ("nir", "B08"),
            "SCL": (None, "SCL"),
        },
    )


@pytest.fixture
def s2_e84_item() -> pystac.Item:
    """A Sentinel-2 E84-style item where asset keys are common names."""
    return make_item(
        item_id="S2B_32ULD_20240615_E84",
        assets={
            "blue": ("blue", "blue"),
            "green": ("green", "green"),
            "red": ("red", "red"),
            "nir": ("nir", "nir"),
            "scl": (None, "scl"),
        },
    )


@pytest.fixture
def s1_item() -> pystac.Item:
    """A Sentinel-1 RTC item with no eo:bands common names."""
    return make_item(
        item_id="S1A_IW_SLC_20240615",
        cloud_cover=None,
        assets={
            "vv": (None, "vv"),
            "vh": (None, "vh"),
        },
    )
