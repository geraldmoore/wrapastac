from __future__ import annotations

import os
from collections.abc import Callable
from typing import Any

import requests

from wrapastac.providers._base import Provider


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

        if not self._client_id or not self._client_secret:
            raise ValueError(
                "CopernicusDataSpaceEcosystem requires OAuth2 credentials. "
                "Set CDSE_CLIENT_ID and CDSE_CLIENT_SECRET environment variables, "
                "or pass client_id and client_secret directly."
            )

    @property
    def api_url(self) -> str:
        return "https://stac.dataspace.copernicus.eu/v1"

    @property
    def use_cql2(self) -> bool:
        return True

    def _get_token(self) -> str:
        """Fetch or return cached OAuth2 token."""
        if self._token is not None:
            return self._token

        response = requests.post(
            "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
            data={
                "grant_type": "client_credentials",
                "client_id": self._client_id,
                "client_secret": self._client_secret,
            },
            timeout=30,
        )
        response.raise_for_status()
        self._token = response.json()["access_token"]
        return self._token

    def _make_modifier(self) -> Callable:
        """Return a callable that injects the Bearer token into requests."""

        def modifier(request: Any) -> Any:
            token = self._get_token()
            request.headers["Authorization"] = f"Bearer {token}"
            return request

        return modifier

    @property
    def modifier(self) -> Callable | None:
        return self._make_modifier()
