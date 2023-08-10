"""Module to manage the findme config file."""
import re
import json

from pathlib import Path
from typing import List

from pydantic import BaseModel, field_validator

from appdirs import user_config_dir

from findme import FINDME_APPNAME
from findme.exceptions import DuplicateAliasError


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

    @field_validator
    @classmethod
    def validate_pattern(cls, pattern: str) -> str:
        """Validates if the given pattern can be compiled to a regex expression."""
        re.compile(pattern)
        return pattern


def load_config(config_path: str = None) -> List[Pattern]:
    """Parse the user config for `Pattern`s."""
    patterns: List[Pattern] = []

    with open(config_path or _get_default_config_location(), "r") as f:
        for alias, pattern_data in json.load(f):
            patterns.append(Pattern(**pattern_data))

    return patterns


def save_config(patterns: List[Pattern], config_path: str = None):
    """Write the given `Pattern`s to the user config file."""
    patterns_dict = {}

    for pattern in patterns:
        if pattern.alias in patterns_dict:
            raise DuplicateAliasError(
                f"Alias {pattern.alias} already present in config."
            )

        patterns_dict[pattern.alias] = pattern.dict()

    with open(config_path or _get_default_config_location(), "w") as f:
        f.write(json.dumps(patterns_dict))


def _get_default_config_location() -> str:
    """Get the appropriate default location for the user config file based on platform."""
    return str(Path(user_config_dir(FINDME_APPNAME)) / "config.json")
