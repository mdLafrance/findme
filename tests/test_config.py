"""Test config loading and management."""
import os
import json

from unittest import mock

from pyfakefs.fake_filesystem_unittest import TestCase

from findme.config import Pattern, load_config, save_config
from findme.exceptions import IllegalPatternError

from .utils import (
    get_test_config_location,
    get_raw_test_pattern_data,
    get_test_patterns,
)


class ConfigTestCase(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

        self.fs.create_file(
            get_test_config_location(), contents=json.dumps(get_raw_test_pattern_data())
        )

    def test_pattern_validation(self):
        """Test `Pattern` dataclass validates regex patterns correctly."""
        legal_patterns = ["asdf"]
        illegal_patterns = ["(asdf", "asjhfakshdf9172938723[]{}()"]

        pattern_data = {
            "alias": "test",
        }

        ### Test legal patterns
        for pat in legal_patterns:
            self.assertIsNotNone(Pattern(pattern=pat, **pattern_data))

        ### Test illegal patterns
        for pat in illegal_patterns:
            with self.assertRaises(IllegalPatternError):
                Pattern(pattern=pat, **pattern_data)

    def test_pattern_dataclass(self):
        """Test proper construction of `Pattern` dataclass."""
        self.assertIsNotNone(
            Pattern(
                alias="test",
                pattern="test",
            )
        )

    @mock.patch(
        "findme.config._get_default_config_location", new=get_test_config_location
    )
    def test_load_config(self):
        self.assertEqual(get_test_patterns(), load_config())

    def tests_save_config(self):
        temp_config_location = "temp_config.json"

        patterns = get_test_patterns()

        self.assertFalse(os.path.isfile(temp_config_location))

        save_config(patterns, config_path=temp_config_location)

        self.assertTrue(os.path.isfile(temp_config_location))

        self.assertEqual(patterns, load_config(temp_config_location))
