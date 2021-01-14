from typing import Dict


def nested_dict_get(data: Dict, *path, default=None, as_type=None):
    """
    Reads data out of object, returns None if not existent
    :param data: Nested dictionary
    :param path: Path to seeked datapoint
    :param default: Default return value if path is invalid
    :param as_type: Conversion type of return value
    :return: Datapoint behind path
    """
    for key in path:
        try:
            data = data[key]
        except KeyError:
            return default
    if data is None:
        return default
    if as_type:
        return as_type(data)
    return data
