"""Functionality to search the filesystem."""
import os
import re
import sys

from typing import Generator, List

from pydantic import BaseModel, field_validator

from findme.config import Pattern


def find_pattern(root: str, pattern: Pattern) -> Generator[str]:
    """Call `find` with the properties of the given `pattern`. See `find`."""
    return find(
        root,
        pattern.pattern,
        files_only=pattern.files_only,
        directories_only=pattern.directories_only,
    )


def find(
    root: str, pattern: str, files_only: bool = False, directories_only: bool = False
) -> Generator[str]:
    """Recursively walk through `root` and yield any files or folders that match the regular expression `pattern`.

    Args:
        root: Initial directory to search in.
        pattern: Regex-compilable pattern to match against files.
        files_only (Optional): Whether or not to only search for files.
        directories_only (Optional): Whether or not to only search for directories.

    Yields:
        Descendent paths of `root` which matched the input arguments.
    """
    compiled_pattern = re.compile(pattern)

    for root, dirs, files in os.walk(root):
        ### Separate files and directories as specified
        to_search = []

        to_search += dirs if not files_only
        to_search += files if not directories_only

        ### Filter items by regex match
        for item in to_search:
            if compiled_pattern.match(item):
                yield item
