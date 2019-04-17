from collections import defaultdict
from typing import List


def tree():
    return defaultdict(tree)


class Tree:
    def __init__(self):
        self.data = tree()

    def append_by_keys_path(self, keys_path, value):
        leaf = self.data
        for key in keys_path[:-1]:
            leaf = leaf[key]
        leaf.setdefault(keys_path[-1], []).append(value)


class JsonArrayValidationError(Exception):
    pass


class NestingLevelListValidationError(Exception):
    pass


class JsonArray:
    def __init__(self, data):
        self.data = data

    def validate(self):
        if not isinstance(self.data, list):
            raise JsonArrayValidationError('passing json array should be list')

        if any([not isinstance(item, dict) for item in self.data]):
            raise JsonArrayValidationError('passing json array should be list of dictionaries')

        if any([isinstance(value, dict) for item in self.data for value in item.values()]):
            raise JsonArrayValidationError('passing json array should be list of flat dictionaries')

        if len(set([tuple(sorted(item.keys())) for item in self.data])) > 1:
            raise JsonArrayValidationError('passing json array should be list of flat dictionaries with the same structure')


class NestingLevelList:
    def __init__(self, data, json_array):
        self.data = data
        self.array = json_array

    def validate(self):
        if not self.array.data and not self.data:
            return

        if not isinstance(self.data, list):
            raise NestingLevelListValidationError('passing nesting keys path should be list')

        if any([not isinstance(item, str) for item in self.data]):
            raise NestingLevelListValidationError('passing nesting keys path should be list of strings')

        if self.array.data and not self.data:
            raise NestingLevelListValidationError('passing nesting keys path is empty for non empty json array')

        if not self.array.data and self.data:
            raise NestingLevelListValidationError('passing json array is empty for non empty nesting keys path')

        array_keys = self.array.data[0].keys()

        if len(self.data) != len(set(self.data)):
            raise NestingLevelListValidationError('passing nesting keys path contains duplicate keys')

        if any([passed_key not in array_keys for passed_key in self.data]):
            raise NestingLevelListValidationError('passing nesting keys path contains not existing key')

        if len(array_keys) == len(self.data):
            raise NestingLevelListValidationError('you can`t pass all available array keys')


def nester(json_array_data: List[dict], nesting_level_list_data: List[str]):
    array = JsonArray(json_array_data)
    array.validate()

    nesting = NestingLevelList(nesting_level_list_data, array)
    nesting.validate()

    keys_path_and_value = [([array_item.pop(key) for key in nesting.data], array_item) for array_item in array.data]

    t = Tree()
    for keys_path, value in keys_path_and_value:
        t.append_by_keys_path(keys_path, value)
    return t.data
