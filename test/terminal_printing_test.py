import time
from colorama import Fore, Back, Style, init

init()

# Initialize data outside of function
data = {
    "Trading Time": [],
    "24h Trading Volume": [],
    "Accumulated Rewards": [],
    "Number of Stop-Loss Calls": []
}

def print_header():
    # Set fixed width for all columns
    fixed_width = 20

    # Define color for each column
    colors = {
        "Trading Time": Fore.CYAN,
        "24h Trading Volume": Fore.MAGENTA,
        "Accumulated Rewards": Fore.GREEN,
        "Number of Stop-Loss Calls": Fore.RED
    }

    # Get max width for each column
    widths = {
        key: max(fixed_width, max(len(v) for v in values))
        for key, values in data.items()
    }

    # Print header
    header = "| " + " | ".join(f"{key:<{widths[key]}}" for key in data.keys()) + " |"
    print(header)
    print("|" + "-" * (len(header) - 2) + "|")

def update_table(trading_time, trading_volume, accumulated_rewards, num_stop_loss_calls):
    # Convert time to standard form
    standard_time = time.strftime('%H:%M:%S', time.gmtime(trading_time))

    # Append new entries to data
    data["Trading Time"].append(standard_time)
    data["24h Trading Volume"].append(f"${trading_volume}")
    data["Accumulated Rewards"].append(f"${accumulated_rewards}")
    data["Number of Stop-Loss Calls"].append(f"{num_stop_loss_calls} times")

    # Set fixed width for all columns
    fixed_width = 20

    # Define color for each column
    colors = {
        "Trading Time": Fore.CYAN,
        "24h Trading Volume": Fore.MAGENTA,
        "Accumulated Rewards": Fore.GREEN,
        "Number of Stop-Loss Calls": Fore.RED
    }

    # Get max width for each column
    widths = {
        key: max(fixed_width, max(len(v) for v in values))
        for key, values in data.items()
    }

    # Print row for last entry in data
    row = "| " + " | ".join(
        f"{colors[key]}{value[-1]:<{widths[key]}}"
        for key, value in data.items()
    ) + Style.RESET_ALL + " |"
    print(row)

# Testing the function
print_header()
update_table(3600, 100, 1000, 1)
time.sleep(1)  # delay for 1 second
update_table(3660, 200, 2000, 2)
