import pytest
import budget.csv_utils

test_config = {
    "itemsToSkip": ["transfer", "deposit"],
    "categoryFromDesc": {
        "health": ["walgreens", "cvs"],
        "news": ["nytimes", "washington post", "post dispatch"],
        "tech": ["apple.com/bill", "amazon prime"],
    },
    "categoryFromCsvCategory": {
        "grocery": ["Grocery"],
        "health": ["Medical"]
    }
}


@pytest.fixture(autouse=True)
def load_test_config(monkeypatch):

    monkeypatch.setattr(budget.csv_utils,
                        "config", test_config)
