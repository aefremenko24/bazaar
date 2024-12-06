import unittest
from collections import deque

from Bazaar.Common.turn_state import TurnState
from Bazaar.Player.strategy import Strategy
from Bazaar.Referee.player_state import PlayerState
from Bazaar.Referee.referee import (
    Referee,
    OverState,
    InitState,
    ExchangeState,
    PurchaseState,
)
from Bazaar.Referee.game_state import GameState
from Bazaar.Common.equations import Equations, Equation
from Bazaar.Player.mechanism import Mechanism
from Bazaar.Common.cards import Cards, Card
from Bazaar.Common.pebble import init_bank, Pebble, PebbleColor, PebbleCollection


class DummyPlayer(Mechanism):
    """dummy player for testing purpose"""

    def request_pebble_or_trades(self, turn_state: TurnState):
        """always request a pebble"""
        return []

    def request_cards(self, turn_state: TurnState):
        """never purchase card"""
        # return PurchaseSequence(
        #     sequence=Cards(),
        #     points=0,
        #     wallet=turn_state.active_player.wallet,
        #     bank=turn_state.bank,
        # )


class ExceptionPlayer(Mechanism):
    """
    testing player that misbehave by raising exception on every call
    """

    id: int

    def request_pebble_or_trades(self, turn_state: TurnState):
        raise Exception

    def request_cards(self, turn_state: TurnState):
        """request a card that may not be visible"""
        raise Exception


class CheatPlayer(Mechanism):
    """
    testing player that misbehave by raising exception on every call
    """

    id: int

    def request_pebble_or_trades(self, turn_state: TurnState):
        """request a equation that may not exist or can't purchase"""
        return Equations(
            equations={
                Equation(
                    lhs=PebbleCollection(list_of_pebbles=[self.red, self.green]),
                    rhs=PebbleCollection(list_of_pebbles=[self.blue, self.yellow]),
                ),
                Equation(
                    lhs=PebbleCollection(list_of_pebbles=[self.green, self.green]),
                    rhs=PebbleCollection(list_of_pebbles=[self.white, self.yellow]),
                ),
                Equation(
                    lhs=PebbleCollection(list_of_pebbles=[self.red, self.blue]),
                    rhs=PebbleCollection(list_of_pebbles=[self.yellow, self.yellow]),
                ),
            }
        )

    def request_cards(self, turn_state: TurnState):
        """request a card that may not be visible"""
        blue = Pebble(color=PebbleColor.BLUE)
        collectionBBBBB = PebbleCollection(pebbles=(blue, blue, blue, blue, blue))
        # return PurchaseSequence(
        #     sequence=Cards(cards=Card(pebbles=collectionBBBBB, happy_face=True)),
        #     points=0,
        #     wallet=turn_state.active_player.wallet,
        #     bank=turn_state.bank,
        # )


class MaxpointPlayer(Mechanism):
    """
    testing player that misbehave by raising exception on every call
    """

    name: str
    policy: str

    def request_pebble_or_trades(self, turn_state: TurnState):
        strategy = Strategy(policy="purchase-points")
        return strategy.get_trade_purchase()[0]

    def request_cards(self, turn_state: TurnState):
        """request a card that may not be visible"""
        strategy = Strategy(policy="purchase-points")
        if not strategy.get_trade_purchase()[0]:
            return strategy.get_purchase()[0]
        return strategy.get_trade_purchase()[1]


