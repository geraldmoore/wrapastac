from __future__ import annotations

import os
import time
from collections.abc import Callable
from typing import Any

import requests

from wrapastac.providers._base import Provider

_TOKEN_URL = (
    "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
)
_TOKEN_EXPIRY_BUFFER_S = 30  # re-fetch this many seconds before the token expires


class CopernicusDataSpaceEcosystem(Provider):
    """Copernicus Data Space Ecosystem STAC API (https://stac.dataspace.copernicus.eu).

    Requires OAuth2 authentication. Set ``CDSE_CLIENT_ID`` and ``CDSE_CLIENT_SECRET``
    environment variables, or pass credentials directly via the ``client_id`` and
    ``client_secret`` parameters.

    Args:
        client_id: OAuth2 client ID. If not provided, reads from ``CDSE_CLIENT_ID`` env var.
        client_secret: OAuth2 client secret. If not provided, reads from ``CDSE_CLIENT_SECRET`` env var.
    """

    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
    ) -> None:
        self._client_id = client_id or os.environ.get("CDSE_CLIENT_ID")
        self._client_secret = client_secret or os.environ.get("CDSE_CLIENT_SECRET")
        self._token: str | None = None
        self._token_expires_at: float = 0.0

        if not self._client_id or not self._client_secret:
            raise ValueError(
                "CopernicusDataSpaceEcosystem requires OAuth2 credentials. "
                "Set CDSE_CLIENT_ID and CDSE_CLIENT_SECRET environment variables, "
                "or pass client_id and client_secret directly."
            )

        # Build the modifier once so every call to self.modifier returns the same object.
        self._modifier: Callable = self._build_modifier()

    @property
    def api_url(self) -> str:
        return "https://stac.dataspace.copernicus.eu/v1"

    @property
    def use_cql2(self) -> bool:
        return True

    def _get_token(self) -> str:
        """Return a valid OAuth2 Bearer token, fetching a fresh one when near expiry."""
        if self._token is not None and time.monotonic() < self._token_expires_at:
            return self._token

        response = requests.post(
            _TOKEN_URL,
            data={
                "grant_type": "client_credentials",
                "client_id": self._client_id,
                "client_secret": self._client_secret,
            },
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        self._token = data["access_token"]
        ttl = data.get("expires_in", 300)
        self._token_expires_at = time.monotonic() + ttl - _TOKEN_EXPIRY_BUFFER_S
        return self._token

    def _build_modifier(self) -> Callable:
        def modifier(request: Any) -> Any:
            request.headers["Authorization"] = f"Bearer {self._get_token()}"
            return request

        return modifier

    @property
    def modifier(self) -> Callable:
        return self._modifier
