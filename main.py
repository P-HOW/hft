# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from dotenv import load_dotenv
import os
from core.coin import Coin
from core import utils
from binance.client import Client
import statistics


if __name__ == '__main__':
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


