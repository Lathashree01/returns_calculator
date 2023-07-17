"""
Contains functional tests for the main function
"""
from src.main import main


def test_main(capsys):
    """
    Test the complete functionality of the main function by comparing 
    the expected output that gets printed to the console
    """
    # Run the main function with valid file name as input and compare the output
    main(['currency_data.txt'])
    captured = capsys.readouterr()
    assert captured.out == "Maximum possible return over the year: 270.57%\n"
    