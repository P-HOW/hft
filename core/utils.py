import time


def match_trade_data(usdt_trades, tusd_trades):
    # Convert the lists into dictionaries with time as the key
    usdt_dict = {trade['time']: trade['price'] for trade in usdt_trades}
    tusd_dict = {trade['time']: trade['price'] for trade in tusd_trades}

    # Find the common times
    common_times = set(usdt_dict.keys()) & set(tusd_dict.keys())

    # Create a new list of trade data with prices from both pairs at the same time
    matched_trades = [{'time': time, 'usdt_price': usdt_dict[time], 'tusd_price': tusd_dict[time]} for time in
                      common_times]

    # Sort the list by time
    matched_trades.sort(key=lambda trade: trade['time'])

    return matched_trades


def find_pair_price_from_tickers(prices, pair):
    pair_price = None

    # Iterate over the prices data
    for item in prices:
        # If the symbol is "BTCUSDT", save the price and break the loop
        if item['symbol'] == pair:
            pair_price = item['price']
            break

    # Check if we found the price
    return pair_price


def summarize_24h_volume(my_trades):
    current_time = int(time.time() * 1000)

    # Calculate 24 hours ago (in milliseconds)
    twenty_four_hours_ago = current_time - 24 * 60 * 60 * 1000

    # Calculate your trading volume in the last 24 hours
    volume = sum(float(trade['quoteQty']) for trade in my_trades if trade['time'] > twenty_four_hours_ago)

    return volume


def check_price(p, last_buy, price_drop, price_increase):
    return (p - last_buy < price_drop) or (p - last_buy > price_increase)
