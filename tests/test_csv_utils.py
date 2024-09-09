import pytest
from budget.csv_utils import (skip_row, category_matches_config_category, get_category,
                              desc_matches_category)


skipRowData = [
    (['5/5/2024', 'Transaction', 'Grocery', '-100.00'], False),
    (['5/5/2024', 'Test', 'Grocery', '-100.00'], False),
    (['5/5/2024', 'transfer', '', '-100.00'], True),
    (['5/5/2024', 'deposit', '', '-100.00'], True)
]


@pytest.mark.parametrize("csv_row,expected", skipRowData)
def test_skip_row(csv_row, expected):
    result = skip_row(csv_row, 1)
    assert result is expected


categoryMatchesData = [
    ("Grocery", "grocery", True),
    ("Medical", "health", True),
    ("Medical", "grocery", False),
]


@pytest.mark.parametrize("csv_category,budget_category,expected", categoryMatchesData)
def test_category_matches_config_category(csv_category, budget_category, expected):
    result = category_matches_config_category(csv_category, budget_category)
    assert result is expected


getCategoryData = [
    (['5/5/2024', 'Transaction', 'Grocery', '-100.00'], 2, 'grocery'),
    (['5/5/2024', 'Test', 'Medical', '-100.00'], 2, 'health'),
    (['5/5/2024', 'transfer', 'other', '-100.00'], 2, ''),
    (['5/5/2024', 'deposit', 'other', '-100.00'], 2, '')
]


@pytest.mark.parametrize("row,category_idx,expected", getCategoryData)
def test_get_category(row, category_idx, expected):
    result = get_category(row, category_idx)
    assert result == expected


descMatchesData = [
    ("walgreens purchase", "health", True),
    ("bill apple.com/bill", "tech", True),
    ("example cvs transaction", "health", True),
    ("new york times", "tech", False),
    ("blah blah blah", "news", False),
]


@pytest.mark.parametrize("desc,category,expected", descMatchesData)
def test_desc_matches_category(desc, category, expected):
    result = desc_matches_category(desc, category)
    assert result is expected
