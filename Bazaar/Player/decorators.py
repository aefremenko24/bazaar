from typing import Callable

from Bazaar.Common.cards import Cards, Card
from Bazaar.Common.equations import Equations, Equation
from Bazaar.Common.rule_book import RuleBook
from Bazaar.Common.turn_state import TurnState
from Bazaar.Player.exchanges import Exchange
from Bazaar.Player.purchases import PurchaseSequence


def setup_exception_decorator(func: Callable) -> Callable:
    """
    Applied to the setup method.
    Throws an exception if the "setup" exception is provided in self.exception_raised.

    :param self: this Mechanism containing the exception type
    :param func: The function to decorate
    :return: The decorated function
    """

    def wrapper_func(self, equations: Equations):
        if self.exception_raised == "setup":
            if self.count == 1:
                raise Exception("Exception raised during setup")
            else:
                self.count -= 1
        return func(self, equations)

    return wrapper_func


def request_pebble_or_trades_decorator(func: Callable) -> Callable:
    """
    Applied to the request_pebble_or_trades method.
    Throws an exception if the "request-pebble-or-trades" exception is provided in self.exception_raised.

    :param self: this Mechanism containing the exception type
    :param func: The function to decorate
    :return: The decorated function
    """

    def wrapper_func(self, turn_state: TurnState):
        if self.exception_raised == "request-pebble-or-trades":
            if self.count == 1:
                raise Exception("Exception raised during request-pebble-or-trades")
            else:
                self.count -= 1
        return func(self, turn_state)

    return wrapper_func


def request_cards_decorator(func: Callable) -> Callable:
    """
    Applied to the request_cards method.
    Throws an exception if the "request-cards" exception is provided in self.exception_raised.

    :param self: this Mechanism containing the exception type
    :param func: The function to decorate
    :return: The decorated function
    """

    def wrapper_func(self, turn_state: TurnState):
        if self.exception_raised == "request-cards":
            if self.count == 1:
                raise Exception("Exception raised during request-cards")
            else:
                self.count -= 1
        return func(self, turn_state)

    return wrapper_func


def win_decorator(func: Callable) -> Callable:
    """
    Applied to the win_decorator method.
    Throws an exception if the "win" exception is provided in self.exception_raised.

    :param self: this Mechanism containing the exception type
    :param func: The function to decorate
    :return: The decorated function
    """
    def wrapper_func(self, did_win: bool):
        if self.exception_raised == "win":
            if self.count == 1:
                raise Exception("Exception raised during win")
            else:
                self.count -= 1
        return func(self, did_win)

    return wrapper_func


def use_non_existent_equation_decorator(func: Callable) -> Callable:
    """
    Applied to the request_pebble_or_trades method.
    Returns a request for an exchange using a non-existent equation
    if the self.cheat_type flag is set to "use-non-existent-equation"

    :param self: this Mechanism containing the cheat type
    :param func: The function to decorate
    :return: The decorated function
    """
    def wrapper_func(self, turn_state: TurnState):
        if self.cheat_type == "use-non-existent-equation":
            non_existent_equation = Equation.generate_random()
            while non_existent_equation in self.equations:
                non_existent_equation = Equation.generate_random()
            return [non_existent_equation]
        else:
            return func(self, turn_state)

    return wrapper_func


def bank_cannot_trade_decorator(func: Callable) -> Callable:
    """
    Applied to the request_pebble_or_trades method.
    Returns a request for an exchange that the bank cannot trade
    if the self.cheat_type flag is set to "bank-cannot-trade"

    :param self: this Mechanism containing the cheat type
    :param func: The function to decorate
    :return: The decorated function
    """

    def wrapper_func(self, turn_state: TurnState):
        if self.cheat_type == "bank-cannot-trade":
            invalid_equation = Equation.generate_random()
            while invalid_equation.rhs in turn_state.bank:
                invalid_equation = Equation.generate_random()
            return [invalid_equation]
        else:
            return func(self, turn_state)

    return wrapper_func


def wallet_cannot_trade_decorator(func: Callable) -> Callable:
    """
    Applied to the request_pebble_or_trades method.
    Returns a request for an exchange that the player's wallet cannot trade
    if the self.cheat_type flag is set to "wallet-cannot-trade"

    :param self: this Mechanism containing the cheat type
    :param func: The function to decorate
    :return: The decorated function
    """

    def wrapper_func(self, turn_state: TurnState):
        if self.cheat_type == "wallet-cannot-trade":
            invalid_equation = Equation.generate_random()
            while invalid_equation.lhs in turn_state.active_player_wallet:
                invalid_equation = Equation.generate_random()
            return [invalid_equation]
        else:
            return func(self, turn_state)

    return wrapper_func


def buy_unavailable_card_decorator(func: Callable) -> Callable:
    """
    Applied to the request_cards method.
    Returns a request to purchase a card that is not among the currently visible ones
    if the self.cheat_type flag is set to "buy-unavailable-card".

    :param self: this Mechanism containing the cheat type
    :param func: The function to decorate
    :return: The decorated function
    """

    def wrapper_func(self, turn_state: TurnState):
        if self.cheat_type == "buy-unavailable-card":
            non_existent_card = Card.generate_random()
            while non_existent_card in turn_state.cards.cards:
                non_existent_card = Card.generate_random()
            return PurchaseSequence(sequence=Cards(cards=[non_existent_card]))
        else:
            return func(self, turn_state)

    return wrapper_func


def wallet_cannot_buy_card_decorator(func: Callable) -> Callable:
    """
    Applied to the request_cards method.
    Returns a request to purchase a card that is not affordable by the player's wallet
    if the self.cheat_type flag is set to "wallet-cannot-buy-card".

    :param self: this Mechanism containing the cheat type
    :param func: The function to decorate
    :return: The decorated function
    """

    def wrapper_func(self, turn_state: TurnState):
        if self.cheat_type == "wallet-cannot-buy-card":
            if self.cheat_type == "buy-unavailable-card":
                unavailable_card = Card.generate_random()
                while RuleBook.can_purchase_card(
                    unavailable_card, turn_state.active_player_wallet
                ):
                    unavailable_card = Card.generate_random()
                return PurchaseSequence(sequence=Cards(cards=[unavailable_card]))
        else:
            return func(self, turn_state)

    return wrapper_func
