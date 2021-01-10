from typing import Tuple
import json
from datetime import datetime


class APIObject():
    """
    An API Object can be converted to a dictionary consisting of only primitives which can then be converted
    into a JSON or directly saved to a noSQL database.
    """

    def as_dict(self: Tuple[str] = tuple([])) -> dict:
        """
        Calls static method and returns dictionary that represents current instance
        :param ignore_keys: List of keys that will be ignored when converting instance to dictionary
        :return: Instance as dict
        """
        return APIObject.to_dict(self)

    def json(self, ignore_keys: Tuple[str] = tuple([])) -> str:
        """
        Create string representation of current instance that can be sent as JSON object
        :param ignore_keys: List of keys that will be ignored when converting instance to dictionary
        :return: instance as dict
        """
        return json.dumps(
            self.to_dict(self, ignore_keys=ignore_keys),
            sort_keys=False,
            indent=4
        )

    def __getitem__(self, name: str) -> any:
        """
        Allows accessing properties of the instance using []-syntax
        :param name: Name of property that shall be accessed
        :return: The value behind 'name'
        """
        return getattr(self, name)

    @staticmethod
    def to_dict(obj, ignore_keys=tuple([]), date_format="%Y-%m-%d"):
        """
        Converts an instance of any class into a dictionary recursively. Private attributes, whose name starting with
        an underscore, are ignored. Further, the key names specified under "ignore_keys" are also not being considered.
        Datees are converted into strins following the specified syntax.
        :param obj: Any object that shall be converted to a dictionary
        :param ignore_keys:
        :param date_format:
        :return:
        """
        recall = lambda o: APIObject.to_dict(o, ignore_keys=ignore_keys, date_format=date_format)
        valid_entry = lambda k, v: not callable(v) and not k.startswith('_') and k not in ignore_keys
        # Convert dates to strings
        if isinstance(obj, datetime):
            return obj.strftime(date_format)
        # Convert class objects
        if hasattr(obj, "__dict__"):
            return dict([(key, recall(value)) for key, value in obj.__dict__.items() if valid_entry(key, value)])
        # Convert objects
        if isinstance(obj, dict):
            return dict([(key, recall(value)) for key, value in obj.items() if valid_entry(key, value)])
        # Convert abstract syntax trees
        if hasattr(obj, "_ast"):
            return recall(obj._ast())
        # Convert Iterables
        if hasattr(obj, "__iter__") and not isinstance(obj, str):
            return [recall(v) for v in obj]
        # Base case
        return obj
