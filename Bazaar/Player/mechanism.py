from copy import copy
from typing import Optional, List, Callable

from pydantic import BaseModel

from Bazaar.Common.cards import Cards
from Bazaar.Common.equations import Equations, Equation
from Bazaar.Common.turn_state import TurnState

from Bazaar.Player.exchanges import Exchange
import re

from Bazaar.Player.purchases import PurchaseSequences, PurchaseSequence
from Bazaar.Player.strategy import Strategy
from Bazaar.Player.decorators import *

_ACTOR_ALLOWED_LENGTHS = [2, 3, 4]
_ACTOR_NAME_INDEX = 0
_POLICY_INDEX = 1
_EXN_INDEX = 2
_CHEAT_INDEX = 3
_COUNT_INDEX = 3
_DEFAULT_COUNT = 1
_MIN_COUNT_INCLUSIVE = 1
_MAX_COUNT_EXCLUSIVE = 8

SETUP_EXN = "setup"
REQUEST_PEBBLE_OR_TRADES_EXN = "request-pebble-or-trades"
REQUEST_CARDS_EXN = "request-cards"
WIN_EXN = "win"

class Mechanism(BaseModel):

    name: str
    policy: str
    equations: Equations = None
    exception_raised: Optional[str] = None
    cheat_type: Optional[str] = None
    count: Optional[int] = _DEFAULT_COUNT
    did_win: bool = False
    game_over: bool = False

    def name(self) -> str:
        """
        Get the name of the player.
        """
        return self.name

    @setup_exception_decorator
    def setup(self, equations: Equations) -> None:
        """
        The player is handed the set of equations, which is visible to all.

        :param equations: the equations handed to the player.
        :type equations: Equations
        :return: None
        """
        self.equations = copy(equations)

    @request_pebble_or_trades_decorator
    @use_non_existent_equation_decorator
    @bank_cannot_trade_decorator
    @wallet_cannot_trade_decorator
    def request_pebble_or_trades(
        self, turn_state: TurnState
    ) -> Optional[list[Equation]]:
        """
        After receiving the turn state, a player requests one of:
        requests a pebble, or a possibly empty sequence of exchanges of pebbles.

        :param turn_state: the turn state of the player
        :type turn_state: TurnState
        :return: None if the player requests a pebble, sequence of exchanges otherwise.
        :rtype: Optional[Exchange]
        """
        strategy = Strategy(equations=copy(self.equations), turn_state=turn_state, policy=self.policy)
        return strategy.get_trade_purchase()[0].pebble_exchanges

    @request_cards_decorator
    @buy_unavailable_card_decorator
    @wallet_cannot_buy_card_decorator
    def request_cards(self, turn_state: TurnState) -> PurchaseSequence:
        """
        After receiving the turn state, a player requests a possible empty sequence of card purchases.

        :param turn_state: the turn state of the player
        :type turn_state: TurnState
        :return: sequence of (possibly empty) card purchases
        :rtype: PurchaseSequence
        """
        strategy = Strategy(equations=copy(self.equations), turn_state=turn_state, policy=self.policy)
        purchases = strategy.get_purchase(turn_state)
        return purchases

    @win_decorator
    def win(self, did_win: bool) -> None:
        """
        The player is informed whether it won or not.

        :param did_win: True if the player is won, False otherwise.
        :type did_win: bool
        """
        self.game_over = True
        self.did_win = did_win

    @classmethod
    def deserialize(cls, data: List[str]) -> "Mechanism":
        """
        Deserializes an actor from a data list following one of the formats:
        [ActorName, Policy], [ActorName, Policy, Exn], [ActorName, Policy, a cheat]

        :param data: Actor data to be deserialized.
        :type data: List[str]
        :return: actor class object
        :rtype: Mechanism
        """
        if len(data) not in _ACTOR_ALLOWED_LENGTHS:
            raise ValueError("Actor data provided for deserialization is invalid.")
        if not all([isinstance(field, str) or isinstance(field, int) for field in data]):
            raise TypeError(
                "Actor data fields provided for deserialization are not of type string."
            )

        name = data[_ACTOR_NAME_INDEX]
        if not re.fullmatch("^[a-zA-Z0-9]+$", name):
            raise ValueError(
                "Actor name provided for deserialization is of invalid format."
            )

        policy = data[_POLICY_INDEX]
        if not policy in ("purchase-points", "purchase-size"):
            raise ValueError("Actor policy provided for deserialization is invalid.")

        exception_raised = None
        count = _DEFAULT_COUNT
        if len(data) == 3 or (len(data) == 4 and data[_EXN_INDEX] != "a cheat"):
            exception_raised = data[_EXN_INDEX]
            count = data[_COUNT_INDEX] if len(data) == 4 else _DEFAULT_COUNT
            if count and count not in range(_MIN_COUNT_INCLUSIVE, _MAX_COUNT_EXCLUSIVE):
                raise ValueError("Actor count provided for deserialization is invalid.")
            if not exception_raised in (
                "setup",
                "request-pebble-or-trades",
                "request-cards",
                "win",
            ):
                raise ValueError(
                    "Actor exception raised provided for deserialization is invalid."
                )

        cheat_type = None
        if len(data) == 4 and data[2] == "a cheat":
            cheat_type = data[3]
            if not cheat_type in (
                "use-non-existent-equation",
                "bank-cannot-trade",
                "wallet-cannot-trade",
                "buy-unavailable-card",
                "wallet-cannot-buy-card"
            ):
                raise ValueError(
                    "Actor exception raised provided for deserialization is invalid."
                )

        return cls(name=name, policy=policy, exception_raised=exception_raised, cheat_type=cheat_type, count=count)

    def serialize(self) -> str:
        """
        Serializes the actor as its name string.

        :return: actor's name
        :rtype: str
        """
        return self.name

def check_duplicate_names(actors: List[Mechanism]) -> bool:
    """
    Checks whether a list of actors contains duplicate names.

    :param actors: list of actors as a list of Mechanism objects.
    :type actors: List[Mechanism]
    :return: True if the list of actors contains duplicate names, False otherwise.
    :rtype: bool
    """
    actor_names = [actor.name for actor in actors]
    if len(actor_names) != len(set(actor_names)):
        return True
    return False


def deserialize_actors(data: List[List[str]]) -> List[Mechanism]:
    """
    Deserializes *Actors from a list of Actor data.

    :param data: *Actors data to be deserialized
    :type data: List[List[str]]
    :returns: list of deserialized Mechanism objects
    :rtype: List[Mechanism]
    """
    if not isinstance(data, list) or len(data) > 6:
        raise ValueError("*Actors data provided for deserialization is invalid.")

    actors = [Mechanism.deserialize(actor) for actor in data]

    if check_duplicate_names(actors):
        raise ValueError("Duplicate actor names found in provided deserialize data.")

    return actors


def serialize_actors(actors: List[Mechanism]) -> List[str]:
    """
    Serializes *Actors as a list of Mechanism objects.

    :param actors: *Actors data to be serialized as a list of Mechanism objects.
    :type actors: List[Mechanism]
    :return: list of actor names
    :rtype: List[str]
    """
    if check_duplicate_names(actors):
        raise ValueError("Duplicate actor names found in provided serialized data.")

    return [actor.serialize() for actor in actors]
