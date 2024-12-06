import unittest
from collections import Counter


from Bazaar.Common.equations import Equation, Equations
from Bazaar.Player.exchanges import *
from Bazaar.Common.pebble import Pebble, PebbleColor, PebbleCollection


class TestExchange(unittest.TestCase):

    def setUp(self):
        # Set up some initial data to use in tests
        self.red = Pebble(color=PebbleColor.RED)
        self.green = Pebble(color=PebbleColor.GREEN)
        self.blue = Pebble(color=PebbleColor.BLUE)
        self.yellow = Pebble(color=PebbleColor.YELLOW)
        self.white = Pebble(color=PebbleColor.WHITE)


        self.collectionR = PebbleCollection(
            pebbles=tuple([self.red])
        )
        self.collectionB = PebbleCollection(pebbles=tuple([self.blue]))
        self.collectionG = PebbleCollection(pebbles=tuple([self.green]))
        self.collectionY = PebbleCollection(pebbles=tuple([self.yellow]))
        self.collectionRG = self.collectionR +self.collectionG

        self.collectionRWB = PebbleCollection(
            pebbles=(self.red, self.white, self.blue)
        )
        self.collectionRGBY = PebbleCollection(
            pebbles=(self.red, self.green, self.blue, self.yellow)
        )
        self.collectionRGWBY = PebbleCollection(
            pebbles=(self.red, self.green, self.white, self.blue, self.yellow)
        )
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

        self.equationR_B = Equation(
            lhs=self.collectionR,
            rhs=self.collectionB,
            directed=True,
        )
        self.equationG_Y = Equation(
            lhs=self.collectionG,
            rhs=self.collectionY,
            directed=True,
        )

    def test_perform_exchange(self):
        """
        Test that performing an exchange updates the wallet and bank correctly
        and appends the equation to the action_sequence.
        """
        exchange = Exchange(
            wallet=self.collectionR +self.collectionG, bank=self.collectionB +self.collectionY, pebble_exchanges=[]
        )
        new_exchange = exchange.perform_exchange(self.equationR_B)

        expected_wallet = PebbleCollection(pebbles=(self.green, self.blue))
        expected_bank = PebbleCollection(pebbles=(self.red, self.yellow))
        expected_action_sequence = [self.equationR_B]

        self.assertEqual(
            Counter(new_exchange.wallet.pebbles), Counter(expected_wallet.pebbles)
        )
        self.assertEqual(
            Counter(new_exchange.bank.pebbles), Counter(expected_bank.pebbles)
        )
        self.assertEqual(new_exchange.pebble_exchanges, expected_action_sequence)

    def test_possible_next_exchange(self):
        """
        Test that the possible_next_exchange method returns the correct list of next exchanges
        based on the available equations.
        """
        equations = Equations(equations={self.equationR_B, self.equationG_Y})
        exchange = Exchange(
            wallet=self.collectionRG, bank=self.collectionBY, pebble_exchanges=[]
        )

        next_exchanges = exchange.possible_next_exchange(equations)

        # Perform the expected exchanges
        expected_wallet_1, expected_bank_1 = self.equationR_B.trade_equation(
            self.collectionRG, self.collectionBY
        )
        expected_wallet_2, expected_bank_2 = self.equationG_Y.trade_equation(
            self.collectionRG, self.collectionBY
        )

        expected_exchange_1 = Exchange(
            wallet=expected_wallet_1,
            bank=expected_bank_1,
            action_sequence=[self.equationR_B],
        )
        expected_exchange_2 = Exchange(
            wallet=expected_wallet_2,
            bank=expected_bank_2,
            action_sequence=[self.equationG_Y],
        )

        self.assertEqual(len(next_exchanges), 2)

        # Test that both possible exchanges are included in the result
        self.assertIn(expected_exchange_1, next_exchanges)
        self.assertIn(expected_exchange_2, next_exchanges)

    def test_no_possible_exchanges(self):
        """
        Test that if no exchanges are possible, the possible_next_exchange method returns an empty list.

        """
        exchange = Exchange(
            wallet=self.collectionRG, bank=self.collectionBY, action_sequence=[]
        )
        empty_equations = Equations(equations=set())
        next_exchanges = exchange.possible_next_exchange(empty_equations)

        self.assertEqual(next_exchanges, [])


