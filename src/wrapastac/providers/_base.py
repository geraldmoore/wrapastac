from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable


class Provider(ABC):
    """Abstract base class representing a STAC API provider.

    A Provider knows two things: where the STAC API lives (api_url) and how to
    authenticate with it (modifier). Subclass this to add support for private or
    custom STAC endpoints.
    """

    @property
    @abstractmethod
    def api_url(self) -> str:
        """The root URL of the STAC API."""

    @property
    def modifier(self) -> Callable | None:
        """Optional callable passed to pystac_client.Client.open() to sign/modify requests."""
        return None

    @property
    def headers(self) -> dict[str, str] | None:
        """Optional HTTP headers to include with every request."""
        return None

    def __repr__(self) -> str:
        return f"{type(self).__name__}(api_url={self.api_url!r})"
