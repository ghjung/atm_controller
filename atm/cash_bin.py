class CashBin:
    """Represent cash bin """

    def __init__(self):
        self._balance = 0

    @property
    def balance(self):
        return self._balance

    def load_cash(self, cash):
        self._balance += cash

    def prepare_cash(self, demand):
        """Prepare cash by user demanding"""
        pass

    def wait_for_cash(self):
        """Wait for cash insert"""
        pass