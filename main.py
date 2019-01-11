from src import APIObject


class TestAPIObject(APIObject):

    def __init__(self):
        self.visible_value = 1
        self._invisible_value = 2


if __name__ == "__main__":
    t = TestAPIObject()
    print(t.json())
