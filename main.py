# This is a sample Python script.
import time

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from dotenv import load_dotenv
import os
from core.coin import Coin
from core import utils
from binance.client import Client
import statistics
from core import hft

if __name__ == '__main__':
    # Load the environment variables from the .env file
    load_dotenv()

    # Get the environment variables
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")
    k1 = float(os.getenv('K1'))
    k2 = float(os.getenv('K2'))
    d_bar_array_length = int(os.getenv('D_BAR_ARRAY_LENGTH'))
    deviation = float(os.getenv('DEVIATION'))
    order_bias = float(os.getenv('ORDER_BIAS'))
    qty_min = float(os.getenv('QTY_MIN'))  # this is for BTC_min
    qty_TUSD_min = float(os.getenv('QTY_TUSD_MIN'))
    time_out_for_stop_losses = int(os.getenv('TIME_OUT_FOR_STOP_LOSSES'))

    half_deviation = deviation / 2
    double_deviation = deviation * 2
    two_thirds_deviation = deviation * 2 / 3
    client = Client(api_key, api_secret)
    coin = Coin("BTC", client)
    coin.add_pair("TUSD")
    last_buy = 0
    d_bar_array = []
    hft.initialize_d_bar_array(coin, d_bar_array, k1, k2, d_bar_array_length)

    last_buy = hft.place_BTC_buyorder_once(coin, "TUSD", d_bar_array, k1, k2, d_bar_array_length, order_bias, deviation,
                                           qty_TUSD_min)

    while True:
        last_buy = hft.place_BTC_buyorder_once(coin, "TUSD", d_bar_array, k1, k2, d_bar_array_length, order_bias,
                                               deviation,
                                               qty_TUSD_min)

        # first, we need to check if the orders have been filled.
        ul, l = coin.guaranteed_get_balance("BTC")
        if l > qty_min:
            if hft.wait_for_pending_BTC_orders(qty_min, coin, d_bar_array, k1, k2, d_bar_array_length, time_out_for_stop_losses):
                "We need to place stop losses function there"

        if ul > qty_min:
            coin.blocked_for_sell_all("TUSD", last_buy + two_thirds_deviation, order_bias, qty_min, d_bar_array, k1, k2, d_bar_array_length, time_out_for_stop_losses)

        p, p3 = hft.get_p_reference(coin, d_bar_array, k1, k2, d_bar_array_length)

        if utils.check_price(p, last_buy,two_thirds_deviation, double_deviation):

            coin.guaranteed_cancel_orders_above_threshold("TUSD", 0)

            ul, _ = coin.guaranteed_get_balance("BTC")
            if ul > qty_min:
                coin.blocked_for_sell_all("TUSD", last_buy + two_thirds_deviation, order_bias, qty_min, d_bar_array, k1,
                                          k2, d_bar_array_length, time_out_for_stop_losses)

            last_buy = hft.place_BTC_buyorder_once(coin, "TUSD", d_bar_array, k1, k2, d_bar_array_length, order_bias,
                                                   deviation,
                                                   qty_TUSD_min)
