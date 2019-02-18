from src import APICoin


class TestCoinInfo(APICoin):

    def __init__(self):
        super().__init__("test-id", "Testcoin", "TST")
        self.visible_value = 1
        self._invisible_value = 2


if __name__ == "__main__":
    t = TestCoinInfo()
    print(t.json())

    t.save()
    tc = TestCoinInfo.load("test-id")
    print(tc.json())

