from .APIObject import APIObject


class APICoin(APIObject):

    def __init__(self, coin_id, coin_name, coin_symbol):
        self.coin_id = coin_id
        self.coin_name = coin_name
        self.coin_symbol = coin_symbol

    def objectid(self):
        return self.coin_id
