from wrapastac.exceptions import UnknownProviderError
from wrapastac.providers._base import Provider
from wrapastac.providers.copernicus_dataspace import CopernicusDataSpaceEcosystem
from wrapastac.providers.element84 import Element84
from wrapastac.providers.planetary_computer import PlanetaryComputer

# Provider registry
_REGISTRY: dict[str, Provider] = {
    "element84": Element84(),
    "planetary_computer": PlanetaryComputer(),
}


def resolve_provider(provider: str | Provider) -> Provider:
    """Resolve a provider name or instance."""
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
