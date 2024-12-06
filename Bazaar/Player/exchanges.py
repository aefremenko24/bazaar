import queue
from copy import copy
from typing import List, Set, Optional

from pydantic import BaseModel, Field

from Bazaar.Common.data import MAX_EXCHANGE_DEPTH
from Bazaar.Common.equations import Equation, Equations
from Bazaar.Common.cards import Cards, Card
from Bazaar.Common.pebble import PebbleCollection

MAX_EXCHANGE_DEPTH = 4


class Exchange(BaseModel):
    """
    An entry of pebble exchange.
    wallet is the state of wallet after performing the exchange
    bank is the state of bank after exchange.
    pebble_exchanges is the sequence of equation used for exchange.

    """

    wallet: PebbleCollection = PebbleCollection()
    bank: PebbleCollection = PebbleCollection()
    pebble_exchanges: List[Equation] = list()

    def perform_exchange(self, equation: Equation):
        """
        return the next exchange entry with new bank and wallet after the exchange of this equation,
        action_sequence append the new equation
        :param equation: an equation that can be exchange with this wallet
        :type equation: Equation
        :returns: exchange with updated info
        :rtype: Exchange
        """
        new_action_sequence = self.pebble_exchanges + [equation]
        new_wallet, new_bank = equation.trade_equation(self.wallet, self.bank)
        return Exchange(
            wallet=new_wallet, bank=new_bank, pebble_exchanges=new_action_sequence
        )

    def possible_next_exchange(self, equations: Equations):
        """
        Based on all possible next exchange of equations using the  wallet of this exchange, return all possible
        exchange entries with new bank and wallet after the exchange of equation, action_sequence appened the new equation
        :param equations: all equation for exchange
        :type equations: Equations
        :returns: a List of next Exchange
        :rtype: List(Exchange)
        """
        next_exchanges = []

        filtered_equation = equations.filter_equations(self.wallet, self.bank)
        for eq in filtered_equation:
            next_exchange = self.perform_exchange(eq)
            next_exchanges = next_exchanges + [next_exchange]
        return next_exchanges

    def less_pebble_exchange(self, other):
        if not isinstance(other, Exchange):
            raise TypeError("The second argument is not of type Exchange")
        if len(self.pebble_exchanges) == len(other.pebble_exchanges):
            for i in range(len(self.pebble_exchanges)):
                if self.pebble_exchanges[i] < other.pebble_exchanges[i]:
                    return True
        return len(self.pebble_exchanges) < len(other.pebble_exchanges)

    @staticmethod
    def validate_deserialize_data(data: list) -> bool:
        """
        Validates that every element in the list used to deserialize this object is a valid Equation list

        :param data: Exchanges data stored as a list of Equation data elements
        :type data: list
        :return: True if each element in the list is a proper Equation data, False otherwise
        """
        return Equations.validate_deserialize_data(data)

    @classmethod
    def deserialize(cls, data: list):
        """
        Deserializes the Equations list data into an Exchange object.

        :param data: Equations data stored as a list
        :type data: list
        :return: Equation objects stored as an Exchange object
        :rtype: Exchange
        """
        if not Equations.validate_deserialize_data(data):
            raise Exception("Invalid Equations data provided.")
        list_of_equations = [
            Equation.deserialize(equation_data, True) for equation_data in data
        ]
        try:
            return cls(pebble_exchanges=list_of_equations)
        except:
            raise Exception("Invalid Exchange data provided.")

    def serialize(self) -> list:
        """
        Serializes the Exchange data into a list of Equation objects.

        :return: Exchange data stored as a list of equations
        :rtype: list
        """
        return [equation.serialize() for equation in self.pebble_exchanges]


