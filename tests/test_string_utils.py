from budget.string_utils import flip_sign_of_amount


def test_flip_sign_of_amount():
    amount = '-23.45'
    assert flip_sign_of_amount(amount) == '23.45'
