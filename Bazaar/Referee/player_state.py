from typing import Dict, Union

from attr import dataclass
from pydantic import BaseModel

from Bazaar.Common.cards import Cards
from Bazaar.Common.game_interface import DrawableComponent, Board
from Bazaar.Common.pebble import Pebble, PebbleCollection
from Bazaar.Player.mechanism import Mechanism
from Bazaar.Server.player import ProxyPlayer

@dataclass
class PlayerState(DrawableComponent):
    """Represents information about a player known to the referee."""

    cards: Cards = Cards()
    wallet: PebbleCollection = PebbleCollection()
    score: int = 0
    cards: list = []
    actor: Mechanism = None

    def draw(self, board: Board):
        board.draw_playerstate(self.actor.name, self.wallet, self.score)

    @staticmethod
    def validate_deserialize_data(data: dict) -> bool:
        """
        Validates that the dictionary used to deserialize this object is valid

        :param data: PlayerState data stored as a dict with "wallet" and "score" fields
        :type data: dict
        :return: True if dictionary is valid, False otherwise
        """
        try:
            assert "wallet" in data and PebbleCollection.validate_deserialize_data(
                data.get("wallet")
            )
            # assert "cards" in data and Cards.validate_deserialize_data(
            #     data.get("cards")
            # )
            assert "score" in data and data.get("score", -1) >= 0
            return True
        except AssertionError:
            return False

    @classmethod
    def deserialize(cls, data: dict):
        """
        Deserializes the PlayerState object from a dictionary

        :param data: PlayerState dara stored as a dict with "wallet" and "score" fields
        :type data: dict
        :return: PlayerState object deserialized from a dictionary
        :rtype: PlayerState
        """
        if not PlayerState.validate_deserialize_data(data):
            raise Exception("Invalid PlayerState data provided.")
        wallet = PebbleCollection.deserialize(data.get("wallet"))
        score = data.get("score")
        cards = Cards.deserialize(data.get("cards")) if data.get("cards") else None
        return cls(wallet=wallet, score=score, cards=cards)

    def serialize(self) -> dict:
        """
        Converts this card to a dictionary representation.
        Keys are "pebbles" and "happy_face" and values are a list of pebbles and a boolean, respectively.

        :returns: a dictionary representation of the card
        :rtype: dict
        """
        return {"wallet": self.wallet.serialize(), "score": self.score}
