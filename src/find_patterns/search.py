"""Functionality to search the filesystem."""
import os
import re
import sys

from pathlib import Path
from typing import Generator, List

from pydantic import BaseModel, field_validator

from findme.config import Pattern


def find_pattern(root: str, pattern: Pattern) -> Generator[str, None, None]:
    """Call `find` with the properties of the given `pattern`. See `find`."""
    return find(
        root,
        pattern.pattern,
        files_only=pattern.files_only,
        directories_only=pattern.directories_only,
    )


def find(
    initial_path: str,
    pattern: str,
    files_only: bool = False,
    directories_only: bool = False,
) -> Generator[str, None, None]:
    """Recursively walk through `root` and yield any files or folders that match the regular expression `pattern`.

    NOTE: Files are matched with `re.search`, not `re.match`.

    Args:
        initial_path: Initial directory to search in.
        pattern: Regex-compilable pattern to search against files.
        files_only (Optional): Whether or not to only search for files.
        directories_only (Optional): Whether or not to only search for directories.

    Yields:
        Descendent paths of `root` which matched the input arguments.
    """
    compiled_pattern = re.compile(pattern)

    if not os.path.isdir(initial_path):
        raise FileNotFoundError(f"Given path doesn't exist: {initial_path}")

    for root, dirs, files in os.walk(initial_path):
        ### Separate files and directories as specified
        to_search = []

        to_search += dirs if not files_only else []
        to_search += files if not directories_only else []

        ### Filter items by regex match
        for item in (os.path.join(root, item) for item in to_search):
            if compiled_pattern.search(item):
                yield item
