from typing import List, Set, Optional
from xml.etree.ElementInclude import include

from pydantic import BaseModel, conint
import queue
from copy import copy

from Bazaar.Common.turn_state import TurnState
from Bazaar.Player.exchanges import *
from Bazaar.Player.purchases import *


class Strategy(BaseModel):
    """
    Class representing the strategy of the AI player.
    Currently,  there are two greedy strategies, one pick for card purchase that maximize the number of points, the
    other pick for maximize number of cards

    equations: equations for exchange
    cards: cards for purchase
    """

    equations: Equations
    turn_state: TurnState
    policy: str
    points_received: int = 0
    num_cards_bought: int = 0

    def tie_break_card_purchase(
        self, candidates: List[Tuple[Exchange, PurchaseSequence]]
    ):
        """
        Perform a tie-breaking process on a given candidates based on purchase sequences. Return anytime if there is
        only one candidates left
        First, it performs tie breaking of highest number of points.
        Second, it performs tie breaking of  largest number of remaining pebbles in the player’s wallet.
        Then it  performs tie breaking of smallest wallet in exchange
        Finally, it performs tie breaking of smallest sequence of cards
        :param candidates: list of best so-far candidate
        :type candidates:List[Tuple[Exchange, PurchaseSequence]]
        :return: candidates that pass tie-breaks
        :rType: List[Tuple[Exchange, PurchaseSequence]]
        """
        while len(candidates) > 1:
            candidates = self.__filter_card_by_highest_score(candidates)
            if len(candidates) == 1:
                break
            candidates = self.__filter_card_sequences_by_remaining_pebbles(candidates)
            if len(candidates) == 1:
                break
            candidates = self.__filter_card_sequences_by_wallet(candidates)
            if len(candidates) == 1:
                break
            candidates = self.__filter_card_sequences_by_lengths(candidates)

        return candidates

    def __filter_card_by_highest_score(
        self, candidates: List[Tuple[Exchange, PurchaseSequence]]
    ) -> List[Tuple[Exchange, PurchaseSequence]]:
        """
        Filters the candidates based on the highest score .eliminates any candidates that do not have the highest scores.

        :param candidates: list of best so-far candidates
        :type candidates: List[Tuple[Exchange, PurchaseSequence]]
        :return: Filtered list of candidates with the highest score
        :rtype: List[Tuple[Exchange, PurchaseSequence]]
        """
        highest_score = 0
        filtered_candidates = []

        for exchange, sequence in candidates:
            current_score = sequence.get_purchase_sequence_score(exchange.wallet)
            if current_score == highest_score:
                filtered_candidates.append((exchange, sequence))
            elif current_score > highest_score:
                highest_score = current_score
                filtered_candidates = [(exchange, sequence)]
        return filtered_candidates

    def __filter_card_sequences_by_remaining_pebbles(
        self, candidates: List[Tuple[Exchange, PurchaseSequence]]
    ) -> List[Tuple[Exchange, PurchaseSequence]]:
        """
        Filters the candidates based on the wallet the player will be left with after purchasing it.

        :param candidates: list of best so-far candidate
        :type candidates: List[Tuple[Exchange, PurchaseSequence]]
        :param wallet: current player's wallet
        :type wallet: PebbleCollection
        :return: Filtered list of candidates that leave the player with the most pebbles
        :rtype: List[Tuple[Exchange, PurchaseSequence]]
        """
        best_wallet_remaining = 0
        filtered_candidates = []
        for exchange, sequence in candidates:
            remaining_wallet = sequence.get_purchase_sequence_remaining_pebbles(
                exchange.wallet
            )
            if len(remaining_wallet.pebbles) == best_wallet_remaining:
                filtered_candidates.append((exchange, sequence))
            elif len(remaining_wallet.pebbles) > best_wallet_remaining:
                best_wallet_remaining = len(remaining_wallet.pebbles)
                filtered_candidates = [(exchange, sequence)]
        return filtered_candidates

    def __filter_card_sequences_by_wallet(
        self, candidates: List[Tuple[Exchange, PurchaseSequence]]
    ) -> List[Tuple[Exchange, PurchaseSequence]]:
        """
        Filters the candidates based on the smallest wallet.

        :param candidates: list of best so-far candidates
        :type candidates: List[Tuple[Exchange, PurchaseSequence]]
        :return: Filtered list of candidates with the smallest wallet
        :rtype: List[Tuple[Exchange, PurchaseSequence]]
        """
        first_exchange = candidates[0]
        smallest_wallet = first_exchange[0].wallet
        filtered_candidates = []

        for exchange, sequence in candidates:
            current_wallet = exchange.wallet
            if current_wallet == smallest_wallet:
                filtered_candidates.append((exchange, sequence))
            elif current_wallet < smallest_wallet:
                smallest_wallet = current_wallet
                filtered_candidates = [(exchange, sequence)]
        return filtered_candidates

    def __filter_card_sequences_by_lengths(
        self, candidates: List[Tuple[Exchange, PurchaseSequence]]
    ) -> List[Tuple[Exchange, PurchaseSequence]]:
        """
        Filters the candidates based on the smallest card sequence.

        :param candidates: list of best so-far candidates
        :type candidates: List[Tuple[Exchange, PurchaseSequence]]
        :return: Filtered list of candidates with the smallest card sequence
        :rtype: List[Tuple[Exchange, PurchaseSequence]]
        """
        smallest_sequence_length = min(
            [sequence.sequence.cards for _, sequence in candidates]
        )

        filtered_candidates = [
            (exchange, sequence)
            for exchange, sequence in candidates
            if sequence.sequence.cards == smallest_sequence_length
        ]

        return filtered_candidates

    def tie_break_exchange_and_purchase(
        self, candidates: Optional[List[Tuple[Exchange, PurchaseSequence]]]
    ):
        """
        Perform a tie-breaking process on a given candidates based on purchase sequences. Return anytime if there is
        only one candidates left
        First, it picks the ones that need the smallest number of trades
        Then it performs tie breaking of based one card purchase
        Finally, it pick the one that uses the smallest pebble-exchanges.
        :param candidates: list of best so-far candidate
        :type candidates:List[Tuple[Exchange, PurchaseSequence]]
        :return: candidates that pass tie-breaks
        :rType: Tuple[Exchange, PurchaseSequence]
        """
        if len(candidates) == 0:
            return None
        while len(candidates) > 1:
            candidates = self.__filter_smallest_exchange_length(candidates)
            if len(candidates) == 1:
                break
            candidates = self.tie_break_card_purchase(candidates)
            if len(candidates) == 1:
                break
            candidates = self.filter_smallest_exchange_pebble(candidates)
        return candidates[0]

    def __filter_smallest_exchange_length(
        self, candidates: List[Tuple[Exchange, PurchaseSequence]]
    ) -> List[Tuple[Exchange, PurchaseSequence]]:
        """
        Filters the candidates by selecting the ones with the smallest number of pebble_exchanges,

        :param candidates:  list of best so-far candidates
        :type candidates: List[Tuple[Exchange, PurchaseSequence]]
        :return: Filtered list of candidates with the smallest exchange sequence length
        :rtype: List[Tuple[Exchange, PurchaseSequence]]
        """
        smallest_sequence_length = min(
            len(exchange.pebble_exchanges) for exchange, purchase in candidates
        )
        filtered_candidates = [
            candidate
            for candidate in candidates
            if len(candidate[0].pebble_exchanges) == smallest_sequence_length
        ]
        return filtered_candidates

    def __filter_smallest_pebble_exchange(
        self, candidates: List[Tuple[Exchange, PurchaseSequence]]
    ) -> List[Tuple[Exchange, PurchaseSequence]]:
        """
        Filters the candidates by selecting the ones with the smallest pebble_exchanges in exchange

        :param candidates:  list of best so-far candidates
        :type candidates: List[Tuple[Exchange, PurchaseSequence]]
        :return: Filtered list of candidates with the smallest pebble exchanges
        :rtype: List[Tuple[Exchange, PurchaseSequence]]
        """

        exchanges_with_smallest_pebbles = candidates[0]
        filtered_candidates = []

        for exchange, sequence in candidates:
            if exchange.less_pebble_exchange(exchanges_with_smallest_pebbles):
                exchanges_with_smallest_pebbles = exchange
                filtered_candidates = [(exchange, sequence)]
        return filtered_candidates

    def __populate_exchange_n_purchase(
        self, exchange: Exchange, purchase_sequences: list[PurchaseSequence]
    ) -> list[tuple[Exchange, PurchaseSequence]]:
        """
        Populates a list of tuples, each containing an exchange and a purchase sequence from the pass in purchase_sequnces.

        :param exchange: The current exchange
        :type exchange: Exchange
        :param purchase_sequences: PurchaseSequences conatain a list of purchase sequences to pair with the exchange
        :type purchase_sequences: list(PurchaseSequence)
        :return: A list of tuples, each containing the exchange and a purchase sequence
        :rtype: List[Tuple[Exchange, PurchaseSequence]]
        """
        exchange_n_purchase = []
        for purchase_sequence in purchase_sequences:
            exchange_n_purchase.append((exchange, purchase_sequence))
        return exchange_n_purchase

    def get_purchase(self, turn_state: TurnState) -> PurchaseSequence:
        """
        After player have made the exchange, find the best card purchase sequences
        """
        player_wallet = turn_state.active_player_wallet
        bank = turn_state.bank
        cards = turn_state.cards
        return self.best_purchase(bank, cards, player_wallet)

    def best_purchase(self, bank, cards, player_wallet) -> PurchaseSequence:
        """
        Find the best purchase for this bank and wallet.
        :param bank: game bank
        :param cards: visible cards
        :param player_wallet: player's wallet
        :return: best purchase
        :rtype: PurchaseSequence
        """
        candidates = find_all_possible_purchase(cards, player_wallet, bank, self.policy)
        if not candidates:
            return PurchaseSequence(wallet=player_wallet, bank=bank)
        if len(candidates) == 1:
            return candidates[0]
        if len(candidates) > 1:
            exchange_purchase_set = self.__populate_exchange_n_purchase(
                Exchange(), candidates
            )
            winner = self.tie_break_card_purchase(exchange_purchase_set)[0]
            return winner[1]

    def get_trade_purchase(self) -> Optional[tuple[Exchange, PurchaseSequence]]:
        """
        Plays the player's turn by finding the best exchange and purchase sequence based on the current wallet and bank.
        It first finds all possible exchange, if it can not perform any exchanges, then check if the bank is empty for
        drawing a pebble

        :param wallet: The current wallet for purchase and exchange
        :type wallet: PebbleCollection
        :param bank: The current bank for purchase and exchange
        :type bank: PebbleCollection
        :param max_points: True if prioritize maximum points,or  false to maximize the number of cards
        :type max_points: bool
        :return: Best exchange and purchase sequence after evaluation,empty exchange if draw pebble, None if skip
        :rtype: Optional[Tuple[Exchange, PurchaseSequence]]
        """
        player_wallet = self.turn_state.active_player_wallet
        bank = self.turn_state.bank
        all_exchanges = all_possible_exchanges(self.equations, player_wallet, bank)
        if not all_exchanges.exchanges:
            if len(bank.pebbles) == 0:
                return None
            return Exchange(bank=bank, player_wallet=player_wallet), PurchaseSequence(bank=bank, wallet=player_wallet)
        candidates = []
        for exchange in all_exchanges.exchanges:
            best_purchase = self.best_purchase(
                exchange.bank, self.turn_state.cards, exchange.wallet
            )
            if best_purchase:
                self.add_if_better_exchange_purchase(candidates, (exchange, best_purchase))
        if not candidates:
            return Exchange(bank=bank, player_wallet=player_wallet), PurchaseSequence(bank=bank, wallet=player_wallet)
        rules, cards = self.tie_break_exchange_and_purchase(candidates)
        self.points_received = cards.points
        return rules, cards

    def add_if_better_exchange_purchase(
        self,
        candidates: List[Tuple[Exchange, PurchaseSequence]],
        new: Tuple[Exchange, PurchaseSequence],
    ):
        """
        Return the new tuple as candidates if the points obtained after purchase are higher, append to existing candidates if equal.

        :param candidates: existing candidates
        :type candidates: list[tuple[Exchange, PurchaseSequence]]
        :param new: new exchange and purchase sequence to be added
        :type new: Tuple[Exchange, PurchaseSequence]
        :return: new tuple or existing one with new candidate appended
        :rtype: Tuple[Exchange, PurchaseSequence]
        """
        if self.policy == "purchase-points":
            if not candidates or new[1].points > candidates[0][1].points:
                candidates.clear()
                candidates.append(new)
            elif new[1].points == candidates[0][1].points:
                candidates.append(new)
        elif self.policy == "purchase-size":
            if not candidates or len(new[1].sequence.cards) > len(candidates[0][1].sequence.cards):
                candidates.clear()
                candidates.append(new)
            elif len(new[1].sequence.cards) == len(candidates[0][1].sequence.cards):
                if new not in candidates:
                    candidates.append(new)
