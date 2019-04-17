import unittest  # using this standart test module to have possibility to take out app/nest.py and this tests file from this project and everything will work

from app.nest import (JsonArray,
                      JsonArrayValidationError,
                      NestingLevelList,
                      NestingLevelListValidationError,
                      Tree,
                      nester)


class TestTreeAppendByKeysPath(unittest.TestCase):
    def setUp(self):
        self.tree = Tree()

    def test_passing_single_item_keys_path(self):
        self.tree.append_by_keys_path(['key'], 'value')
        self.assertEqual(self.tree.data['key'], ['value'])

    def test_passing_not_single_item_keys_path(self):
        self.tree.append_by_keys_path(['key1', 'key2'], 'value')
        self.assertEqual(self.tree.data['key1']['key2'], ['value'])

    def test_appending_value_by_the_same_keys_path(self):
        self.tree.append_by_keys_path(['key1', 'key2'], 'value1')
        self.tree.append_by_keys_path(['key1', 'key2'], 'value2')
        self.assertEqual(self.tree.data['key1']['key2'], ['value1', 'value2'])

    def test_passing_keys_path_containing_equal_keys(self):
        self.tree.append_by_keys_path(['key', 'key'], 'value')
        self.assertEqual(self.tree.data['key']['key'], ['value'])


class TestJsonArrayValidation(unittest.TestCase):
    def test_passing_not_list_of_dicts(self):
        array = JsonArray({})
        with self.assertRaises(JsonArrayValidationError) as err:
            array.validate()
        self.assertEqual(str(err.exception), 'passing json array should be list')

    def test_passing_list_of_not_dicts(self):
        array = JsonArray([{'i-am': 'dict'}, ['i-am-not-dict']])
        with self.assertRaises(JsonArrayValidationError) as err:
            array.validate()
        self.assertEqual(str(err.exception), 'passing json array should be list of dictionaries')

    def test_passing_list_of_not_flat_dicts(self):
        array = JsonArray([{'i-am': 'flat-dict'}, {'i-am': {'not': 'flat-dict'}}])
        with self.assertRaises(JsonArrayValidationError) as err:
            array.validate()
        self.assertEqual(str(err.exception), 'passing json array should be list of flat dictionaries')

    def test_passing_list_of_dicts_with_not_the_same_structure(self):
        array = JsonArray([{'i-have': 'this-structure'}, {'i-have': 'too', 'but': 'except-this'}])
        with self.assertRaises(JsonArrayValidationError) as err:
            array.validate()
        self.assertEqual(str(err.exception), 'passing json array should be list of flat dictionaries with the same structure')

    def test_passing_empty_list(self):
        array = JsonArray([])
        array.validate()

    def test_passing_valid_data(self):
        array = JsonArray([{'i-am': 'valid'}, {'i-am': 'too'}])
        array.validate()


class TestNestingLevelListValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.json_array = JsonArray([{'key1': '11', 'key2': '12', 'key3': '13'}, {'key1': '21', 'key2': '22', 'key3': '23'}])

    def test_passing_not_list(self):
        nesting = NestingLevelList({}, self.json_array)
        with self.assertRaises(NestingLevelListValidationError) as err:
            nesting.validate()
        self.assertEqual(str(err.exception), 'passing nesting keys path should be list')

    def test_passing_not_list_of_strings(self):
        nesting = NestingLevelList(['string', {'not': 'string'}], self.json_array)
        with self.assertRaises(NestingLevelListValidationError) as err:
            nesting.validate()
        self.assertEqual(str(err.exception), 'passing nesting keys path should be list of strings')

    def test_passing_with_empty_json_array(self):
        nesting = NestingLevelList(['key1', 'key2'], JsonArray([]))
        with self.assertRaises(NestingLevelListValidationError) as err:
            nesting.validate()
        self.assertEqual(str(err.exception), 'passing json array is empty for non empty nesting keys path')

    def test_passing_empty_list_with_empty_json_array(self):
        nesting = NestingLevelList([], JsonArray([]))
        nesting.validate()

    def test_passing_empty_list_with_non_empty_json_array(self):
        nesting = NestingLevelList([], JsonArray([{'key': 'value'}]))
        with self.assertRaises(NestingLevelListValidationError) as err:
            nesting.validate()
        self.assertEqual(str(err.exception), 'passing nesting keys path is empty for non empty json array')

    def test_passing_key_not_existing_in_json_array(self):
        nesting = NestingLevelList(['key1', 'not-existing-key'], self.json_array)
        with self.assertRaises(NestingLevelListValidationError) as err:
            nesting.validate()
        self.assertEqual(str(err.exception), 'passing nesting keys path contains not existing key')

    def test_passing_the_same_key_multiple_times(self):
        nesting = NestingLevelList(['key1', 'key2', 'key1'], self.json_array)
        with self.assertRaises(NestingLevelListValidationError) as err:
            nesting.validate()
        self.assertEqual(str(err.exception), 'passing nesting keys path contains duplicate keys')

    def test_passing_all_json_array_item_keys(self):
        nesting = NestingLevelList(['key1', 'key3', 'key2'], self.json_array)
        with self.assertRaises(NestingLevelListValidationError) as err:
            nesting.validate()
        self.assertEqual(str(err.exception), 'you can`t pass all available array keys')

    def test_passing_empty_list(self):
        nesting = NestingLevelList([], JsonArray([]))
        nesting.validate()

    def test_passing_one_existing_key(self):
        nesting = NestingLevelList(['key3'], self.json_array)
        nesting.validate()

    def test_passing_multiple_valid_existing_keys(self):
        nesting = NestingLevelList(['key3', 'key2'], self.json_array)
        nesting.validate()


