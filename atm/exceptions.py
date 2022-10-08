class InvalidCardError(Exception):
    """There was problem to read inserted card"""

class NotEnoughBalance(Exception):
    """There was insufficient amount of balance"""

class NoRrespondingBankError(Exception):
    """There was no responding from bank API"""
