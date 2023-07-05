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

my_trades = coin.get_my_trades("TUSD")
#my_trades = []
print(utils.summarize_24h_volume(my_trades))
# Get the current time (in milliseconds)
#avg_price = client.get_avg_price(symbol='BTCUSDT')
#print(avg_price)
#print(f"Your 24-hour trading volume for BTCTUSD: {volume} TUSD")
#status = client.get_account_api_trading_status()
#print (status)