class TestNester(unittest.TestCase):
    def test_passing_empty_nesting_for_empty_array(self):
        self.assertEqual(nester([], []), {})

    def test_passing_empty_nesting_for_non_empty_array(self):
        with self.assertRaises(NestingLevelListValidationError) as err:
            nester([{'key': 'value'}], [])
        self.assertEqual(str(err.exception), 'passing nesting keys path is empty for non empty json array')

    def test_nesting_by_single_key_with_unique_values(self):
        json_array_data = [{'key1': 1, 'key2': 2}, {'key1': 3, 'key2': 4}]
        nesting_key_path_data = ['key1']
        actual = nester(json_array_data, nesting_key_path_data)
        expected = {1: [{'key2': 2}], 3: [{'key2': 4}]}
        self.assertDictEqual(actual, expected)

    def test_nesting_by_single_key_with_repeated_values(self):
        json_array_data = [{'key1': 1, 'key2': 2}, {'key1': 1, 'key2': 4}, {'key1': 11, 'key2': 3}]
        nesting_key_path_data = ['key1']
        actual = nester(json_array_data, nesting_key_path_data)
        expected = {1: [{'key2': 2}, {'key2': 4}], 11: [{'key2': 3}]}
        self.assertDictEqual(actual, expected)

    def test_nesting_by_multiple_key_path_with_unique_values(self):
        json_array_data = [{'key1': '1', 'key2': '2', 'key3': '3'}, {'key1': '4', 'key2': '5', 'key3': '6'}]
        nesting_key_path_data = ['key2', 'key1']
        actual = nester(json_array_data, nesting_key_path_data)
        expected = {'2': {'1': [{'key3': '3'}]}, '5': {'4': [{'key3': '6'}]}}
        self.assertDictEqual(actual, expected)

    def test_nesting_by_multiple_key_path_with_repeated_values(self):
        json_array_data = [
            {'key1': '1', 'key2': '2', 'key3': '3'},
            {'key1': '4', 'key2': '5', 'key3': '6'},
            {'key1': '4', 'key2': '5', 'key3': '7'},
        ]
        nesting_key_path_data = ['key2', 'key1']
        actual = nester(json_array_data, nesting_key_path_data)
        expected = {'2': {'1': [{'key3': '3'}]}, '5': {'4': [{'key3': '6'}, {'key3': '7'}]}}
        self.assertDictEqual(actual, expected)

    def test_pass_invalid_keys_path(self):
        json_array_data = [{'key': 1}, {'key': 22}]
        nesting_key_path_data = ['not-existing-key']
        with self.assertRaises(NestingLevelListValidationError):
            nester(json_array_data, nesting_key_path_data)

    def test_pass_invalid_json_array(self):
        json_array_data = [{'key': 1}, {'key': 22, 'different-structure': 2}]
        nesting_key_path_data = ['key']
        with self.assertRaises(JsonArrayValidationError):
            nester(json_array_data, nesting_key_path_data)
