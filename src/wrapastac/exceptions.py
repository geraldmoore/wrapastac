from __future__ import annotations


class EmptyItemCollectionError(ValueError):
    """Raised when .load() is called on an ItemCollection with no items."""


class UnknownProviderError(ValueError):
    """Raised when a provider string cannot be resolved to a known Provider."""
