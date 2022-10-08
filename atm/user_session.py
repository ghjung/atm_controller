from atm.card import Card


class UserSession:
    """
    Represent user session

    It stores informations while user access the system
    """

    def __init__(self, card=None):
        self.card = card
        self._selected_account = None

    def store_data(self, card=None):
        self.card = card

    @property
    def card_id(self):
        return self.card.id

    @property
    def accounts_in_card(self):
        return self.card.accounts

    @property
    def selected_account(self):
        return self._selected_account

    @selected_account.setter
    def selected_account(self, account):
        self._selected_account = account
