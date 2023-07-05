from dotenv import load_dotenv
import os
from core.coin import Coin
from core import utils
from core import hft
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
    ticker = client.get_ticker(symbol="BTCTUSD")
    bid_price = float(ticker['bidPrice'])
    ask_price = float(ticker['askPrice'])
    print(f'\rBidpirce: {bid_price}, Askprice : {ask_price}', end='', flush=True)
