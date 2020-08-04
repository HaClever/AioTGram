# -*- coding: utf-8 -*-

"""
Module contains abstract base classes for all types.

Classes:
- Dictionaryable
- JsonSerializable
- JsonDeserializable
"""

try:
    import ujson as json
except ImportError:
    import json

from abc import ABCMeta, abstractmethod


class Dictionaryable(metaclass=ABCMeta):
    @abstractmethod
    def to_dict(self):
        pass


class JsonSerializable(metaclass=ABCMeta):
    @abstractmethod
    def to_json(self):
        pass


class JsonDeserializable(metaclass=ABCMeta):
    """
    Subclasses of this class are guaranteed to be able to be created from a json-style dict or json formatted string.
    All subclasses of this class must override de_json.
    """

    @classmethod
    def de_json(cls, json_string):
        """
        Returns an instance of this class from the given json dict or string.
        This function must be overridden by subclasses.
        :return: an instance of this class created from the given json dict or string.
        """
        raise NotImplementedError

    @staticmethod
    def check_json(json_type):
        """
        Checks whether json_type is a dict or a string. If it is already a dict, it is returned as-is.
        If it is not, it is converted to a dict by means of json.loads(json_type)
        :param json_type:
        :return:
        """
        if isinstance(json_type, dict):
            return json_type
        elif isinstance(json_type, str):
            return json.loads(json_type)
        else:
            raise ValueError("json_type should be a json dict or string.")

    def __str__(self):
        dict_ = {}
        for key, val in iter(self.__dict__.items()):
            if hasattr(val, '__dict__'):
                dict_[key] = val.__dict__
            else:
                dict_[key] = val

        return str(dict_)