class Exchanges(BaseModel):
    """
    A list of exchange entries
    exchange: list of exchange
    """

    exchanges: List[Exchange] = Field(default_factory=list)

    def put(self, exchange: Exchange) -> None:
        """
        imitating a queue behaviour. Add an Exchange to the end of the list of exchanges.
        """
        self.exchanges.append(exchange)

    def get(self) -> Exchange:
        """
        Imitates a queue behavior. Removes and returns the first Exchange from the list.
        Raises an IndexError if the queue is empty.

        :returns: Exchange that is at the front of the list.
        :rtype: Exchange
        """
        if not self.exchanges:
            raise IndexError("get from empty Exchanges")
        return self.exchanges.pop(0)

    def is_empty(self) -> bool:
        """
        Returns True if the exchanges instances in this Exchanges object is empty, False otherwise.

        :returns: True if the length of the list of exchange instances is 0, False otherwise.
        :rtype: bool
        """
        return len(self.exchanges) == 0

    def have_wallet_n_exchanges(
        self, wallet: PebbleCollection, pebble_exchanges: List[Equation]
    ) -> bool:
        """
        Check if any exchange in the exchanges list has the specified wallet, and same pebble_exchnges.

        :param wallet: The PebbleCollection representing the wallet to check.
        :return: True if any exchange has the given wallet, False otherwise.
        """
        for exchange in self.exchanges:
            if (
                exchange.wallet == wallet
                and exchange.pebble_exchanges == pebble_exchanges
            ):
                return True
        return False

    def exchange_with_wallet(self,wallet: PebbleCollection) -> Optional[Exchange]:
        """
        return the exchange with the same wallet
        :param wallet:
        :return: Exchage that have the wallet, none if there isn't
        """
        for exchange in self.exchanges:
            if exchange.wallet == wallet:
                return exchange
        return None


    def remove_empty_sequences(self) -> None:
        """
        Removes empty exchange sequences from this Exchanges object.
        """
        self.exchanges = [exchange for exchange in self.exchanges if exchange.pebble_exchanges]

def all_possible_exchanges(
    equations: Equations, wallet: PebbleCollection, bank: PebbleCollection
) -> Exchanges:
    """
    Return an Exchanges instance contains all possible exchanges the pass in wallet could make
    that up to exchange of four equations.

    :param equations: the available equations  for exchange
    :param wallet: current wallet of player
    :param bank: current bank
    :return : an exchange contain all possible exchanges
    :rtype: Exchanges
    """

    initial_exchange = Exchange(wallet=wallet, bank=bank, pebble_exchanges=[])
    explored = Exchanges()
    explored.put(initial_exchange)

    exchange_search(initial_exchange, equations,explored)

    explored.remove_empty_sequences()
    return explored

def exchange_search(current_exchange:Exchange, equations: Equations, explored:Exchanges):
    """
    run a search

    :param current_exchange:
    :param equations:
    :param explored:
    :return:
    """

    if len(current_exchange.pebble_exchanges) >= MAX_EXCHANGE_DEPTH:
        return
    possible_exchanges = current_exchange.possible_next_exchange(equations)
    if len(possible_exchanges) == 0:
        return
    for next_exchange in possible_exchanges:
        add_if_better(explored,next_exchange)
        exchange_search(next_exchange,equations,explored)

def add_if_better(explored:Exchanges, new_exchange: Exchange):
    """
    add if the explored does not have the wallet, or pebble exchange of this exchange is less than the pebble_exchange of
    exchange that have the same wallet in the list. Remove the exchange have the same wallet but bigger pebble exchange

    :param explored:
    :param new_exchange:
    """

    same_wallet_exchange = explored.exchange_with_wallet(new_exchange.wallet)
    if same_wallet_exchange:
        if new_exchange.less_pebble_exchange(same_wallet_exchange):
            explored.exchanges.remove(same_wallet_exchange)
            explored.exchanges.append(new_exchange)
    else:
        explored.exchanges.append(new_exchange)
def __update_frontier_nodes(
    frontier: Exchanges, equations: Equations, current_exchange: Exchange
):
    """
    Add possible next level exchanges going from this exchange to the frontier.

    :param frontier: The Exchanges to be explored
    :param equations: All possible equations
    :param current_exchange: The current Exchange being explored
    """
    possible_exchanges = current_exchange.possible_next_exchange(equations)
    for exchange in possible_exchanges:
        next_wallet = exchange.wallet
        next_pebble_exchanges = exchange.pebble_exchanges
        if not frontier.have_wallet_n_exchanges(next_wallet, next_pebble_exchanges):
            frontier.put(exchange)
