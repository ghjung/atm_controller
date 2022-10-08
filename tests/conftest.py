import pytest

from atm import exceptions
from atm.bank import Bank
from atm.card import Card
from atm.card_reader import CardReader
from atm.cash_bin import CashBin
from atm.controller import ATMController
from atm.touch_screen import TouchScreen
from atm.user_session import UserSession


@pytest.fixture
def controller():
    atm = ATMController()
    yield atm

@pytest.fixture
def card_reader(monkeypatch):
    def return_card(*args, **kwargs):
        return Card(id='1', accounts=['a', 'b'], owner='Bear')
    monkeypatch.setattr(CardReader, 'read', return_card)

@pytest.fixture
def broken_card_reader(monkeypatch):
    def failed(*args, **kwargs):
        raise exceptions.InvalidCardError
    monkeypatch.setattr(CardReader, 'read', failed)

@pytest.fixture
def invalid_pin(monkeypatch):
    def invalid(*args, **kwargs):
        return False
    monkeypatch.setattr(Bank, 'validate_pin_number', invalid)

@pytest.fixture
def valid_pin(monkeypatch):
    def valid(*args, **kwargs):
        return True
    monkeypatch.setattr(Bank, 'validate_pin_number', valid)

@pytest.fixture
def card_id(monkeypatch):
    def id(*args, **kwargs):
        return '1'
    monkeypatch.setattr(UserSession, 'card_id', id)

@pytest.fixture
def account_select(monkeypatch):
    def account(*args, **kwargs):
        return 'a'
    monkeypatch.setattr(TouchScreen, 'select_account', account)

@pytest.fixture
def balance(monkeypatch):
    def balance(*args, **kwargs):
        return 3000
    monkeypatch.setattr(Bank, 'get_balance', balance)

@pytest.fixture
def big_user_demand(monkeypatch):
    def big(*args, **kwargs):
        return 4000
    monkeypatch.setattr(TouchScreen, 'cash_demand_input', big)

@pytest.fixture
def proper_user_demand(monkeypatch):
    def proper(*args, **kwargs):
        return 1000
    monkeypatch.setattr(TouchScreen, 'cash_demand_input', proper)

@pytest.fixture
def cash_deposit(monkeypatch):
    def cash(*args, **kwargs):
        return 1000
    monkeypatch.setattr(CashBin, 'wait_for_cash', cash)
