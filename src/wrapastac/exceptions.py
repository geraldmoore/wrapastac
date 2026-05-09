class EmptyItemCollectionError(ValueError):
    """Raised when an item collection is empty."""


class UnknownProviderError(ValueError):
    """Raised when a provider string cannot be resolved to a known Provider."""
