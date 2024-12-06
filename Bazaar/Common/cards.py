import random

from pydantic import BaseModel, conlist, model_validator
from typing import Tuple

from Bazaar.Common.data import PEBBLE_COUNT, CARD_REWARDS, MIN_CARDS_NUM, MAX_CARDS_NUM
from Bazaar.Common.game_interface import Board
from Bazaar.Common.pebble import Pebble, PebbleColor, PebbleCollection


class Card(BaseModel):
    """
    A single card. Pebbles represent how much it will cost players to buy this card.
    Happy face appears randomly on each card and awards the player extra points if the card is purchased.

    :param pebbles: pebbles representing the cost of the card
    :type pebbles: PebbleCollection
    :param happy_face: True if the card has a happy face, False otherwise
    :type happy_face: bool
    """

    pebbles: PebbleCollection
    happy_face: bool

    model_config = {"frozen": True}

    @model_validator(mode="before")
    def validate_pebble_count(cls, values):
        """
        Validates that a card should have 5 pebbles.
        """
        pebbles = values.get("pebbles")
        if len(pebbles.pebbles) != PEBBLE_COUNT:
            raise ValueError(f"Card must contain exactly {PEBBLE_COUNT} pebbles.")
        return values

    @staticmethod
    def generate_random():
        """
        Static method. Randomly generates a number of pebbles equal to PEBBLE_COUNT
        and returns a Card instance with those pebbles as a field.

        :returns: a Card instance with randomly generated pebbles
        :rtype: Card
        """
        card_pebbles = PebbleCollection.generate_random(PEBBLE_COUNT)
        happy_face = random.choice([True, False])
        return Card(pebbles=card_pebbles, happy_face=happy_face)

    @staticmethod
    def validate_deserialize_data(data: dict) -> bool:
        """
        Validates that the dictionary used to deserialize this object is valid

        :param data: Card data stored as a dict with "pebbles" and "face?" fields
        :type data: dict
        :return: True if dictionary is valid, False otherwise
        """
        try:
            assert "pebbles" in data and PebbleCollection.validate_deserialize_data(
                data.get("pebbles")
            )
            assert "face?" in data and data.get("face?") in [True, False]
            return True
        except AssertionError:
            return False

    @classmethod
    def deserialize(cls, data: dict):
        """
        Deserializes the Card object from a dictionary

        :param data: Card data stored as a dict with "pebbles" and "face?" fields
        :type data: dict
        :return: Card object deserialized from a dictionary
        :rtype: Card
        """
        if not Card.validate_deserialize_data(data):
            raise Exception("Invalid Card data provided.")
        pebbles = PebbleCollection.deserialize(data.get("pebbles"))
        happy_face = data.get("face?")
        return Card(pebbles=pebbles, happy_face=happy_face)

    def serialize(self) -> dict:
        """
        Converts this card to a dictionary representation.
        Keys are "pebbles" and "happy_face" and values are a list of pebbles and a boolean, respectively.

        :returns: a dictionary representation of the card
        :rtype: dict
        """
        return {"pebbles": self.pebbles.serialize(), "face?": self.happy_face}

    def draw(self, board: Board):
        """
        Draws this Card on the given Board instance.

        :param board: a Board instance to draw the card on
        """
        card_dictionary = self.serialize()
        board.draw_card(
            card_dictionary.get("pebbles"), card_dictionary.get("happy_face")
        )

    def purchase(
        self, player_wallet: PebbleCollection, bank: PebbleCollection
    ) -> Tuple[PebbleCollection, PebbleCollection]:
        """
        Processes a card purchase using the player wallet and bank provided.

        :param player_wallet: player wallet
        :type player_wallet: PebbleCollection
        :param bank: bank pebbles
        :type bank: PebbleCollection
        :return: player wallet and bank after the transaction
        :rtype: Tuple[PebbleCollection, PebbleCollection]
        """
        player_pebbles_copy = PebbleCollection(pebbles=tuple(player_wallet.pebbles))
        bank_copy = PebbleCollection(pebbles=tuple(bank.pebbles))
        player_pebbles_copy = player_pebbles_copy - self.pebbles
        bank_copy = bank_copy + self.pebbles
        return (player_pebbles_copy, bank_copy)

    def __str__(self):
        """
        Converts this Card to a string representation.
        Example: for a Card object with 2 white, 1 yellow, 2 red pebbles, and a happy face,
        the string representation will look like:
        "Card: white white yellow red red 😊"

        :returns: a string representation of the card
        :rtype: str
        """
        return f"Card: {' '.join(str(pebble) for pebble in self.pebbles.pebbles)} {'😊' if self.happy_face else ''}"

    def __eq__(self, other) -> bool:
        """
        Overrides the default implementation of equals for equality of two cards.

        :param other: other instance of the Card class
        :returns: True if this Card has the same pebbles and happy face as the other Card, False otherwise
        :rtype: bool
        """
        if not isinstance(other, Card):
            return False
        pebbles_same = self.pebbles == other.pebbles
        happy_face_same = self.happy_face == other.happy_face
        return pebbles_same and happy_face_same

    def __hash__(self):
        """
        Overrides the default hash method to properly calculate hash values for this object.

        :returns: hashable object for this Card object, accounting for pebbles and happy_face fields
        """
        return hash((self.pebbles, self.happy_face))

    def __lt__(self, other) -> bool:
        """
        Overrides the default implementation of less than comparison between two cards.

        :param other: other instance of the Card class.
        :returns: True if this and other cards don’t both come with a face and this card doesn’t display one (other card has a face)
        :rtype: bool
        """
        other_card_displays_face = other.happy_face
        if other_card_displays_face and not self.happy_face:
            return True
        else:
            return self.pebbles < other.pebbles


