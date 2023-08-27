"""Module to manage the findme config file."""
import os
import re
import json

from pathlib import Path
from typing import List

from pydantic import BaseModel, field_validator

from appdirs import user_config_dir

from find_patterns.exceptions import DuplicateAliasError, IllegalPatternError


FINDME_APPNAME = "findme"


class Pattern(BaseModel):
    """Dataclass describing a pattern in the user's config file."""

    alias: str
    """Alias for the pattern object. For example; `excel` for patterns matching `.xslx` variants. """
    pattern: str
    """Regex pattern to locate this alias."""
    files_only: bool = False
    """Whether or not this pattern should only match files."""
    directories_only: bool = False
    """Whether or not this pattern should only match directories."""

    @field_validator("pattern")
    def validate_pattern(cls, pattern: str) -> str:
        """Validates if the given pattern can be compiled to a regex expression."""
        try:
            re.compile(pattern)
        except re.error as e:
            raise IllegalPatternError(
                f"Given pattern couldn't be compiled to a valid regex: {pattern}"
            ) from e

        return pattern


def load_config(config_path: str = None) -> List[Pattern]:
    """Parse the user config for `Patterns`.

    If `config_path` is not provided, the config will be loaded from the
    location defined by `get_default_config_location`.
    Generally, this is a standard location in the system's user config directory.

    Args:
        config_path (Optional): Load the config from a specific path instead of the default location.

    Returns:
        A list of `Pattern` objects found in the config.

    Raises:
        `FileNotFoundError` if the config cannot be located.
    """
    patterns: List[Pattern] = []

    with open(config_path or get_default_config_location(), "r") as f:
        for alias, pattern_data in json.load(f).items():
            patterns.append(Pattern(**pattern_data))

    return patterns


def save_config(patterns: List[Pattern], config_path: str = None):
    """Write the given `Pattern`s to the user config file.

    Args:
        patterns: A list of `Patterns` to write to the config.
        config_path (Optional): The location of the config to write to. Uses the default location if not provided.

    Raises:
        `DuplicateAliasError` if the given patterns define the same alias more than once.
    """
    patterns_dict = {}

    for pattern in patterns:
        if pattern.alias in patterns_dict:
            raise DuplicateAliasError(
                f"Alias {pattern.alias} already present in config."
            )

        patterns_dict[pattern.alias] = pattern.model_dump()

    config_path: Path = Path(config_path or get_default_config_location())

    if not config_path.parent.is_dir():
        config_path.parent.mkdir(parents=True)

    with open(config_path, "w") as f:
        f.write(json.dumps(patterns_dict))


def get_default_config_location() -> str:
    """Get the appropriate default location for the user config file based on platform."""
    return str(Path(user_config_dir(FINDME_APPNAME)) / "config.json")
