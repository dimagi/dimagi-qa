import unittest

from app_script.utils import merge_dicts


class TestDeepMergeDicts(unittest.TestCase):
    def test_merge_with_empty_dicts(self):
        dict1 = {}
        dict2 = {}
        result = merge_dicts(dict1, dict2)
        self.assertEqual(result, {})

    def test_merge_with_non_empty_and_empty_dict(self):
        dict1 = {"key1": "value1"}
        dict2 = {}
        result = merge_dicts(dict1, dict2)
        self.assertEqual(result, {"key1": "value1"})

    def test_merge_with_empty_and_non_empty_dict(self):
        dict1 = {}
        dict2 = {"key1": "value1"}
        result = merge_dicts(dict1, dict2)
        self.assertEqual(result, {"key1": "value1"})

    def test_merge_with_non_empty_dicts(self):
        dict1 = {"key1": "value1"}
        dict2 = {"key2": "value2"}
        result = merge_dicts(dict1, dict2)
        self.assertEqual(result, {"key1": "value1", "key2": "value2"})

    def test_merge_with_overlapping_keys(self):
        dict1 = {"key1": "value1", "key2": "value2"}
        dict2 = {"key2": "new_value2", "key3": "value3"}
        result = merge_dicts(dict1, dict2)
        self.assertEqual(result, {"key1": "value1", "key2": "new_value2", "key3": "value3"})

    def test_merge_with_nested_dicts(self):
        dict1 = {"key1": {"subkey1": "value1"}}
        dict2 = {"key1": {"subkey2": "value2"}}
        result = merge_dicts(dict1, dict2)
        self.assertEqual(result, {"key1": {"subkey1": "value1", "subkey2": "value2"}})
