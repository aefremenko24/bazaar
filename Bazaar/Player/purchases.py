from copy import copy
from typing import List, Tuple, Callable

from pydantic import BaseModel

from Bazaar.Common.cards import Cards, Card
from Bazaar.Common.pebble import PebbleCollection
from Bazaar.Common.rule_book import RuleBook


class PurchaseSequence(BaseModel):
    """
    Represents the sequence of card purchases.

    :param sequence: sequence of card purchases as a Cards object
    :type sequence: Cards
    """

    sequence: Cards = Cards()
    points: int = 0
    wallet: PebbleCollection = PebbleCollection()
    bank: PebbleCollection = PebbleCollection()

    # TODO: purpose of this? since we already filter in
    def is_purchasable(self, wallet: PebbleCollection) -> bool:
        """
        Checks whether this sequence is affordable given a wallet.

        :param wallet: wallet to check against
        :type wallet: PebbleCollection

        :return: True if the sequence can be purchased with the given wallet, False otherwise
        :rtype: bool
        """
        from Bazaar.Common.rule_book import RuleBook
        if len(self.sequence.cards) == 0:
            return True
        sequence_copy = copy(self)
        next_card = sequence_copy.sequence.pop_card(0)
        if RuleBook.can_purchase_card(next_card, wallet):
            return sequence_copy.is_purchasable(wallet - next_card.pebbles)
        else:
            return False

    def purchase_card(self, card: Card):
        """
        return a new purchase sequence with card added in purchase path,update socre,wallet and bank accordingly.
        The score is calculated based on strategy
        :param card:
        :return:
        """
        from Bazaar.Common.rule_book import RuleBook
        if not RuleBook.can_purchase_card(card, self.wallet):
            return None
        new_cards = Cards(cards=self.sequence.cards.copy())
        new_cards.add_card(card)
        new_score = self.calculate_score_based_on_strategy(card, self.wallet)
        new_wallet, new_bank = card.purchase(self.wallet, self.bank)
        return PurchaseSequence(
            sequence=new_cards, points=new_score, wallet=new_wallet, bank=new_bank
        )

    def calculate_score_based_on_strategy(
        self, card: Card, wallet: PebbleCollection
    ):
        """
        calculate the score based on the strategy

        :param card: cards to be purchase
        :param wallet: player's wallet
        :return: score
        """
        new_score = self.points + RuleBook.score_if_bought(card, wallet)
        return new_score

    def get_purchase_sequence_score(self, wallet: PebbleCollection) -> int:
        """
        Returns the score the player would receive if they bought cards using this sequence.
        0 is returned if the sequence is not purchasable with the given wallet.

        :param wallet: player's wallet
        :type wallet: PebbleCollection
        :return: the score the player would receive if they bought cards using the sequence provided
        :rtype: int
        """
        from Bazaar.Common.rule_book import RuleBook
        wallet_copy = copy(wallet)
        score = 0

        for card in self.sequence.cards:
            if RuleBook.can_purchase_card(card, wallet_copy):
                score += RuleBook.score_if_bought(card, wallet_copy)
                wallet_copy -= card.pebbles
            else:
                break
        return score

    def get_purchase_sequence_remaining_pebbles(
        self, wallet: PebbleCollection
    ) -> PebbleCollection:
        """
        Returns the PebbleCollection the player would have left if they bought cards using this sequence.
        If the wallet provided does not have enough pebbles to buy any one of the cards,
        the original wallet will be returned.

        :param wallet: player's wallet
        :type wallet: PebbleCollection
        :return: the PebbleCollection the player would have left if they bought cards using this sequence
        :rtype: PebbleCollection
        """
        if not self.is_purchasable(wallet):
            return wallet
        wallet_copy = copy(wallet)
        for card in self.sequence.cards:
            wallet_copy -= card.pebbles
        return wallet_copy


