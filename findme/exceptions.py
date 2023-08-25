class NoSuchAliasError(Exception):
    """Exception raised when a requested alias is not available."""


class DuplicateAliasError(Exception):
    """Exception raised when a pattern already exists with the same alias."""


class IllegalPatternError(Exception):
    """Exception raised when a pattern is not valid."""
