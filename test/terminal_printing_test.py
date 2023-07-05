import curses
import time

# Initial values
values = {
    "Var1": "Hello",
    "Var2": "World",
    "Var3": "PrettyTable",
}


def print_table(stdscr):
    for i in range(5):  # update table for 5 seconds
        # Update values
        values["Var1"] = f"Hola {i}"
        values["Var2"] = f"Mundo {i}"
        values["Var3"] = f"PrettyTable ES {i}"

        stdscr.clear()
        stdscr.addstr(0, 0, "Variable Name | Value")
        for idx, (var, value) in enumerate(values.items(), start=1):
            stdscr.addstr(idx, 0, f"{var}          | {value}")

        stdscr.refresh()
        time.sleep(1)


curses.wrapper(print_table)





