from __future__ import annotations

from wrapastac.exceptions import UnknownProviderError
from wrapastac.providers._base import Provider
from wrapastac.providers.copernicus_dataspace import CopernicusDataSpaceEcosystem
from wrapastac.providers.element84 import Element84
from wrapastac.providers.planetary_computer import PlanetaryComputer

_REGISTRY: dict[str, Provider] = {
    "element84": Element84(),
    "planetary_computer": PlanetaryComputer(),
}


def resolve_provider(provider: str | Provider) -> Provider:
    """Resolve a provider name string or Provider instance to a Provider object.

    Args:
        provider: Either a Provider instance or a string key from the built-in registry.
                  Built-in keys: "element84", "planetary_computer".

    Raises:
        UnknownProviderError: If the string does not match any registered provider.
    """
    if isinstance(provider, Provider):
        return provider
    if provider in _REGISTRY:
        return _REGISTRY[provider]
    raise UnknownProviderError(
        f"Unknown provider {provider!r}. "
        f"Available built-in providers: {sorted(_REGISTRY)}. "
        "Pass a Provider subclass instance for custom providers."
    )


__all__ = [
    "Provider",
    "Element84",
    "PlanetaryComputer",
    "CopernicusDataSpaceEcosystem",
    "resolve_provider",
]
