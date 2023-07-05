# We first import the Client from the python-binance package
from binance.client import Client
from binance.exceptions import BinanceAPIException
from binance.enums import SIDE_BUY, ORDER_TYPE_LIMIT, TIME_IN_FORCE_GTC, SIDE_SELL
import math
import time
import hft

def get_balance(client, asset):
    try:
        balance_info = client.get_asset_balance(asset=asset)
        if balance_info is not None:
            return balance_info['free'], balance_info['locked']
    except BinanceAPIException as e:
        print(f"An error occurred while fetching the balance: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None, None


class Coin:
    def __init__(self, symbol: str, client: Client):
        self.symbol = symbol
        self.client = client
        self.pairs = {}  # This dictionary will store the symbol pair info

    def get_my_trades(self, pair: str):
        # Create the symbol pair string
        symbol_pair = f"{self.symbol}{pair}"

        try:
            # Attempt to get your recent trades for this coin pair
            my_trades = self.client.get_my_trades(symbol=symbol_pair)
            return my_trades

        except BinanceAPIException as e:
            print(f"An error occurred: {e}")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        return None

    def guarantee_get_my_trades(self, pair: str):
        trades = self.get_my_trades(pair)
        while trades is None:
            trades = self.get_my_trades(pair)
        return trades

    def get_symbol_info(self, pair: str):
        symbol_pair = f"{self.symbol}{pair}"

        try:
            # Attempt to get information for this symbol pair
            symbol_info = self.client.get_symbol_info(symbol_pair)
            return symbol_info

        except BinanceAPIException as e:
            print(f"An error occurred while fetching symbol info: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return None

    def guarantee_get_symbol_info(self, pair: str):
        info = self.get_symbol_info(pair)
        while info is None:
            info = self.get_symbol_info(pair)
        return info

    def get_all_tickers(self):
        try:
            # Attempt to get all tickers
            tickers = self.client.get_all_tickers()
            return tickers

        except BinanceAPIException as e:
            print(f"An error occurred while fetching tickers: {e}")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return None

    def guarantee_get_all_tickers(self):
        tickers = self.get_all_tickers()
        while tickers is None:
            tickers = self.get_all_tickers()
        return tickers

    def add_pair(self, pair):
        try:
            # Attempt to get information for this symbol pair
            symbol_info = self.guarantee_get_symbol_info(pair)
            self.pairs[pair] = symbol_info  # Store the symbol pair info in the pairs dictionary

        except BinanceAPIException as e:
            print(f"An error occurred while fetching symbol info: {e}")

    def get_step_size(self, pair):
        try:
            # Attempt to get symbol info from the pairs dictionary
            symbol_info = self.pairs.get(pair)

            # If symbol info was found
            if symbol_info:
                # Find the step size
                for filter_info in symbol_info['filters']:
                    if filter_info['filterType'] == 'LOT_SIZE':
                        return float(filter_info['stepSize'])

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        return None

    def place_buy_limit_order(self, pair, quantity, price):
        symbol_info = self.pairs.get(pair)

        # If symbol info is not available, return early
        if symbol_info is None:
            print(f"Couldn't fetch the symbol info for {self.symbol}/{pair}")
            return

        # Get the filters for the symbol
        filters = symbol_info['filters']

        # Find the price filter and lot size filter
        price_filter = next((f for f in filters if f['filterType'] == 'PRICE_FILTER'), None)
        lot_size_filter = next((f for f in filters if f['filterType'] == 'LOT_SIZE'), None)

        # Get the tick size and step size from the filters
        tick_size = float(price_filter['tickSize'])
        step_size = float(lot_size_filter['stepSize'])

        # Calculate the number of decimal places for the tick size and step size
        tick_size_decimals = int(round(-math.log(tick_size, 10)))
        step_size_decimals = int(round(-math.log(step_size, 10)))

        # Format the price and quantity
        formatted_price = "{:0.0{}f}".format(price, tick_size_decimals)
        formatted_quantity = "{:0.0{}f}".format(quantity, step_size_decimals)

        try:
            order = self.client.create_order(
                symbol=f"{self.symbol}{pair}",
                side=SIDE_BUY,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=formatted_quantity,
                price=formatted_price
            )
            return order
        except BinanceAPIException as e:
            print(f"An error occurred while placing the order: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def place_sell_limit_order(self, pair, quantity, price):
        symbol_info = self.pairs.get(pair)

        # Get the filters for the symbol
        filters = symbol_info['filters']

        # Find the price filter and lot size filter
        price_filter = next((f for f in filters if f['filterType'] == 'PRICE_FILTER'), None)
        lot_size_filter = next((f for f in filters if f['filterType'] == 'LOT_SIZE'), None)

        # Get the tick size and step size from the filters
        tick_size = float(price_filter['tickSize'])
        step_size = float(lot_size_filter['stepSize'])

        # Calculate the number of decimal places for the tick size and step size
        tick_size_decimals = int(round(-math.log(tick_size, 10)))
        step_size_decimals = int(round(-math.log(step_size, 10)))

        # Format the price and quantity
        formatted_price = "{:0.0{}f}".format(price, tick_size_decimals)
        formatted_quantity = "{:0.0{}f}".format(quantity, step_size_decimals)

        try:
            order = self.client.create_order(
                symbol=f"{self.symbol}{pair}",
                side=SIDE_SELL,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=formatted_quantity,
                price=formatted_price
            )
            return order
        except BinanceAPIException as e:
            print(f"An error occurred while placing the order: {e}")
            return None

    def guaranteed_get_balance(self, asset):
        free_balance, locked_balance = get_balance(self.client, asset)
        while free_balance is None or locked_balance is None:
            free_balance, locked_balance = get_balance(self.client, asset)
        return float(free_balance), float(locked_balance)

    def get_open_orders(self, pair):
        try:
            open_orders = self.client.get_open_orders(symbol=f"{self.symbol}{pair}")
            return open_orders
        except BinanceAPIException as e:
            print(f"An error occurred while fetching the open orders: {e}")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return None

    def guaranteed_get_open_orders(self, pair):
        open_orders = self.get_open_orders(pair)
        while open_orders is None:
            open_orders = self.get_open_orders(pair)
        return open_orders

    def guaranteed_cancel_orders_above_threshold(self, pair, threshold):
        while True:
            open_orders = self.guaranteed_get_open_orders(pair)
            # filter the orders whose price is higher than the threshold
            high_price_orders = [order for order in open_orders if float(order['price']) > threshold]

            if len(high_price_orders) == 0:
                break  # break the loop if no high price orders are left

            for order in high_price_orders:
                try:
                    result = self.client.cancel_order(
                        symbol=f"{self.symbol}{pair}",
                        orderId=order['orderId']
                    )
                    return result
                except BinanceAPIException as e:
                    print(f"An error occurred while cancelling the order {order['orderId']}: {e}")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                return None

    def blocked_for_sell_all(self, pair, price, order_bias, qty_min, d_bar_array, k1, k2, d_bar_array_length, TIME_OUT):
        start_time = time.time()  # Get the current time
        ul, _ = self.guaranteed_get_balance(self.symbol)
        while self.place_sell_limit_order(pair, ul * order_bias, price) is None:
            print("Blocked_for_sell_all function error")
        _, l = self.guaranteed_get_balance(self.symbol)
        while l > qty_min:
            if time.time() - start_time > TIME_OUT:
                return True
            hft.get_p_reference(self, d_bar_array, k1, k2, d_bar_array_length)
            _, l = self.guaranteed_get_balance(self.symbol)
            # wait for sell orders to be filled....
        return False

    def get_avg_price(self, pair):
        try:
            ticker = self.client.get_ticker(symbol=f"{self.symbol}{pair}")
            bid_price = float(ticker['bidPrice'])
            ask_price = float(ticker['askPrice'])
            avg_price = (bid_price + ask_price) / 2
            return avg_price
        except BinanceAPIException as e:
            print(f"An error occurred while fetching the ticker: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return None

    def guaranteed_get_avg_price(self, pair):
        avg_price = self.get_avg_price(pair)
        while avg_price is None:
            avg_price = self.get_avg_price(pair)
        return avg_price

    def sell_at_market_price(self, pair, quantity):
        symbol = f"{self.symbol}{pair}"
        try:
            order = self.client.order_market_sell(symbol=symbol, quantity=quantity)
            return order
        except BinanceAPIException as e:
            print(f"An error occurred while placing the order: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return None
