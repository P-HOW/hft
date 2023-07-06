from dotenv import load_dotenv
import os

from core import coin
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
coin = coin.Coin("BTC", client)
coin.add_pair("TUSD")
my_trades = coin.get_my_trades("TUSD")
#coin.sell_at_market_price("TUSD", 0.0147)
#my_trades = []
print(utils.summarize_24h_volume(my_trades))
#coin.guaranteed_cancel_orders_above_threshold("TUSD", 0)
#print(coin.get_last_buy_average_price("TUSD"))
#coin.guaranteed_cancel_all_open_orders("TUSD")
# Get the current time (in milliseconds)
#avg_price = client.get_avg_price(symbol='BTCUSDT')
#print(avg_price)
#print(f"Your 24-hour trading volume for BTCTUSD: {volume} TUSD")
#status = client.get_account_api_trading_status()
#print (status)