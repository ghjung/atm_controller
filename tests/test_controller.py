import pytest
from _pytest import monkeypatch


from atm.card import Card
from atm import exceptions
from atm.card_reader import CardReader
from atm.bank import Bank
from atm.controller import ATMController
from atm.user_session import UserSession


def test_insert_card(card_reader, controller):
    assert controller.insert_card()

@pytest.mark.xfail(raises=exceptions.InvalidCardError)
def test_insert_card_exception(broken_card_reader, controller):
    controller.insert_card()

def test_pin_number_success(valid_pin, controller):
    card = Card(id='1', accounts=['a', 'b'], owner='Bear')
    controller.user_session.store_data(card)
    assert controller.pin_number()

def test_pin_number_fail(invalid_pin, controller):
    card = Card(id='1', accounts=['a', 'b'], owner='Bear')
    controller.user_session.store_data(card)
    assert not controller.pin_number()

def test_select_account_success(account_select, controller):
    card = Card(id='1', accounts=['a', 'b'], owner='Bear')
    controller.user_session.store_data(card)
    assert controller.select_account() == 'a'

def test_balance(balance, controller):
    card = Card(id='1', accounts=['a', 'b'], owner='Bear')
    controller.user_session.store_data(card)
    controller.user_session.selected_account = 'a'
    assert controller.balance() == 3000

def test_withdraw_success(proper_user_demand, balance, controller):
    card = Card(id='1', accounts=['a', 'b'], owner='Bear')
    controller.user_session.store_data(card)
    controller.user_session.selected_account = 'a'
    res = controller.withdraw()

    assert res == 2000

@pytest.mark.xfail(raises=exceptions.NotEnoughBalance)
def test_withdraw_fail(big_user_demand, balance, controller):
    card = Card(id='1', accounts=['a', 'b'], owner='Bear')
    controller.user_session.store_data(card)
    controller.user_session.selected_account = 'a'
    controller.withdraw()

def test_deposit_success(cash_deposit, balance, controller):
    card = Card(id='1', accounts=['a', 'b'], owner='Bear')
    controller.user_session.store_data(card)
    controller.user_session.selected_account = 'a'
    res = controller.deposit()

    assert res == 4000
