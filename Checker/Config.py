# -*- coding: utf-8 -*-
import json
import os


def deep_update(original, update):
    for key, value in original.items():
        if key not in update:
            update[key] = value
        elif isinstance(value, dict):
            deep_update(value, update[key])
    return update


class Config(dict):

    def __init__(self, base_url):
        data = self._read_config(os.path.join(base_url, 'config.json'))
        self.update(data)

    @staticmethod
    def _read_config(file_name):
        data = {}
        try:
            with open(file_name, encoding='utf-8') as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            pass

        return data

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)
