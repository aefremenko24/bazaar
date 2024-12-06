from collections import deque, Counter
import copy
from copy import copy
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict

import os, sys

from Bazaar.Common.equations import Equations
from Bazaar.Player.mechanism import Mechanism

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from Bazaar.Common.game_interface import Board, DrawableComponent

from Bazaar.Common.cards import Cards
from Bazaar.Common.pebble import Pebble, PebbleCollection
from Bazaar.Common.turn_state import TurnState
from Bazaar.Referee.player_state import PlayerState


class GameState(BaseModel, DrawableComponent):
    """Stores information about the current game."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    equations: Optional[Equations]
    bank: PebbleCollection = PebbleCollection()
    invisible_deck: Cards
    visibles: Cards
    players: deque[
        PlayerState
    ]  # players in play order. The player in 0th index is active

    def is_bank_empty(self) -> bool:
        """Is the bank empty?"""
        return not self.bank.pebbles

    def can_any_player_buy_any_card(self):
        for player in self.players:
            filtered_cards = self.invisible_deck.find_matching_cards(player.wallet)
            if len(filtered_cards.cards) == 0:
                return False
        return True

    def kick_active_player(self) -> PlayerState:
        """
        Kicks the active player.

        :return: player that was just kicked
        :rtype: PlayerState
        """
        return self.players.popleft()

    def kick_player_by_actor(self, actor: Mechanism):
        """
        Kicks the player that has a provided actor.

        :return: kicked player
        :rtype: PlayerState
        """
        for player_index, player in enumerate(self.players):
            if player.actor.name == actor.name:
                self.players.remove(player)
                return player
        return None

    def player_draw_pebble(self):
        """
        Awards the active player a random pebble when requested.

        :return: True if the pebble was successfully awarded, False otherwise (the bank is out of pebbles)
        :rtype: bool
        """
        pebble = self.bank.draw_pebble()
        if not pebble:
            return False
        self.players[0].wallet.add_pebble(pebble)
        return True

    def extract_turnstate(self) -> TurnState:
        """
        Returns data about the next turn of the game.
        """
        remaining_players = copy(self.players)
        current_player = remaining_players.popleft()
        return TurnState(
            bank=self.bank,
            active_player_wallet=current_player.wallet,
            active_player_score=current_player.score,
            player_scores=[player.score for player in remaining_players],
            cards=self.visibles,
        )

    def get_active_player(self) -> PlayerState:
        """
        Get active player of the current turn
        :return: active player
        :rtype: PlayerState
        """
        return self.players[0]


    def next_turn(self):
        """
        change the active player to next player
        """
        self.players.rotate(-1)

    @staticmethod
    def validate_deserialize_data(data: dict) -> bool:
        """
        Validates JSON dictionary used to deserialize the game state object.

        :param data: game data stored as a dictionary
        :type data: dict
        :return: True if data contains "bank", "visibles", "cards", and "players" field and those fields are valid according to
        validate_deserialize_data in their class, False otherwise
        """
        try:
            assert "bank" in data and PebbleCollection.validate_deserialize_data(
                data.get("bank")
            ), "Invalid bank data provided."
            assert "visibles" in data and Cards.validate_deserialize_data(
                data.get("visibles")
            ), "Invalid visible cards data provided."
            assert "cards" in data and Cards.validate_deserialize_data(
                data.get("cards")
            ), "Invalid cards data provided."
            assert "players" in data and all(
                PlayerState.validate_deserialize_data(player)
                for player in data.get("players")
            ), "Invalid players data provided."
            return True
        except AssertionError:
            return False

    @classmethod
    def deserialize(cls, data: dict, equations: Equations = None) -> "GameState":
        """
        Deserializes the game state data into a GameState object.

        :param data: game data stored as a dictionary
        :type data: dict
        :return: game state data stored as a GameState object
        :rtype: GameState
        """
        if not GameState.validate_deserialize_data(data):
            raise Exception("Invalid game state data provided.")
        bank = PebbleCollection.deserialize(data.get("bank"))
        visibles = Cards.deserialize(data.get("visibles"))
        cards = Cards.deserialize(data.get("cards"))
        players = deque(
            [PlayerState.deserialize(player) for player in data.get("players")]
        )
        newGameState = cls(
            bank=bank, visibles=visibles, invisible_deck=cards, players=players, equations=equations
        )
        return newGameState

    def serialize(self) -> dict:
        """
        Serializes the game state data into a dictionary.

        :return: game state data stored as a dictionary
        :rtype: dict
        """
        bank = self.bank.serialize()
        visibles = self.visibles.serialize()
        cards = self.invisible_deck.serialize()
        players = [player.serialize() for player in self.players]
        return {"bank": bank, "visibles": visibles, "cards": cards, "players": players}

    def draw_bank(self, board: Board):
        board.draw_bank(self.bank)

    def draw_deck(self, board: Board):
        self.visibles.draw(board)

    def draw(self, board: Board):
        self.draw_deck(board)
        self.draw_bank(board)
        for player in self.players:
            player.draw(board)

    def fill_actors(self, actors: "List[Mechanism]") -> bool:
        if len(actors) != len(self.players):
            return False
        for player_index in range(len(self.players)):
            self.players[player_index].actor = actors[player_index]
        return True
