from dotenv import load_dotenv
import os
from core.coin import Coin
import time
from binance.client import Client
# Load the environment variables from the .env file
load_dotenv()

# Get the API key and secret from the environment variables
from core import utils
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

# Create an instance of the Binance client
client = Client(api_key, api_secret)

# Now you can create an instance of Coin
coin = Coin("BTC", client)
coin.add_pair("TUSD")

print(coin.guaranteed_cancel_orders_above_threshold("TUSD",30000))

