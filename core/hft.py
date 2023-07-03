from dotenv import load_dotenv
import os
from core.coin import Coin
from core import utils
from binance.client import Client
import statistics
def get_p_reference(coin,d_bar_array):
    # Load the environment variables from the .env file
    load_dotenv()

    # Access the environment variables K1 and K2
    k1 = float(os.getenv('K1'))
    k2 = float(os.getenv('K2'))

    prices = coin.guarantee_get_all_tickers()
    p2 = float(utils.find_pair_price_from_tickers(prices, "BTCUSDT"))
    p3 = float(utils.find_pair_price_from_tickers(prices, "BTCTUSD"))
    p1 = float(utils.find_pair_price_from_tickers(prices, "TUSDUSDT"))
    p3_star = float(p2 / p1)
    d_bar_array.append(p3 - p2)
    if len(d_bar_array) > 100:
        d_bar_array.pop(0)
    d_bar = statistics.mean(d_bar_array)
    p3_bar = p2 + d_bar
    return p3_bar*k1+p3_star*k2