import unittest
from collections import deque

from Bazaar.Common.cards import Card
from Bazaar.Common.pebble import *
from game_state import *
from player_state import PlayerState


class TestGameState(unittest.TestCase):

    bank = {
        Pebble(color=PebbleColor.RED): 25,
        Pebble(color=PebbleColor.BLUE): 25,
        Pebble(color=PebbleColor.GREEN): 25,
        Pebble(color=PebbleColor.YELLOW): 25,
        Pebble(color=PebbleColor.WHITE): 25,
    }
    empty_bank = {
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
    cards = Cards(cards=[card1, card2])
    scores = [4, 21, 5]
    game_state_1 = GameState(bank=bank, deck=cards, players=players)

    def testIsGameOver(self):
        # players kicked
        players = deque()
        game_state_1 = GameState(bank=self.bank, deck=self.cards, players=players)
        self.assertTrue(game_state_1.is_game_over())

        # there is a player
        players = deque([self.player_1])
        game_state_1 = GameState(bank=self.bank, deck=self.cards, players=players)
        self.assertFalse(game_state_1.is_game_over())

        # the last player won
        players = deque([self.player_1, self.won_player])
        game_state_1 = GameState(bank=self.bank, deck=self.cards, players=players)
        self.assertTrue(game_state_1.is_game_over())

        # no more cards
        cards = Cards(cards=[])
        game_state_1 = GameState(bank=self.bank, deck=cards, players=players)
        self.assertTrue(game_state_1.is_game_over())

        # bank is empty
        game_state_1 = GameState(bank=self.empty_bank, deck=self.cards, players=players)
        self.assertTrue(game_state_1.is_bank_empty())
        self.assertTrue(game_state_1.is_game_over())

        # players can't buy a card but bank is not empty
        players = deque([self.player_1])
        game_state_1 = GameState(bank=self.bank, deck=self.cards, players=players)
        self.assertFalse(game_state_1.is_bank_empty())
        self.assertFalse(game_state_1.is_game_over())

        # players can't buy a card and bank is empty
        game_state_1 = GameState(bank=self.empty_bank, deck=self.cards, players=players)
        self.assertTrue(game_state_1.is_bank_empty())
        self.assertTrue(game_state_1.is_game_over())

    def testCanAnyPlayerBuyAnyCard(self):
        players = deque([self.player_1])
        game_state_1 = GameState(bank=self.empty_bank, deck=self.cards, players=players)
        self.assertFalse(game_state_1.can_any_player_buy_any_card())

        players = deque([self.player_1, self.won_player])
        game_state_1 = GameState(bank=self.empty_bank, deck=self.cards, players=players)
        self.assertFalse(game_state_1.can_any_player_buy_any_card())

        players = deque([self.player_1, self.won_player, self.player_2])
        game_state_1 = GameState(bank=self.empty_bank, deck=self.cards, players=players)
        self.assertTrue(game_state_1.can_any_player_buy_any_card())

    def testNextTurn(self):
        turn_state_1 = TurnState(
            bank=self.bank, active_player=self.player_2, player_scores=self.scores
        )
        self.assertEqual(self.game_state_1.extract_turnstate(), turn_state_1)

    def testKickPlayer(self):
        players = deque([self.player_1, self.won_player, self.player_2])
        game_state_1 = GameState(bank=self.empty_bank, deck=self.cards, players=players)
        game_state_1.kick_player(1)
        self.assertCountEqual(game_state_1.players, [self.won_player, self.player_2])
