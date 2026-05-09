from abc import ABC, abstractmethod
from collections.abc import Callable


class Provider(ABC):
    """Abstract STAC API provider."""

    @property
    @abstractmethod
    def api_url(self) -> str:
        """The STAC API URL."""

    @property
    def modifier(self) -> Callable | None:
        """Optional callable to sign or modify requests."""
        return None

    @property
    def headers(self) -> dict[str, str] | None:
        """Optional HTTP headers."""
        return None

    def __repr__(self) -> str:
        return f"{type(self).__name__}(api_url={self.api_url!r})"
