import unittest
from collections import deque

from Bazaar.Common.cards import Card
from Bazaar.Common.pebble import *
from game_state import *
from game_state_board import GameStateBoard
from player_state import PlayerState
from Bazaar.Common.vertical_board import SingleBoard

BANK = {
    Pebble(color=PebbleColor.RED): 25,
    Pebble(color=PebbleColor.BLUE): 25,
    Pebble(color=PebbleColor.GREEN): 25,
    Pebble(color=PebbleColor.YELLOW): 25,
    Pebble(color=PebbleColor.WHITE): 25,
}
EMPTY_BANK = {
    Pebble(color=PebbleColor.RED): 0,
    Pebble(color=PebbleColor.BLUE): 0,
    Pebble(color=PebbleColor.GREEN): 0,
    Pebble(color=PebbleColor.YELLOW): 0,
    Pebble(color=PebbleColor.WHITE): 0,
}
wallet_1 = {Pebble(color=PebbleColor.BLUE): 1}
wallet_2 = {
    Pebble(color=PebbleColor.RED): 2,
    Pebble(color=PebbleColor.GREEN): 2,
    Pebble(color=PebbleColor.YELLOW): 2,
    Pebble(color=PebbleColor.WHITE): 1,
}
player_1 = PlayerState(id=1, wallet=wallet_1, score=5)
player_2 = PlayerState(id=2, wallet=wallet_2, score=4)
won_player = PlayerState(id=3, wallet=wallet_1, score=21)
players = deque([player_1, player_2, won_player])
players2 = deque([player_2, won_player])
card1 = Card(
    pebbles=[
        Pebble(color=PebbleColor.RED),
        Pebble(color=PebbleColor.GREEN),
        Pebble(color=PebbleColor.RED),
        Pebble(color=PebbleColor.GREEN),
        Pebble(color=PebbleColor.YELLOW),
    ]
)
card2 = Card(
    pebbles=[
        Pebble(color=PebbleColor.GREEN),
        Pebble(color=PebbleColor.GREEN),
        Pebble(color=PebbleColor.WHITE),
        Pebble(color=PebbleColor.WHITE),
        Pebble(color=PebbleColor.WHITE),
    ]
)
CARDSMILE3 = Card(
    pebbles=[
        Pebble(color=PebbleColor.GREEN),
        Pebble(color=PebbleColor.BLUE),
        Pebble(color=PebbleColor.RED),
        Pebble(color=PebbleColor.WHITE),
        Pebble(color=PebbleColor.WHITE),
    ],
    happy_face=True,
)
cards = Cards(cards=[card1, card2, CARDSMILE3, CARDSMILE3])
game_state_1 = GameState(bank=BANK, deck=cards, players=players)
game_state_2 = GameState(bank=BANK, deck=cards, players=players2)
SCORE = [1, 2, 3, 5, 1, 2, 20]
TURNSTATE = TurnState(bank=BANK, active_player=player_1, player_scores=SCORE)
SINGLEBOARD = SingleBoard()
GAMEBOARD = GameStateBoard()


class GameStateGraphicTest(unittest.TestCase):

    def testDrawBank(self):
        SINGLEBOARD.create_canvas()
        game_state_1.draw_bank(SINGLEBOARD)
        SINGLEBOARD.show()

    def testDrawActivePlayerState(self):
        SINGLEBOARD.create_canvas()
        game_state_1.draw_active_player(SINGLEBOARD)
        SINGLEBOARD.show()

    def testDrawActivePlayerState2(self):
        SINGLEBOARD.create_canvas()
        game_state_2.draw_active_player(SINGLEBOARD)
        SINGLEBOARD.show()

    def testDrawScore(self):
        SINGLEBOARD.create_canvas()
        SINGLEBOARD.draw_score(SCORE)
        SINGLEBOARD.show()

    def testDrawTurnState(self):
        SINGLEBOARD.create_canvas()
        TURNSTATE.draw(SINGLEBOARD)
        SINGLEBOARD.show()

    """
    testing game state Board below
    """

    def testGSDrawBank(self):
        GAMEBOARD.create_canvas()
        game_state_1.draw_bank(GAMEBOARD)
        GAMEBOARD.show()

    def testGSDrawActivePlayerState(self):
        GAMEBOARD.create_canvas()
        game_state_1.draw_active_player(GAMEBOARD)
        GAMEBOARD.show()

    def testGSDrawActivePlayerState2(self):
        GAMEBOARD.create_canvas()
        game_state_2.draw_active_player(GAMEBOARD)
        GAMEBOARD.show()

    def testGSDrawCards(self):
        GAMEBOARD.create_canvas()
        game_state_2.draw_deck(GAMEBOARD)
        GAMEBOARD.show()

    def testGSDRAW(self):
        GAMEBOARD.create_canvas()
        game_state_2.draw(GAMEBOARD)
        GAMEBOARD.show()
