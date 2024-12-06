import unittest

from Bazaar.Common.cards import Card, Cards
from Bazaar.Common.equations import Equations, Equation
from Bazaar.Common.pebble import PebbleCollection, Pebble, PebbleColor
from Bazaar.Common.turn_state import TurnState
from Bazaar.Player.mechanism import Mechanism
from Bazaar.Player.purchases import PurchaseSequence
from Bazaar.Referee.test_game_state_board import cards, card1


class TestMechanism(unittest.TestCase):

    def setUp(self):
        self.player1 = Mechanism()
        self.player2 = Mechanism()
        self.equationsRandom = Equations.generate_random(10)
        self.pebblesRR = PebbleCollection(
            pebbles=tuple[Pebble(color=PebbleColor.RED), Pebble(color=PebbleColor.RED)]
        )
        self.pebblesGG = PebbleCollection(
            pebbles=tuple[
                Pebble(color=PebbleColor.GREEN), Pebble(color=PebbleColor.GREEN)
            ]
        )
        self.equationRRtoGG = Equation(lhs=self.pebblesRR, rhs=self.pebblesGG)
        self.equations1 = Equations(equations=[self.equationRRtoGG])
        self.turnstate1 = TurnState.deserialize(
            data={
                "active": {"score": 11, "wallet": ["green", "green", "green"]},
                "bank": ["red", "red"],
                "cards": [
                    {"face?": False, "pebbles": ["red", "red", "red", "blue", "green"]}
                ],
                "scores": [2, 3],
            }
        )
        self.turnstate2 = TurnState.deserialize(
            data={
                "active": {"score": 11, "wallet": ["red", "red", "red"]},
                "bank": [],
                "cards": [
                    {"face?": False, "pebbles": ["red", "red", "red", "blue", "green"]}
                ],
                "scores": [2, 3],
            }
        )
        self.card1 = Card.deserialize(
            {"face?": False, "pebbles": ["red", "red", "red", "blue", "green"]}
        )

    def test_setup(self):
        self.assertIsNone(self.player1.equations)
        self.assertIsNone(self.player2.equations)
        self.player1.setup(equations=self.equationsRandom)
        self.player2.setup(equations=self.equations1)
        self.assertEqual(self.player1.equations, self.equationsRandom)
        self.assertEqual(self.player2.equations, self.equations1)

    def test_request_pebble_or_trades(self):
        self.assertEqual(
            self.player2.request_pebble_or_trades(turn_state=self.turnstate1),
            self.equations1,
        )
        self.assertIsNone(
            self.player2.request_pebble_or_trades(turn_state=self.turnstate2)
        )

    def test_request_cards(self):
        self.assertIsNone(self.player2.request_cards(turn_state=self.turnstate1))
        self.assertIsNone(self.player2.request_cards(turn_state=self.turnstate2))
        self.turnstate2.active_player.wallet.add_pebble(Pebble(color=PebbleColor.BLUE))
        self.turnstate2.active_player.wallet.add_pebble(Pebble(color=PebbleColor.GREEN))
        self.assertEqual(
            self.player2.request_cards(turn_state=self.turnstate2),
            PurchaseSequence(cards=Cards(cards=[card1])),
        )

    def test_win(self):
        self.player1.win(True)
        self.player2.win(False)
