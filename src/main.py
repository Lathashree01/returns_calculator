"""
Returns Calculator:
Script to calculate the maximum returns possible by trading currencies for over a year
For more details, please refer to the README.md file and design document.
"""

import sys
import logging
import json
import os
import numpy as np


# Check if the root logger has handlers
if not logging.root.handlers:
    logging.basicConfig(
        filename=os.getenv("LOGGER_FILE", "app.log"),
        level=logging.DEBUG,
        format=os.getenv("LOGGER_FORMAT", "%(asctime)s - %(levelname)s - %(message)s"),
    )


def load_data(input_filename: str) -> np.ndarray:
    """
    Load monthly returns data from a text file.

    Args:
        input_filename (str): The name of the file to be loaded

    Returns:
        monthly_returns_arr (p.ndarray): 3D numpy array of monthly returns

    Raises:
        FileNotFoundError: If the file is not found in the `data/` location
        json.JSONDecodeError: If there is any error while parsing the JSON-like content
        Exception: If there is any other error while reading the file
    """

    try:
        # Read the file content
        data_folder = os.getenv("DATA_FOLDER", "./data/")
        with open(data_folder + input_filename, "r", encoding="utf-8") as file:
            file_content = file.read()
            # Parse the JSON-like content
            data = json.loads(file_content)
            monthly_returns_arr = np.array(data)

            # Check for datashape : 12,4,4 else print error and exit
            if monthly_returns_arr.shape != (12, 4, 4):
                print(
                    "Please provide 12 months of data with 4 currencies each month. \n   \
                    !!! 3D ARRAY OF FORMAT (12,4,4) REQUIRED !!!"
                )
                raise Exception
            else:
                return monthly_returns_arr
    # Handle exceptions
    except FileNotFoundError:
        print(f"Error: File not found in the given location: ./data/{ input_filename}")
        raise FileNotFoundError
    except json.JSONDecodeError as json_exception:
        print(
            "Error: Problem with reading the file; check the content of the file. \
              Use only numerical data represented as a 3D matrix of shape (12,4,4)"
        )
        raise json_exception
    except Exception as generic_except:
        print(
            f"Error: Unexpected problem while loading the data;\
                  please check with the development team. {generic_except}",
        )
        raise generic_except


def max_return(
    month: int,
    from_currency: int,
    portfolio_value: float,
    monthly_returns_arr: np.ndarray,
    num_months: int,
    num_currencies: int,
) -> float:
    """
    Calculate the maximum return from a portfolio of currencies

    Args:
        month (int): The current month
        from_currency (int): The current currency
        portfolio_value (float): The current value of the portfolio
        monthly_returns_arr (np.ndarray): The monthly returns of currencies in a
                     3D array of shape (12,4,4)
        num_months (int): The total number of months
        num_currencies (int): The total number of currencies

    Returns:
        total_trade_return (float): The maximum possible return for the given
            returns data and portfolio value
    """

    # Check if we have reached the last but one month: Need to end trade with
    if month == num_months - 1:
        # Switch last month trade to GBP (Problem constraint)
        to_trade_currency = int(os.getenv("TO_TRADE_CURRENCY", "0"))
        trade_return = monthly_returns_arr[month, from_currency, to_trade_currency]
        total_trade_return = portfolio_value * trade_return
        return total_trade_return

    max_total_returns = 0

    # Iterate over all possible trades in the current month
    for to_trade_currency in range(num_currencies):
        trade_return = monthly_returns_arr[month, from_currency, to_trade_currency]
        total_trade_return = portfolio_value * trade_return

        # Recursively calculate the maximum return from the next month
        next_return = max_return(
            month + 1,
            to_trade_currency,
            total_trade_return,
            monthly_returns_arr,
            num_months,
            num_currencies,
        )

        # Update the maximum profit
        max_total_returns = max(max_total_returns, next_return)

    return max_total_returns


def calculate_max_return(
    monthly_returns_arr: np.ndarray) -> float:
    """
    Calculate the maximum return from a portfolio of currencies

    Args:
        monthly_returns_arr (np.ndarray): The monthly returns of currencies in a \
            3D array of shape (12,4,4)

    Returns:
        maximum_returns (float): The maximum possible returns for the given returns data
    """

    # Get the number of months and currencies
    num_months = monthly_returns_arr.shape[0]
    num_currencies = monthly_returns_arr.shape[1]

    # Initial currency is GBP (Problem constraint)
    from_currency = int(os.getenv("FROM_CURRENCY", "0"))  # GBP
    first_month = int(os.getenv("START_MONTH", "0"))  # First month
    portfolio_value = 1.0


    # Start the recursive calculation from the first month with GBP
    return max_return(
        first_month,
        from_currency,
        portfolio_value,
        monthly_returns_arr,
        num_months,
        num_currencies,
    )


def main(input_args):
    """
    Main function to run the application

    Args:
        input_args (list): The list of command line arguments

    Returns:
        None

    Prints:
        Maximum possible return over the year

    Exits:
        If the filename is not provided
        If any exception occurs while loading the data or calculating the maximum return,\
            errors will be printed and the application will exit
    """

    # Check if the filename is provided
    if input_args:
        input_filename = input_args[0]
    else:
        print(
            "\nError: Could not calculate the maximum returns. Please provide returns data file name."
        )
        print("Usage of application: python main.py filename")
        sys.exit(1)
    # Load the data from the file
    try:
        logging.info(f"Loading data from file: {input_filename}")
        
        monthly_returns_matrix = load_data(input_filename)

        logging.info("Data loaded successfully")
        logging.info("Calculating the maximum return over the year ...")

        # Calculate the maximum return
        max_return_possible = calculate_max_return(monthly_returns_matrix)

        # Calculate the maximum profit
        max_profit_possible = (max_return_possible - 1.00)*100
        max_profit_possible = round(max_profit_possible, 2)

        print(f"Maximum possible return over the year: {max_profit_possible}%")
        logging.info(f"Maximum possible return over the year: {max_profit_possible}%")
    except Exception as exeption:
        logging.exception(f"Error:{ exeption}")
        print(
            "\nCould not calculate the maximum returns. Please try again after correcting the errors."
        )
        sys.exit(1)


if __name__ == "__main__":
    command_line_input_args = sys.argv[1:]
    main(command_line_input_args)
