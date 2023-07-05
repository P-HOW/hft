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
    qty_min = float(os.getenv('QTY_BTC_MIN'))  # this is for BTC_min
    qty_TUSD_min = float(os.getenv('QTY_TUSD_MIN'))
    time_out_for_stop_losses = int(os.getenv('TIME_OUT_FOR_STOP_LOSSES'))
    stop_loss_time = int(os.getenv('STOP_LOSS_DURATION'))
    stop_loss_rounds = int(os.getenv('STOP_LOSS_ROUNDS'))
    stop_loss_orders = int(os.getenv('STOP_LOSS_ORDERS'))
    half_deviation = deviation / 2
    double_deviation = deviation * 2
    two_thirds_deviation = deviation * 2 / 3
    client = Client(api_key, api_secret)
    coin = Coin("BTC", client)
    coin.add_pair("TUSD")
    last_buy = 0
    d_bar_array = []

coin.sell_at_market_price("TUSD", 0.00196)
