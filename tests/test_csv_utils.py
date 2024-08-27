import pytest
from budget.csv_utils import skip_row, category_matches_config_category


data = [
    (['5/5/2024', 'Transaction', 'Grocery', '-100.00'], False),
    (['5/5/2024', 'Test', 'Grocery', '-100.00'], False),
    (['5/5/2024', 'Requested transfer', '', '-100.00'], True),
    (['5/5/2024', 'ACH DEPOSIT', '', '-100.00'], True)
]


@pytest.mark.parametrize("csv_row,expected", data)
def test_skip_row(csv_row, expected):
    result = skip_row(csv_row, 1)
    assert result is expected


categoryData = [
    ("Grocery", "grocery", True),
    ("Medical", "health", True),
    ("Medical", "grocery", False),
]


@pytest.mark.parametrize("csv_category,budget_category,expected", categoryData)
def test_category_matches_config_category(csv_category, budget_category, expected):
    result = category_matches_config_category(csv_category, budget_category)
    assert result is expected
