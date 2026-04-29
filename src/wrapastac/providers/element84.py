from __future__ import annotations

from wrapastac.providers._base import Provider


class Element84(Provider):
    """Element84 Earth Search STAC API (https://earth-search.aws.element84.com/v1).

    No authentication required. Assets are publicly accessible on AWS S3.
    """

    @property
    def api_url(self) -> str:
        return "https://earth-search.aws.element84.com/v1"

    @property
    def use_cql2(self) -> bool:
        return True
