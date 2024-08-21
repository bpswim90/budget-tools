
def flipSignOfAmount(amount):
    """Flip positive value to negative & vice versa, given a string amount"""
    if amount.startswith('-'):
        return amount[1:]
    return '-' + amount
