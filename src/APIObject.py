from typing import Tuple
import json
from datetime import datetime
import pickle
import os


class APIObject():
    """
    An API Object can be converted to a dictionary consisting of only primitives which can then be converted
    into a JSON or directly saved to a noSQL database.
    """

    basepath = ".savedata"
    static = ".data"

    def objectid(self):
        return "default"

    def _save_path(self):
        classname = self.__class__.__name__.lower()
        object_id = self.objectid()
        head, tail = os.path.normpath(f"./{self.basepath}/{classname}"), os.path.normpath(f"{object_id}.pickle")
        return head, tail, os.path.join(head, tail)

    def save(self):
        head, tail, save_path = self._save_path()
        if not os.path.exists(head):
            os.makedirs(head)
        with open(save_path, 'wb') as handle:
            pickle.dump(self, handle, protocol=pickle.HIGHEST_PROTOCOL)

    @classmethod
    def load(cls, object_id):
        classname = cls.__name__.lower()
        picklepath = f"./{cls.basepath}/{classname}/{object_id}.pickle"
        with open(picklepath, 'rb') as handle:
            return pickle.load(handle)

    def as_dict(self, ignore_keys=tuple([]), date_format="%Y-%m-%d") -> dict:
        """
        Converts an instance of any class into a dictionary recursively. Private attributes, whose name starting with
        an underscore, are ignored. Further, the key names specified under "ignore_keys" are also not being considered.
        Dates are converted into strins following the specified syntax.
        :param ignore_keys: Keys that shall be ignored during conversion
        :param date_format: String format into which dates shall be converted
        """
        return APIObject.to_dict(self, ignore_keys=ignore_keys, date_format=date_format, stop_recursion=True)

    def json(self, ignore_keys: Tuple[str] = tuple([]), date_format="%Y-%m-%d") -> str:
        """
        Create string representation of current instance that can be sent as JSON object
        :param ignore_keys: List of keys that will be ignored when converting instance to dictionary
        :param date_format: String format into which dates shall be converted
        :return: instance as json string
        """
        return json.dumps(
            self.as_dict(ignore_keys=ignore_keys, date_format=date_format),
            sort_keys=False,
            indent=4,
        )

    def __getitem__(self, name: str) -> any:
        """
        Allows accessing properties of the instance using []-syntax
        :param name: Name of property that shall be accessed
        :return: The value behind 'name'
        """
        return getattr(self, name)

    @staticmethod
    def to_dict(obj, ignore_keys=tuple([]), date_format="%Y-%m-%d", stop_recursion=False):
        """
        Converts an instance of any class into a dictionary recursively. Private attributes, whose name starting with
        an underscore, are ignored. Further, the key names specified under "ignore_keys" are also not being considered.
        Datees are converted into strins following the specified syntax.
        :param obj: Any object that shall be converted to a dictionary
        :param ignore_keys: Keys that shall be ignored during conversion
        :param date_format: String format into which dates shall be converted
        :param stop_recursion: Indicates that call to .json() shall be made prevented due to recursion
        :return:
        """
        recall = lambda o: APIObject.to_dict(o, ignore_keys=ignore_keys, date_format=date_format)
        valid_entry = lambda k, v: not callable(v) and not k.startswith('_') and k not in ignore_keys
        # Call .json() for APIObjects
        if not stop_recursion and isinstance(obj, APIObject):
            return obj.as_dict(ignore_keys=ignore_keys, date_format=date_format)
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
        if isinstance(obj, str):
            return json.dumps(obj)[1:-1]
        # Base case
        return obj