class Cards(BaseModel):
    """
    Deck of cards.

    :param cards: list of Card instances represented as a conlist
    :type cards: conlist[Card]
    """

    cards: conlist(Card, min_length=MIN_CARDS_NUM, max_length=MAX_CARDS_NUM) = []

    @classmethod
    def generate_random(cls, count: int = MAX_CARDS_NUM):
        """
        Class method. Randomly generates a number of cards equal to the count argument
        and returns a Cards object with the generated Card objects as a field.

        :param count: number of cards to generate
        :type count: int
        :returns: a Cards object with randomly generated Card objects
        :rtype: Cards
        """
        cards = []
        for _ in range(count):
            card = Card.generate_random()
            cards.append(card)
        return cls(cards=cards)

    def find_matching_cards(self, player_pebbles: PebbleCollection):
        """
        Returns the subset of all these cards that can be bought with the given pebbles
        :param pebbles: The dictionary of pebbles in the player's wallet
        :return: Cards instance with filtered Card object list as a field
        :rtype: Cards
        """
        from Bazaar.Common.rule_book import RuleBook

        filtered_cards = [
            card
            for card in self.cards
            if RuleBook.can_purchase_card(card, player_pebbles)
        ]
        return Cards(cards=filtered_cards)

    def draw(self, board: Board):
        """
        Draws this Cards object on the given Board instance.

        :param board: a Board instance to draw the card on
        """
        for card in self.cards:
            card.draw(board)

    def is_empty(self) -> bool:
        """
        Returns True if the list of Card instances in this Cards object is empty, False otherwise.

        :returns: True if the length of the list of Card instances is 0, False otherwise.
        :rtype: bool
        """
        return len(self.cards) == 0

    def sorted(self):
        """
        Returns a new Cards object with the list of cards field sorted so that cards with smaller wallet or no
        appearing happy face come first.

        :returns: Cards object with cards field sorted
        :rtype: Cards
        """
        sorted_card_list = sorted(self.cards)
        return Cards(cards=sorted_card_list)

    def __str__(self):
        """
        Converts this Cards object to a string representation by appending string representation of Card on
        the consecutive line. See __str__ method in Card for example of visual representation.

        :returns: a string representation of this Cards object
        :rtype: str
        """
        out_string = ""
        for card in self.cards:
            out_string += f"{card}" + "\n"
        return out_string

    def __lt__(self, other):
        """
        Returns True if this card sequence is less than the other card sequence of the same length.

        :param other: card sequence to compare to
        :type other: Cards
        :returns: True if this card sequence is less than the other card sequence, False otherwise
        :rtype: bool
        """
        if len(self.cards) < len(other.cards):
            return True
        if len(self.cards) > len(other.cards):
            return False
        if len(self.cards) == len(other.cards):
            for card_index, card in enumerate(self.cards):
                if self.cards[card_index] < other.cards[card_index]:
                    return True
        return False

    def __contains__(self, card: Card):
        return card in self.cards

    @staticmethod
    def validate_deserialize_data(data: list) -> bool:
        """
        Validates that every element in the list used to deserialize this object is a valid Card data representation

        :param data: Cards data stored as a list of Card data elements
        :type data: list
        :return: True if each element in the list is a valid Card data dict, False otherwise
        """
        try:
            assert all([Card.validate_deserialize_data(element) for element in data])
            return True
        except AssertionError:
            return False

    @classmethod
    def deserialize(cls, data: list):
        """
        Deserializes the Card list data into a Cards object.

        :param data: Cards data stored as a list
        :type data: list
        :return: Card objects stored as a Cards object
        :rtype: Cards
        """
        if not Cards.validate_deserialize_data(data):
            raise Exception("Invalid Cards data provided.")
        list_of_cards = [Card.deserialize(card_data) for card_data in data]
        newCardCollection = cls(cards=list_of_cards)
        return newCardCollection

    def serialize(self) -> list:
        """
        Serializes the Cards data into a list of Card objects.

        :return: Cards data stored as a list
        :rtype: list
        """
        return [card.serialize() for card in self.cards]

    def add_card(self, card: Card):
        """
        Adds a card to the list of cards stored in this Cards class instance.

        :param card: card to add
        :type card: Card
        """
        self.cards.append(card)

    def pop_card(self, index: int) -> Card:
        """
        Pops a card at a given index from the list of cards stored in this Cards class instance.

        :param index: index at which to pop the card
        :type index: int
        """
        return self.cards.pop(index)
