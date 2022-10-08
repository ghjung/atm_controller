class Card:
    """ Represent bank card """

    def __init__(self, id=None, accounts=[], owner=None):
        self._id = id
        self._accounts = accounts
        self._owner = owner

    @property
    def id(self):
        return self._id

    @property
    def accounts(self):
        return self._accounts

    @property
    def owner(self):
        return self._owner