class PurchaseSequences(BaseModel):

    sequences: List[PurchaseSequence]

    @staticmethod
    def __get_card_purchase_tree(cards: Cards, wallet: PebbleCollection) -> dict:
        """
        Builds a dictionary representing the tree of all possible card purchase sequences.
        Here, keys are cards and values are dictionaries of tree levels

        :param cards: visible cards available for the players to purchase
        :type cards: Cards
        :param wallet: player's wallet
        :type wallet: PebbleCollection
        :return: dictionary representing the tree of all possible card purchase sequences
        :rtype: dict
        """
        filtered_cards = cards.find_matching_cards(wallet)
        if len(filtered_cards.cards) == 0:
            return {}
        purchase_sequence_tree = {}
        for card_index, card in enumerate(filtered_cards.cards):
            cards_copy = copy(filtered_cards)
            cards_copy.pop_card(card_index)
            remaining_pebbles = wallet - card.pebbles
            recursive_call = PurchaseSequences.__get_card_purchase_tree(
                cards_copy, remaining_pebbles
            )
            purchase_sequence_tree[card] = recursive_call
        return purchase_sequence_tree

    @staticmethod
    def __get_card_purchase_lists(tree=None):
        """
        Returns a list of all possible card purchase sequences using a dictionary derived in _get_card_purchase_tree_

        :param tree: dictionary representing the tree of all possible card purchase sequences
        :type tree: dict
        :return: list of all possible card purchase sequences
        :rtype: List[List[Card]]
        """
        if tree is None:
            tree = {}
        if tree == {}:
            return []
        output_list = []
        for this_card in tree:
            next_call = PurchaseSequences.__get_card_purchase_lists(tree[this_card])
            if len(next_call) == 0:
                output_list.append([this_card])
            else:
                for next_card in next_call:
                    output_list.append([this_card] + next_card)
        return output_list

    @classmethod
    def init_possible_purchase_sequences(cls, cards: Cards, wallet: PebbleCollection):
        """
        Initializes an instance of the PurchaseSequences class with a list of all possible card purchase sequences as a field.
        The list is constructed based on the cards and the player wallet given as arguments

        :param cards: visible cards available for the players to purchase
        :type cards: Cards
        :param wallet: player's wallet
        :type wallet: PebbleCollection

        :return: PurchaseSequences instance
        :rtype: PurchaseSequences
        """
        purchase_tree = PurchaseSequences.__get_card_purchase_tree(
            cards=cards, wallet=wallet
        )
        purchase_lists = PurchaseSequences.__get_card_purchase_lists(tree=purchase_tree)
        purchase_sequence_list = [
            PurchaseSequence(sequence=Cards(cards=purchase_list))
            for purchase_list in purchase_lists
        ]
        return cls(sequences=purchase_sequence_list)

    def get_best_score_card_sequences(self, wallet: PebbleCollection):
        """
        Returns the sequence that produces the highest score from this PurchaseSequences instance.

        :param wallet: player's wallet
        :type wallet: PebbleCollection
        :return: best score, card sequences with the highest score
        :rtype: Tuple[int, PurchaseSequences]
        """
        largest_sequence_score = 0
        filtered_candidates = []
        for seq in self.sequences:
            current_sequence_score = seq.get_purchase_sequence_score(wallet)
            if current_sequence_score == largest_sequence_score:
                filtered_candidates.append(seq)
            elif current_sequence_score > largest_sequence_score:
                largest_sequence_score = current_sequence_score
                filtered_candidates = [seq]

        return (
            largest_sequence_score,
            PurchaseSequences(sequences=filtered_candidates),
        )

    def get_longest_cards_sequences(self):
        """
        Returns the sequences from this PurchaseSequences instance with the highest number of cards purchased.

        :return: max number of cards purchased, list of card sequences that maximize purchases
        :rtype: int Tuple[int, PurchaseSequences]
        """
        largest_sequence_length = 0
        filtered_candidates = []
        for seq in self.sequences:
            current_sequence_length = len(seq.sequence.cards)
            if current_sequence_length == largest_sequence_length:
                filtered_candidates.append(seq)
            elif current_sequence_length > largest_sequence_length:
                largest_sequence_length = current_sequence_length
                filtered_candidates = [seq]

        return (
            largest_sequence_length,
            PurchaseSequences(sequences=filtered_candidates),
        )


def find_all_possible_purchase(
    cards: Cards, wallet: PebbleCollection, bank: PebbleCollection, policy: str
):
    """
    find all possible purchases in
    :param cards:
    :param wallet:
    :param bank:
    :param policy:
    :return:
    """
    initial_purchase = PurchaseSequence(
        sequences=[], points=0, wallet=wallet, bank=bank
    )
    initial_candidate = []
    search_all_possible(cards, initial_purchase, initial_candidate, policy)
    return initial_candidate


def search_all_possible(
    cards: Cards,
    purchase: PurchaseSequence,
    candidates: list[PurchaseSequence],
    policy: str = "purchase-points",
):
    """

    :param cards:
    :param purchase:
    :param candidates:
    :param policy:
    :return:
    """
    filtered_cards = cards.find_matching_cards(purchase.wallet)
    if not len(filtered_cards.cards) == 0:
        for card_index, card in enumerate(filtered_cards.cards):
            cards_copy = copy(filtered_cards)
            cards_copy.pop_card(card_index)
            new_purchase = purchase.purchase_card(card)
            if not new_purchase:
                continue
            add_if_better(candidates, new_purchase, policy)
            search_all_possible(cards_copy, new_purchase, candidates, policy)

def add_if_better(candidates: list[PurchaseSequence], new: PurchaseSequence, policy: str):
    if policy == "purchase-points":
        if not candidates or new.points > candidates[0].points:
            candidates.clear()
            candidates.append(new)
        elif new.points == candidates[0].points:
            if new not in candidates:
                candidates.append(new)
    if policy == "purchase-size":
        if not candidates or len(new.sequence.cards) > len(candidates[0].sequence.cards):
            candidates.clear()
            candidates.append(new)
        elif len(new.sequence.cards) == len(candidates[0].sequence.cards):
            if new not in candidates:
                candidates.append(new)
