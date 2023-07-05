import math

from dotenv import load_dotenv
import os
from core.coin import Coin
from core import utils
from binance.client import Client
import statistics
from tqdm import tqdm
import time


def get_p_reference(coin, d_bar_array, k1, k2, d_bar_array_length):
    prices = coin.guarantee_get_all_tickers()
    p2 = coin.guaranteed_get_avg_price("USDT")
    p3 = coin.guaranteed_get_avg_price("TUSD")
    p1 = float(utils.find_pair_price_from_tickers(prices, "TUSDUSDT"))
    p3_star = float(p2 / p1)
    d_bar_array.append(p3 - p2)
    if len(d_bar_array) > d_bar_array_length:
        d_bar_array.pop(0)
    d_bar = statistics.mean(d_bar_array)
    p3_bar = p2 + d_bar
    return p3_bar * k1 + p3_star * k2, p3


def initialize_d_bar_array(coin, d_bar_array, k1, k2, d_bar_array_length):
    for _ in tqdm(range(d_bar_array_length), desc="Initializing d_bar_array"):
        get_p_reference(coin, d_bar_array, k1, k2, d_bar_array_length)


def place_BTC_buyorder_once(coin, pair, d_bar_array, k1, k2, d_bar_array_length, order_bias, deviation, minqty):
    ul, _ = coin.guaranteed_get_balance(pair)

    p, p3 = get_p_reference(coin, d_bar_array, k1, k2, d_bar_array_length)

    if ul > minqty:
        coin.place_buy_limit_order(pair, ul * order_bias / (p - deviation), p - deviation)

    return p - deviation


def wait_for_pending_BTC_orders(min_qty, coin, d_bar_array, k1, k2, d_bar_array_length, TIME_OUT):
    start_time = time.time()  # Get the current time
    _, l = coin.guaranteed_get_balance("BTC")
    while l > min_qty:
        if time.time() - start_time > TIME_OUT:
            print("Time limit exceeded, exiting function")
            return True
        get_p_reference(coin, d_bar_array, k1, k2, d_bar_array_length)
        _, l = coin.guaranteed_get_balance("BTC")
    return False


def place_stop_loss_orders(coin, pair, n_orders, last_buy_price, current_price, d_bar_array, k1, k2, d_bar_array_length,
                           minBTC, fault_tolerance, step_size, TIME_OUT):
    start_time = time.time()  # Get the current time
    ul, _ = coin.guaranteed_get_balance("BTC")
    price_decrement = (last_buy_price - current_price) / n_orders
    if ul < minBTC:
        return True
    if current_price >= last_buy_price or price_decrement <= step_size:
        count = 0
        while coin.sell_at_market_price is None and count < fault_tolerance:
            count = count + 1
            get_p_reference(coin, d_bar_array, k1, k2, d_bar_array_length)
        return True
    # Calculate the price increment for each order

    # Calculate the quantity for each order. Here, I'm just using a placeholder value.
    # You should replace this with the actual logic for calculating the order quantity.
    quantity = ul
    n_orders = min(n_orders, math.floor(ul/minBTC)-1)
    # Place the orders
    for i in range(n_orders):
        limit_price = last_buy_price - (i * price_decrement)
        coin.place_sell_limit_order(pair, quantity, limit_price)
    _, l = coin.guaranteed_get_balance("BTC")
    while l > minBTC:
        _, l = coin.guaranteed_get_balance("BTC")
        if time.time() - start_time > TIME_OUT:
            return False
    return True


def stop_loss_thread(coin, pair, n_orders, last_buy_price, current_price, n_rounds, stop_loss_time, d_bar_array, k1, k2,
                     d_bar_array_length, minBTC):
    step_size = coin.get_step_size("TUSD")
    fault_tolerance = 10
    sleep_time = stop_loss_time / n_rounds
    for _ in range(n_rounds):
        coin.guaranteed_cancel_orders_above_threshold(pair, 0)

        if place_stop_loss_orders(coin, pair, n_orders, last_buy_price, current_price, d_bar_array, k1, k2,
                               d_bar_array_length,
                               minBTC, fault_tolerance, step_size, sleep_time):
            return

    count = 0
    while coin.sell_at_market_price is None and count < fault_tolerance:
        count = count + 1
        get_p_reference(coin, d_bar_array, k1, k2, d_bar_array_length)

