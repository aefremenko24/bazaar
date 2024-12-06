from typing import List, Dict

from pydantic import BaseModel

from Bazaar.Common.pebble import PebbleCollection
from game_interface import DrawableComponent
from Bazaar.Common.cards import Cards


class TurnState(BaseModel, DrawableComponent):
    """
    This data representation includes the bank’s pebbles,
    the active player’s state, and the current score of the remaining players.
    """

    bank: PebbleCollection
    active_player_wallet: PebbleCollection
    active_player_score: int
    player_scores: List[int]
    cards: Cards

    def to_dict(self):
        pass

    def draw(self, board):
        bank_dic = {pebble.color: count for pebble, count in self.bank.items()}
        board.draw_bank(bank_dic)
        self.active_player.draw(board)
        board.draw_score(self.player_scores)

    @staticmethod
    def validate_deserialize_data(data: dict) -> bool:
        """
        Validates JSON dictionary used to deserialize the turn state object.

        :param data: turn state data stored as a dictionary
        :type data: dict
        :return: True if data contains "bank", "cards", "active", and "scores" field and those fields are valid according to
        validate_deserialize_data in their class, False otherwise
        """
        try:
            assert "bank" in data and PebbleCollection.validate_deserialize_data(
                data.get("bank")
            ), "Bank data could not be validated."
            assert "cards" in data and Cards.validate_deserialize_data(
                data.get("cards")
            ), "Cards data could not be validated."
            assert "active" in data, "Active player data could not be validated."
            assert "scores" in data and all(
                [isinstance(score, int) and score >= 0 for score in data.get("scores")]
            ), "Scores data could not be validated."
            return True
        except AssertionError as e:
            print(e)
            return False

    @classmethod
    def deserialize(cls, data: dict):
        """
        Deserializes the turn state data into a GameState object.

        :param data: turn state data stored as a dictionary
        :type data: dict
        :return: turn state data stored as a TurnState object
        :rtype: TurnState
        """
        if not TurnState.validate_deserialize_data(data):
            raise Exception("Invalid turn state data provided.")
        bank = PebbleCollection.deserialize(data.get("bank"))
        cards = Cards.deserialize(data.get("cards"))
        active_player_score = data.get("active").get("score")
        active_player_wallet = PebbleCollection.deserialize(
            data.get("active").get("wallet")
        )
        scores = data.get("scores")
        newGameState = cls(
            bank=bank,
            active_player_wallet=active_player_wallet,
            active_player_score=active_player_score,
            player_scores=scores,
            cards=cards,
        )
        return newGameState

    def serialize(self) -> dict:
        """
        Serializes the turn state data into a dictionary.

        :return: turn state data stored as a dictionary
        :rtype: dict
        """
        bank = self.bank.serialize()
        cards = self.cards.serialize()
        active = {
            "wallet": self.active_player_wallet.serialize(),
            "score": self.active_player_score,
        }
        return {
            "bank": bank,
            "cards": cards,
            "active": active,
            "scores": self.player_scores,
        }
