from dotenv import load_dotenv
import os
from core.coin import Coin
from core import utils
from binance.client import Client
import statistics
# Load the environment variables from the .env file
load_dotenv()

# Get the API key and secret from the environment variables
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

# Create an instance of the Binance client
client = Client(api_key, api_secret)

# Now you can create an instance of Coin
coin = Coin("BTC", client)
d_bar_array = []
while True:
    prices = client.get_all_tickers()
    p2 = float(utils.find_pair_price_from_tickers(prices,"BTCUSDT"))
    p3 = float(utils.find_pair_price_from_tickers(prices,"BTCTUSD"))
    p1 = float(utils.find_pair_price_from_tickers(prices,"TUSDUSDT"))
    p3_star = float(p2/p1)
    t_bar = (1/p1-1)*p2
    d_bar_array.append(p3-p2)
    if len(d_bar_array) > 100:
        d_bar_array.pop(0)
    d_bar = statistics.mean(d_bar_array)
    p3_bar = p2+d_bar
    print(f'\rBTCTUSD star price: {p3_star}, BTCTUSD bar price: {p3_bar}, dBarLength : {len(d_bar_array)}', end='', flush=True)
