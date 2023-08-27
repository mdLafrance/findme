"""General utility for testing."""
import json

from typing import List

from find_patterns.config import Pattern


def get_test_patterns() -> List[Pattern]:
    """Generate a testing config file."""

    return [
        Pattern(alias="test_py_file", pattern="\.py$", files_only=True),
        Pattern(alias="test_maya_file", pattern="\.ma$", files_only=True),
        Pattern(alias="cache_folders", pattern="\.\w?cache\w?", directories_only=True),
    ]


def get_raw_test_pattern_data() -> dict:
    return {p.alias: p.model_dump() for p in get_test_patterns()}


def get_test_config_location(*args) -> str:
    return "test_location.json"
