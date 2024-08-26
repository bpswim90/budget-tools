import pytest
from budget.csv_utils import skip_row


@pytest.fixture
def csv_row():
    return ['5/5/2024', 'Transaction', 'Grocery', '-100.00']


@pytest.fixture
def csv_row_skip():
    return ['5/5/2024', 'Requested transfer', '', '-100.00']


def test_skip_row_returns_false(csv_row):
    result = skip_row(csv_row, 1)
    assert result is False


def test_skip_row_returns_true(csv_row_skip):
    result = skip_row(csv_row_skip, 1)
    assert result is True
