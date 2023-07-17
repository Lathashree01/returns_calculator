"""
This file contains fixtures that are used in multiple tests.
"""
from unittest.mock import patch
import numpy as np
import pytest


@pytest.fixture
def mock_monthly_returns_arr():
    #data= [[]] # needs to be a 3d array of shape 12,4,4
    monthly_returns_arr = np.array(data)
    yield monthly_returns_arr


@pytest.fixture
def mock_max_return():
    with patch("src.main.max_return") as mock:
        yield mock


@pytest.fixture
def mock_load_data():
    with patch("src.main.load_data") as mock:
        yield mock


@pytest.fixture
def mock_calculate_max_return():
    with patch("src.main.calculate_max_return") as mock:
        yield mock
