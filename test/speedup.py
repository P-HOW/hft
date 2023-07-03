from dotenv import load_dotenv
import os
from core.coin import Coin
import time
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
start_time_segment_2 = time.time()

# ... (your second segment of code here) ...
prices = client.get_all_tickers()
# Measure the end time of the second segment
end_time_segment_2 = time.time()

# Calculate the elapsed time for the second segment
elapsed_time_segment_2 = end_time_segment_2 - start_time_segment_2

print(f"Time elapsed in segment 2: {elapsed_time_segment_2} seconds")
start_time_segment_1 = time.time()
#info = client.get_symbol_info('BTCUSDT')
#depth1 = client.get_order_book(symbol='BTCUSDT')
#depth2 = client.get_order_book(symbol='BTCTUSD')
avg_price = client.get_avg_price(symbol='BTCUSDT')
avg_price = client.get_avg_price(symbol='BTCTUSD')
end_time_segment_1 = time.time()
elapsed_time_segment_1 = end_time_segment_1 - start_time_segment_1

print(f"Time elapsed in segment 1: {elapsed_time_segment_1} seconds")

