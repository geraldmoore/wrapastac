from __future__ import annotations

from collections.abc import Callable

from wrapastac.providers._base import Provider


class PlanetaryComputer(Provider):
    """Microsoft Planetary Computer STAC API.

    Assets are access-controlled. Items are automatically signed via the
    planetary_computer package so that asset URLs remain valid during loading.
    """

    @property
    def api_url(self) -> str:
        return "https://planetarycomputer.microsoft.com/api/stac/v1"

    @property
    def modifier(self) -> Callable:
        try:
            import planetary_computer
        except ImportError as e:
            raise ImportError(
                "planetary-computer is required for the PlanetaryComputer provider. "
                "Install it with: pip install planetary-computer"
            ) from e
        return planetary_computer.sign_inplace
