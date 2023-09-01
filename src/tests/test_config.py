"""Test config loading and management."""
import os
import json

from unittest import mock

from pyfakefs.fake_filesystem_unittest import TestCase

from find_patterns.config import (
    Pattern,
    load_config,
    save_config,
    get_default_config_location,
)
from find_patterns.exceptions import IllegalPatternError, DuplicateAliasError

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
        "find_patterns.config.get_default_config_location", new=get_test_config_location
    )
    def test_load_config(self):
        # Test that dummy values are correctly reconstructed
        self.assertEqual(load_config(), get_test_patterns())

        # Check missing config raises an error
        with self.assertRaises(FileNotFoundError):
            load_config(config_path="not_a_directory")

    def test_save_config(self):
        temp_config_location = "temp_config.json"

        patterns = get_test_patterns()

        # Check we can successfully create a config
        self.assertFalse(os.path.isfile(temp_config_location))

        save_config(patterns, config_path=temp_config_location)

        self.assertTrue(os.path.isfile(temp_config_location))

        self.assertEqual(patterns, load_config(temp_config_location))

    def test_save_config_with_problems(self):
        patterns = get_test_patterns()

        # Check colliding patterns are rejected
        self.assertFalse(os.path.isfile(get_default_config_location()))

        with self.assertRaises(DuplicateAliasError):
            save_config(patterns * 2)

        # Check no config was created if problems were detected
        self.assertFalse(os.path.isfile(get_default_config_location()))