class TestReferee(unittest.TestCase):
    def setUp(self):
        self.red = Pebble(color=PebbleColor.RED)
        self.green = Pebble(color=PebbleColor.GREEN)
        self.blue = Pebble(color=PebbleColor.BLUE)
        self.yellow = Pebble(color=PebbleColor.YELLOW)
        self.white = Pebble(color=PebbleColor.WHITE)

        self.collectionB = PebbleCollection(pebbles=(self.blue,))
        self.collectionR = PebbleCollection(pebbles=(self.red,))
        self.collectionRG = PebbleCollection(pebbles=(self.red, self.green))
        self.collectionBY = PebbleCollection(pebbles=(self.blue, self.yellow))
        self.collectionRWB = PebbleCollection(pebbles=(self.red, self.white, self.blue))
        self.collectionRGBY = PebbleCollection(
            pebbles=(self.red, self.green, self.blue, self.yellow)
        )
        self.collectionRGWBY = PebbleCollection(
            pebbles=(self.red, self.green, self.white, self.blue, self.yellow)
        )
        self.collection2RGWBY = PebbleCollection(pebbles=(self.blue, self.yellow, self.green, self.white, self.blue,
                                                          self.yellow))
        self.collectionRGGBY = PebbleCollection(
            pebbles=(self.red, self.green, self.green, self.blue, self.yellow)
        )
        self.collectionRGGBB = PebbleCollection(
            pebbles=(self.red, self.green, self.green, self.blue, self.blue)
        )

        self.happy_cardRGWBY = Card(pebbles=self.collectionRGWBY, happy_face=True)
        self.happy_cardRGGBY = Card(pebbles=self.collectionRGGBY, happy_face=True)
        self.sad_cardRGWBY = Card(pebbles=self.collectionRGWBY, happy_face=False)
        self.sad_cardRGGBY = Card(pebbles=self.collectionRGGBY, happy_face=False)

        self.cards_RGWBY = Cards(cards=[self.happy_cardRGWBY, self.sad_cardRGWBY, self.happy_cardRGGBY])
        self.cards_RGGBY = Cards(cards=[self.happy_cardRGGBY, self.sad_cardRGGBY])

        # Define a bank for testing
        self.bank = PebbleCollection(
            pebbles=(self.red, self.green, self.blue, self.yellow, self.white)
        )

    def test_execute_game_one_max_point_winner_one_purchase(self):
        bank = self.collectionRGWBY
        equations = Equations(
            equations={
                Equation(
                    lhs=PebbleCollection(pebbles=(self.red, self.green)),
                    rhs=PebbleCollection(pebbles=(self.blue, self.yellow)),
                ),
                Equation(
                    lhs=PebbleCollection(pebbles=(self.green, self.green)),
                    rhs=PebbleCollection(pebbles=(self.white, self.yellow)),
                ),
                Equation(
                    lhs=PebbleCollection(pebbles=[self.red, self.blue]),
                    rhs=PebbleCollection(pebbles=(self.yellow, self.yellow)),
                ),
            }
        )
        aiPlayer = Mechanism(name= "j", policy= "purchase-points")
        ai2 = Mechanism(name= "k", policy= "purchase-points")
        player_state = PlayerState(actor=aiPlayer,wallet=self.collection2RGWBY)
        player_stat2 = PlayerState(actor= ai2,wallet= self.collectionRGWBY)
        players = deque([player_state,player_stat2])
        players_m = deque([aiPlayer,ai2])
        referee = Referee(equations=equations)
        #
        all_cards = self.cards_RGWBY

        game_state = GameState(
            bank=bank,
            visibles=all_cards,
            invisible_deck=self.cards_RGGBY,
            players=players,
        )
        winner, cheater = referee.execute_game(players_m, game_state)

        # final_state = referee.state
        # self.assertIsInstance(final_state, OverState)
        self.assertEqual(len(winner), 1)
        self.assertEqual(winner, winner)
        self.assertEqual(len(cheater), 0)

    def test_execute_game_one_winner_empty_bank(self):
        bank = self.collectionRGWBY
        equations = Equations.generate_random(10)
        playerDum = DummyPlayer(id=0)
        players = [playerDum]
        referee = Referee(equations=equations)
        #
        all_cards = Cards.generate_random()
        visible_cards = Cards(cards=all_cards.cards[-4:])
        invisible_cards = Cards(cards=all_cards.cards[:-4])
        game_state = GameState(
            bank=bank,
            visibles=visible_cards,
            invisible_deck=invisible_cards,
            players=players,
        )
        winner, cheater = referee.execute_game(players, game_state)
        final_state = referee.state
        self.assertIsInstance(final_state, OverState)
        self.assertEqual(len(winner), 1)
        self.assertIn(playerDum, winner)
        self.assertEqual(len(cheater), 0)

    def test_execute_game_no_winner_empty_bank(self):
        """ "test player have been kicked because they raise execption"""
        bank = self.collectionRGWBY
        equations = Equations.generate_random(10)
        playerE = ExceptionPlayer(id=0)
        players = [playerE]
        referee = Referee(equations=equations)
        #
        all_cards = Cards.generate_random()
        visible_cards = Cards(cards=all_cards.cards[-4:])
        invisible_cards = Cards(cards=all_cards.cards[:-4])
        game_state = GameState(
            bank=bank,
            visibles=visible_cards,
            invisible_deck=invisible_cards,
            players=players,
        )
        winner, cheater = referee.execute_game(players, game_state)
        final_state = referee.state
        self.assertIsInstance(final_state, OverState)
        self.assertEqual(len(winner), 0)

        self.assertEqual(len(cheater), 1)
        self.assertIn(playerE, cheater)

    def test_execute_game_no_winner_one_cheater(self):
        """ "test all  player have been kicked because they cheat (small bank to ensure  exchange for equation is illegal)"""
        bank = self.collectionR
        equations = Equations.generate_random(10)
        playerE = CheatPlayer(id=0)
        players = [playerE]
        referee = Referee(equations=equations)
        all_cards = Cards.generate_random()
        visible_cards = Cards(cards=all_cards.cards[-4:])
        invisible_cards = Cards(cards=all_cards.cards[:-4])
        game_state = GameState(
            bank=bank,
            visibles=visible_cards,
            invisible_deck=invisible_cards,
            players=players,
        )
        winner, cheater = referee.execute_game(players, game_state)
        final_state = referee.state
        self.assertIsInstance(final_state, OverState)
        self.assertEqual(len(winner), 0)

        self.assertEqual(len(cheater), 1)
        self.assertIn(playerE, cheater)

    def test_execute_game_max_point_winner_three_players(self):
        """
        a game that have three player and available for one purchase, ai winner wins regardlyss of order
        """
        bank = self.collectionRGWBY + self.collectionRGWBY
        equations = Equations(
            equations={
                Equation(
                    lhs=PebbleCollection(pebbles=[self.red, self.green]),
                    rhs=PebbleCollection(pebbles=[self.blue, self.yellow]),
                ),
                Equation(
                    lhs=PebbleCollection(pebbles=[self.green, self.green]),
                    rhs=PebbleCollection(pebbles=[self.white, self.yellow]),
                ),
                Equation(
                    lhs=PebbleCollection(pebbles=[self.red, self.blue]),
                    rhs=PebbleCollection(pebbles=[self.yellow, self.yellow]),
                ),
            }
        )
        aiPlayer = Mechanism(name="j",policy="purchase-points")
        playerDum = DummyPlayer(name= "k",policy="purchase-points")
        player_state = PlayerState(actor=aiPlayer, wallet=self.collection2RGWBY)
        pds = PlayerState(actor=playerDum,wallet= self.collectionRGWBY)
        players = deque([player_state,pds])
        players_m = deque([aiPlayer,playerDum])
        referee = Referee(equations=equations)
        all_cards = self.cards_RGWBY

        game_state = GameState(
            bank=bank,
            visibles=all_cards,
            invisible_deck=Cards(),
            players=players,
        )
        winner, cheater = referee.execute_game(players_m, game_state)
        self.assertEqual(len(winner), 1)
        self.assertIn(aiPlayer, winner)
        self.assertEqual(len(cheater), 1)

    def test_initial_to_exchange_state(self):
        """Tests transition from InitState to ExchangeState."""
        players = [DummyPlayer(id=0)]
        referee = Referee()

        game_state = GameState(
            bank=self.bank,
            visibles=self.cards_RGWBY,
            invisible_deck=Cards(),
            players=players,
        )
        state = referee.init_game_state(players, game_state)

        self.assertIsInstance(state, InitState)
        state = state.handle()
        self.assertIsInstance(state, ExchangeState)

    def test_exchange_to_purchase_state(self):
        """Tests transition from ExchangeState to PurchaseState."""
        players = [DummyPlayer(name="")]
        referee = Referee()

    #
        game_state = GameState(
            bank=self.bank,
            visibles=self.cards_RGWBY,
            invisible_deck=Cards(),
            players=players,
        )
        state = referee.init_game_state(players, game_state)

        # ExchangeState
        state = state.handle()
        self.assertIsInstance(state, ExchangeState)

        #  PurchaseState
        state = state.handle()
        self.assertIsInstance(state, PurchaseState)

    def test_exchange_to_over_state(self):
        """Tests transition from PurchaseState to either ExchangeState or OverState based on game conditions."""
        players = [ExceptionPlayer(id=0)]
        referee = Referee()

        game_state = GameState(
            bank=self.bank,
            visibles=self.cards_RGWBY,
            invisible_deck=Cards(),
            players=players,
        )
        state = referee.init_game_state(players, game_state)

        state = state.handle()  # Init to Exchange
        state = state.handle()  # Exchange to Over

        self.assertIsInstance(state, OverState)

    def test_purchase_to_exchange_state(self):
        """Tests transition from PurchaseState to ExchangeState ."""
        players = [DummyPlayer(id=0)]
        referee = Referee()

        game_state = GameState(
            bank=self.bank,
            visibles=self.cards_RGWBY,
            invisible_deck=Cards(),
            players=players,
        )
        state = referee.init_game_state(players, game_state)

        # ExchangeState
        state = state.handle()
        self.assertIsInstance(state, ExchangeState)

        #  PurchaseState
        state = state.handle()
        # ExchangeState
        state = state.handle()
        self.assertIsInstance(state, ExchangeState)

    def test_purchase_to_over_state(self):
        """Tests transition from PurchaseState to OverState based on game conditions."""
        bank = self.collectionRGWBY
        equations = Equations(
            equations={
                Equation(
                    lhs=PebbleCollection(list_of_pebbles=[self.red, self.green]),
                    rhs=PebbleCollection(list_of_pebbles=[self.blue, self.yellow]),
                ),
                Equation(
                    lhs=PebbleCollection(list_of_pebbles=[self.green, self.green]),
                    rhs=PebbleCollection(list_of_pebbles=[self.white, self.yellow]),
                ),
                Equation(
                    lhs=PebbleCollection(list_of_pebbles=[self.red, self.blue]),
                    rhs=PebbleCollection(list_of_pebbles=[self.yellow, self.yellow]),
                ),
            }
        )
        aiPlayer = MaxpointPlayer(id=0)
        players = [aiPlayer]
        referee = Referee(equations=equations)

        game_state = GameState(
            bank=bank,
            visibles=self.cards_RGWBY,
            invisible_deck=Cards(),
            players=players,
        )
        state = referee.init_game_state(players, game_state)

        state = state.handle()  # Init to Exchange
        state = state.handle()  # Exchange to Purchase
        state = state.handle()  # Purchase to Over

        self.assertIsInstance(state, OverState)
