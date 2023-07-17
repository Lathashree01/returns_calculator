"""
This module contains unit tests for the main.py module.
"""
import json
import logging
import pytest
from src.main import load_data, max_return, calculate_max_return, main


def test_load_data():
    """
    This function tests the behavior of the load_data() function with valid input
    and asserts the output to the expected output. It also tests the behavior of the
    function with invalid input and asserts the expected exception.
    """

    # Test Scenario 1: Loading data from a valid monthly returns input file
    monthly_returns_data = load_data("currency_data.txt")
    assert monthly_returns_data.shape == (12, 4, 4)

    # Test Scenario 2: Test loading data from an invalid file:
    # File not present in the given location
    with pytest.raises(FileNotFoundError):
        load_data("invalid_file.txt")

    # Test Scenario 3: Test loading data from a file with invalid data
    # in the file (the matrix has string inputs)
    with pytest.raises(json.JSONDecodeError):
        load_data("currency_data_fail.txt")


def test_max_return(mock_monthly_returns_arr):
    """
    This function tests the behavior of the max_return() function with valid input 
    and assrts the output to the expected output..
    """
    expected_output = 3.705696694904843
    assert max_return(0, 0, 1.0, mock_monthly_returns_arr, 12, 4) == expected_output


def test_calculate_max_return(mock_max_return, mock_monthly_returns_arr):
    """
    This function tests the behavior of the calculate_max_return() function 
    and asserts the output to the expected output.
    The mock_max_return() function is mocked to return the expected output.
    The max_return function is check for the expected call with the expected arguments.
    """
    expected_output = 3.705696694904843
    mock_max_return.return_value = expected_output
    actual_result = calculate_max_return(mock_monthly_returns_arr)
    mock_max_return.assert_called_once_with(0, 0, 1.0, mock_monthly_returns_arr, 12, 4)
    assert actual_result == expected_output


def test_main(mock_load_data, mock_calculate_max_return, caplog):
    """
    This function tests the behavior of the main() function in terms of logging.
    The mock_load_data() and mock_calculate_max_return() functions are mocked.
    """
    mock_load_data.return_value = [[1, 2], [3, 4]]
    mock_calculate_max_return.return_value = 5.0
    input_args = ["filename"]
    with caplog.at_level(logging.INFO):
        main(input_args)
        assert "Loading data from file: filename" in caplog.text
        assert "Data loaded successfully" in caplog.text
        assert "Calculating the maximum return over the year ..." in caplog.text
        assert "Maximum possible return over the year:" in caplog.text
        # assert False
    mock_load_data.assert_called_once_with("filename")
    mock_calculate_max_return.assert_called_once_with([[1, 2], [3, 4]])


def test_main_no_args(caplog):
    """
    This function tests the behavior of the main() function when no arguments are passed.
    """
    input_args = []
    with caplog.at_level(logging.ERROR):
        with pytest.raises(SystemExit):
            main(input_args)
            assert "Usage of application: python main.py filename" in caplog.text


def test_main_load_data_exception(mock_load_data, caplog):
    """
    This function tests the behavior of the main() function when the load_data() function
    performs system exit due to an exception.
    """
    mock_load_data.side_effect = Exception("Error loading data")
    input_args = ["filename"]
    with caplog.at_level(logging.ERROR):
        with pytest.raises(SystemExit):
            main(input_args)
            assert "Error: Error loading data" in caplog.text


def test_main_calculate_max_return_exception(
    mock_load_data, mock_calculate_max_return, caplog
):
    """
    This function tests the behavior of the main() function when the calculate_max_return() 
    function raises an exception.
    """
    mock_load_data.return_value = [[1, 2], [3, 4]]
    mock_calculate_max_return.side_effect = Exception("Error calculating max return")
    input_args = ["filename"]
    with caplog.at_level(logging.ERROR):
        with pytest.raises(SystemExit):
            main(input_args)
            assert "Error: Error calculating max return" in caplog.text