class TestExchanges(unittest.TestCase):
    def setUp(self):
        # Set up some initial data to use in tests
        self.red = Pebble(color=PebbleColor.RED)
        self.green = Pebble(color=PebbleColor.GREEN)
        self.blue = Pebble(color=PebbleColor.BLUE)
        self.yellow = Pebble(color=PebbleColor.YELLOW)
        self.white = Pebble(color=PebbleColor.WHITE)

        self.collectionR = PebbleCollection(
            pebbles=tuple([self.red])
        )
        self.collectionB = PebbleCollection(pebbles=tuple([self.blue]))
        self.collectionG = PebbleCollection(pebbles=tuple([self.green]))
        self.collectionY = PebbleCollection(pebbles=tuple([self.yellow]))
        self.collectionRG = self.collectionR + self.collectionG
        self.collectionBY = self.collectionB + self.collectionY
        self.collectionRW = PebbleCollection(
            pebbles=(self.red, self.white)
        )

        self.collectionRWB = PebbleCollection(
            pebbles=(self.red, self.white, self.blue)
        )
        self.collectionRGBY = PebbleCollection(
            pebbles=(self.red, self.green, self.blue, self.yellow)
        )
        self.collectionRGWBY = PebbleCollection(
            pebbles=(self.red, self.green, self.white, self.blue, self.yellow)
        )
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

        self.equationR_B = Equation(
            lhs=self.collectionR,
            rhs=self.collectionB,
            directed=True,
        )
        self.equationG_Y = Equation(
            lhs=self.collectionG,
            rhs=self.collectionY,
            directed=True,
        )
        self.equations = Equations(equations = tuple([self.equationR_B]))

        self.exchangeRG_BY = Exchange(
            wallet=self.collectionRG, bank=self.collectionBY, pebble_exchanges=[]
        )
        self.exchangeBY_RW = Exchange(
            wallet=self.collectionBY, bank=self.collectionRW, pebble_exchanges=[]
        )


        self.exchanges = Exchanges(exchanges=[])

    def test_put_adds_exchange(self):
        """Test that the put method adds an exchange to the exchanges list."""
        self.exchanges.put(self.exchangeRG_BY)
        self.assertEqual(len(self.exchanges.exchanges), 1)
        self.assertEqual(self.exchanges.exchanges[0], self.exchangeRG_BY)

        self.exchanges.put(self.exchangeBY_RW)
        self.assertEqual(len(self.exchanges.exchanges), 2)
        self.assertEqual(self.exchanges.exchanges[1], self.exchangeBY_RW)

    def test_get_retrieves_and_removes_exchange(self):
        """Test that the get method retrieves the first exchange and removes it from the list."""
        self.exchanges.put(self.exchangeRG_BY)
        self.exchanges.put(self.exchangeBY_RW)

        first_exchange = self.exchanges.get()
        self.assertEqual(first_exchange, self.exchangeRG_BY)
        self.assertEqual(len(self.exchanges.exchanges), 1)
        self.assertEqual(self.exchanges.exchanges[0], self.exchangeBY_RW)
        second_exchange = self.exchanges.get()
        self.assertEqual(second_exchange, self.exchangeBY_RW)
        self.assertEqual(len(self.exchanges.exchanges), 0)

    def test_have_wallet_n_exchanges(self):
        """Test that have_wallet_n_exchanges method works as expected."""
        self.exchanges.put(self.exchangeRG_BY)
        self.assertTrue(
            self.exchanges.have_wallet_n_exchanges(
                self.collectionRG, self.exchangeRG_BY.pebble_exchanges
            )
        )
        self.assertFalse(
            self.exchanges.have_wallet_n_exchanges(
                self.collectionBY, self.exchangeRG_BY.pebble_exchanges
            )
        )
    def test_all_possible_exchanges(self):
        """"""
        explored = all_possible_exchanges(self.equations,self.collectionRGWBY,self.collectionRGWBY)
        print(explored)
        self.assertEqual(len(explored.exchanges), 3)
        equation1 = self.equationR_B
        explored = all_possible_exchanges(self.equations, self.collectionB, self.collectionRGWBY)
        print(explored)
        self.assertEqual(len(explored.exchanges), 2)


if __name__ == "__main__":
    unittest.main()
