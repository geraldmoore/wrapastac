from collections.abc import Callable

import planetary_computer

from wrapastac.providers._base import Provider


class PlanetaryComputer(Provider):
    """Microsoft Planetary Computer search. Assets require signing."""

    @property
    def api_url(self) -> str:
        return "https://planetarycomputer.microsoft.com/api/stac/v1"

    @property
    def modifier(self) -> Callable:
        return planetary_computer.sign_inplace
