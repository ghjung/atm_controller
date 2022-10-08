from atm import exceptions
from atm.bank import Bank
from atm.card import Card
from atm.cash_bin import CashBin
from atm.card_reader import CardReader
from atm.touch_screen import TouchScreen
from atm.user_session import UserSession


# Entering pin number iteration is limited in this.
LIMIT_NUM_OF_ENTER_PIN = 5


class ATMController:
    """
    Represent ATM System

    ATM is consider as in three sub-component: cash bin, screen, card reader.
    ATM connects with Bank through some type of API.
    ATM serve on customer at a time so there is no need to consider multiple
    customer demand
    ATM server like sequentail pipeline which means each of process should be
    done for forwarding next process.
    """

    # Store current customer session while in serving
    user_session = UserSession()

    def __init__(self):
        self.bank = Bank()
        self.cash_bin = CashBin()
        self.screen = TouchScreen()
        self.card_reader = CardReader()

    def insert_card(self):
        """
        Return status of the card what user inserted into card reader

        If valid card, this function return True and caching user information
        what stored in the card
        If failed to read card raise InvalidCardErorr

        By this return value caller(i.e., UI process over display)
        move to a next menu screen or pop up an warning message
        """

        # validate card
        try:
            card = self.card_reader.read()
        except:
            raise exceptions.InvalidCardError()
        else:
            self.user_session.store_data(card)
            return True

    def pin_number(self):
        """
        Validate pin number input

        Pin number is acquired via num pad by user. There is limited number of
        input iteration. If user failed enter correct pin number
        in given iteration, system ask self.bank.to block this card for preventing
        fraud.
        """
        current_attempt = 0
        card_id = self.user_session.card_id
        while current_attempt < LIMIT_NUM_OF_ENTER_PIN:
            try:
                pin_num = self.screen.pin_input()
                if self.bank.validate_pin_number(card_id, pin_num):
                    return True
                else:
                    current_attempt += 1
            except Exception as e:
                current_attempt += 1

        # Call self.bank.system to block this card
        self.bank.block_card(card_id)

        return False

    def select_account(self):
        """
        Select account already caching in user session
        """
        accounts = self.user_session.accounts_in_card

        # Assume display pop account list from accounts
        # Syste waits user input which touch given menu
        try:
            account = self.screen.select_account()
        except Exception as e:
            """raise Timeout"""
            raise

        self.user_session.selected_account = account
        return self.user_session.selected_account

    def withdraw(self):
        """
        Withdraw cash from account

        It assume that system ensure amount of cash in the cash bin.
        This function get input as an amount of cash then check with
        balance of account

        If there is sufficient balance in the account, system ask the cash bin
        to prepare given amount of cash.
        If there is insufficient balance in the account, system raise exception
        NotEnoughBalance then caller will handle this exception
        """

        account = self.user_session.selected_account
        user_demand = self.screen.cash_demand_input()
        try:
            balance = self.bank.get_balance(account)
        except Exception as e:
            """There went something wrong"""
            raise exceptions.NoRrespondingBankError

        if user_demand > balance:
            raise exceptions.NotEnoughBalance()

        balance -= user_demand
        try:
            self.bank.update_balance(account, balance)
        except Exception as e:
            """There went something wrong"""
            raise exceptions.NoRrespondingBankError

        # Ask card bin to prepare cash
        self.cash_bin.prepare_cash(user_demand)

        return balance

    def balance(self):
        """
        Return balance of the account what user selected in previous step
        """
        account = self.user_session.selected_account
        try:
            balance = self.bank.get_balance(account)
        except Exception as e:
            """There went something wrong"""
            raise exceptions.NoRrespondingBankError

        return balance

    def deposit(self):
        """
        Deposit user cash into cash bin and update the balance of account
        """
        account = self.user_session.selected_account
        try:
            balance = self.bank.get_balance(account)
        except Exception as e:
            """There went something wrong"""
            raise exceptions.NoRrespondingBankError

        try:
            user_demand = self.cash_bin.wait_for_cash()
        except Exception as e:
            """There went something wrong"""
            raise exceptions.NoRrespondingBankError

        balance += user_demand
        try:
            self.bank.update_balance(account, balance)
        except Exception as e:
            """There went something wrong"""
            raise exceptions.NoRrespondingBankError

        return balance

    def reset_user_session(self):
        """
        Once serving a customer is finished, previous session data should
        be destroyed
        """
        self.user_session = UserSession()
