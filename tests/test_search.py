"""Tests for searching the filesystem."""
import os
import json

from pathlib import Path

from unittest import mock

from pyfakefs.fake_filesystem_unittest import TestCase

from findme.config import Pattern
from findme.search import find_pattern, find


TEST_FILES = [
    "/test/raw_files/python_file_1.py",
    "/test/raw_files/python_file_2.py",
    "/test/raw_files/text_file_1.txt",
    "/test/raw_files/text_file_2.txt",
    "/test/configs/config_file_1.json",
    "/test/configs/config_file_2.yaml",
    "/test/.cache/cache_file_1.so",
    "/test/.cache/cache_file_2.so",
    "/test/.pycache/pycache_file_1.pyc",
    "/test/.pycache/pycache_file_2.pyc",
]


class SearchTestCase(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

        for f in TEST_FILES:
            self.fs.create_file(str(Path(f)))  # Normalize to operating system

    def test_find_files(self):
        ### Test a couple file extensions
        # Python file
        pattern = Pattern(alias="py", pattern=r"\.py$", files_only=True)
        self.assertEqual(len(list(find_pattern("test", pattern))), 2)

        # Python or compliled python files
        pattern = Pattern(alias="compiled-py", pattern=r"\.pyc?$", files_only=True)
        self.assertEqual(len(list(find_pattern("test", pattern))), 4)

        # Json or yaml config files
        pattern = Pattern(alias="configs", pattern=rf"\.(json|yaml)$", files_only=True)
        self.assertEqual(len(list(find_pattern("test", pattern))), 2)

        # All cache directories
        pattern = Pattern(
            alias="cache-files", pattern=rf"\.(py)?cache", directories_only=True
        )
        self.assertEqual(len(list(find_pattern("test", pattern))), 2)

        # Missing file extension
        pattern = Pattern(
            alias="missing-files", pattern=rf"\.asdf", directories_only=True
        )
        self.assertEqual(len(list(find_pattern("test", pattern))), 0)
