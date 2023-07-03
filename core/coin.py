# We first import the Client from the python-binance package
from binance.client import Client
from binance.exceptions import BinanceAPIException


class Coin:
    def __init__(self, symbol: str, client: Client):
        self.symbol = symbol
        self.client = client

    def get_my_trades(self, pair: str):
        # Create the symbol pair string
        symbol_pair = f"{self.symbol}{pair}"

        try:
            # Attempt to get your recent trades for this coin pair
            my_trades = self.client.get_my_trades(symbol=symbol_pair)
            return my_trades

        except BinanceAPIException as e:
            print(f"An error occurred: {e}")
            return None

    def guarantee_get_my_trades(self, pair: str):
        trades = self.get_my_trades(pair)
        while trades is None:
            trades = self.get_my_trades(pair)
        return trades

    def get_symbol_info(self, pair:str):
        symbol_pair = f"{self.symbol}{self.pair}"

        try:
            # Attempt to get information for this symbol pair
            symbol_info = self.client.get_symbol_info(symbol_pair)
            return symbol_info

        except BinanceAPIException as e:
            print(f"An error occurred while fetching symbol info: {e}")
            return None

    def guarantee_get_symbol_info(self, pair: str):
        info = self.get_symbol_info(pair)
        while info is None:
            info = self.get_symbol_info(pair)
        return info

