# Flips positive value to negative & vice versa, given a string amount
def flipSignOfAmount(amount):
    if amount.startswith('-'):
        return amount[1:]
    return '-' + amount