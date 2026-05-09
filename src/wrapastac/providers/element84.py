from wrapastac.providers._base import Provider


class Element84(Provider):
    """Element84 Earth Search."""

    @property
    def api_url(self) -> str:
        return "https://earth-search.aws.element84.com/v1"
