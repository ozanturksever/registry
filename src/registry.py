#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
import copy

class Registry(object):
    def __init__(self, initial_values = {}):
        self.__cached_values = initial_values

    def get(self, key, values=None):
        if not values:
            values = self.__cached_values

        key_levels = self.extract_key(key)
        last_level = len(key_levels)-1
        for level in xrange(len(key_levels)):
            _key = key_levels[level]
            value = values.get(_key)
            if level == last_level:
                return copy.copy(value)
            if value and isinstance(value, dict):
                return self.get('.'.join(key_levels[1:]), value)
            else:
                return copy.copy(value)

    def set(self, key, value, values=None):
        if not values and not isinstance(values, dict):
            values = self.__cached_values

        key_levels = self.extract_key(key)
        last_level = len(key_levels)-1
        for level in xrange(len(key_levels)):
            _key = key_levels[level]
            _value = values.get(_key)
            if level == last_level:
                values[_key] = value
                return
            if _value and isinstance(_value, dict):
                return self.set('.'.join(key_levels[1:]), value, _value)
            else:
                values[_key] = {}
                return self.set('.'.join(key_levels[1:]), value, values[_key])

    def is_nasted(self, key):
        return len(self.extract_key(key)) > 1

    def extract_key(self, key):
        if not key:
            return []
        return key.split('.')

    def get_values(self):
        return self.__cached_values

    def set_values(self, values):
        self.__cached_values = copy.copy(values)

