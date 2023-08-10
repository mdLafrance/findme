class NoSuchAliasError(Exception):
    """Exception raised when a requested alias is not available."""


class DuplicateAliasError(Exception):
    """Exception riased when a pattern already exists with the same alias."""
