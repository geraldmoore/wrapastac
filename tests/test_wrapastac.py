"""Tests for the top-level wrapastac package imports."""

from __future__ import annotations


def test_top_level_imports():
    import wrapastac

    assert hasattr(wrapastac, "Sentinel2")
    assert hasattr(wrapastac, "Sentinel1")
    assert hasattr(wrapastac, "Landsat")
    assert hasattr(wrapastac, "HLSLandsat")
    assert hasattr(wrapastac, "HLSSentinel")
    assert hasattr(wrapastac, "CopDEM30")
    assert hasattr(wrapastac, "ESRILULC")
    assert hasattr(wrapastac, "RZLULC")
    assert hasattr(wrapastac, "LidarEngland")
    assert hasattr(wrapastac, "Element84")
    assert hasattr(wrapastac, "PlanetaryComputer")
    assert hasattr(wrapastac, "STACCollection")
    assert hasattr(wrapastac, "StaticSTACCollection")
    assert hasattr(wrapastac, "ItemCollection")
    assert hasattr(wrapastac, "EmptyItemCollectionError")
    assert hasattr(wrapastac, "UnknownProviderError")


def test_geometry_subpackage_imports():
    from wrapastac.geometry import bbox, from_geodataframe, point_to_bbox, point_to_circle

    assert callable(point_to_bbox)
    assert callable(point_to_circle)
    assert callable(from_geodataframe)
    assert callable(bbox)


def test_providers_subpackage_imports():
    from wrapastac.providers import Element84, PlanetaryComputer, resolve_provider

    assert callable(resolve_provider)
    assert isinstance(Element84(), Element84)
    assert isinstance(PlanetaryComputer(), PlanetaryComputer)
