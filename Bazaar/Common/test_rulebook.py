import unittest
from collections import Counter

import pydantic_core
from pydantic import ValidationError

from Bazaar.Common.cards import *
from Bazaar.Common.equations import Equation
from Bazaar.Common.pebble import Pebble, PebbleCollection
from Bazaar.Common.data import *
from Bazaar.Common.rule_book import RuleBook
from Bazaar.Common.turn_state import TurnState
from Bazaar.Referee.player_state import PlayerState


# TODO: add constructor frozen tests
class TestRuleBook(unittest.TestCase):
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

        self.eqR_B = Equation(lhs=self.collectionR, rhs=self.collectionB, directed=True)
        self.eqG_R = Equation(
            lhs=PebbleCollection(pebbles=(self.green,)),
            rhs=PebbleCollection(pebbles=(self.red,)),
            directed=True,
        )
        self.eqG_Y = Equation(
            lhs=PebbleCollection(pebbles=(self.green,)),
            rhs=PebbleCollection(pebbles=(self.yellow,)),
            directed=True,
        )
        self.eqY_G = Equation(
            lhs=PebbleCollection(pebbles=(self.yellow,)),
            rhs=PebbleCollection(pebbles=(self.green,)),
            directed=True,
        )
        self.eqB_G = Equation(
            lhs=PebbleCollection(pebbles=(self.blue,)),
            rhs=PebbleCollection(pebbles=(self.green,)),
            directed=True,
        )

        self.cards_RGWBY = Cards(cards=[self.happy_cardRGWBY, self.sad_cardRGWBY])

    def test_can_trade_equation_valid(self):

        result = RuleBook.can_trade_equation(
            self.eqR_B, self.collectionRGWBY, self.collectionRGGBB
        )
        self.assertTrue(result)

    def test_can_trade(self):
        equation = Equation(
            lhs=PebbleCollection(pebbles=(self.red, self.green)),
            rhs=PebbleCollection(pebbles=(self.blue, self.yellow)),
            directed=True,
        )
        my_colors = PebbleCollection(pebbles=(self.red, self.green))
        bank_pebbles = PebbleCollection(
            pebbles=(self.blue, self.yellow, self.blue, self.yellow)
        )
        self.assertTrue(RuleBook.can_trade_equation(equation, my_colors, bank_pebbles))

        equation2 = Equation(
            lhs=PebbleCollection(pebbles=(self.red, self.yellow)),
            rhs=PebbleCollection(pebbles=(self.blue, self.white)),
            directed=True,
        )
        self.assertFalse(
            RuleBook.can_trade_equation(equation2, my_colors, bank_pebbles)
        )
    def test_can_trade(self):
        equation = Equation(
            lhs=PebbleCollection(pebbles=tuple([self.red, self.green])),
            rhs=PebbleCollection(pebbles=tuple([self.blue, self.yellow])),
            directed=True,
        )
        my_colors = PebbleCollection(pebbles=tuple([self.red, self.green]))
        bank_pebbles = PebbleCollection(
            list_of_pebbles=[self.blue, self.yellow, self.blue, self.yellow]
        )
        self.assertTrue(equation.can_trade(my_colors, bank_pebbles))

        equation2 = Equation(
            lhs=PebbleCollection(pebbles=tuple([self.red, self.yellow])),
            rhs=PebbleCollection(pebbles=tuple([self.blue, self.white])),
            directed=True,
        )
        self.assertFalse(equation2.can_trade(my_colors, bank_pebbles))

    def test_tradable_equation_left_to_right(self):
        """Test that trade can happen from LHS -> RHS if player and bank have sufficient pebbles."""
        # Player has enough pebbles for LHS, bank has enough pebbles for RHS
        player_pebbles = PebbleCollection(pebbles=(self.red, self.green))
        bank_pebbles = PebbleCollection(pebbles=(self.blue, self.yellow))
        equation = Equation(lhs=self.collectionRG, rhs=self.collectionBY, directed=True)

        # LHS -> RHS
        result = RuleBook.tradable_equation(equation, player_pebbles, bank_pebbles)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].lhs, equation.lhs)
        self.assertEqual(result[0].rhs, equation.rhs)

    def test_tradable_equation_right_to_left(self):
        """Test that trade can happen from RHS -> LHS if player and bank have sufficient pebbles."""
        # Player has enough pebbles for RHS, bank has enough pebbles for LHS
        player_pebbles = self.collectionBY
        bank_pebbles = self.collectionRG
        equation = Equation(lhs=self.collectionRG, rhs=self.collectionBY, directed=True)

        # RHS -> LHS
        result = RuleBook.tradable_equation(equation, player_pebbles, bank_pebbles)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].lhs, equation.rhs)
        self.assertEqual(result[0].rhs, equation.lhs)

    def test_tradable_equation_both_sides(self):
        """Test that trade can happen from RHS -> LHS if player and bank have sufficient pebbles."""
        # Player has enough pebbles for RHS, bank has enough pebbles for LHS
        collectionBYRG = self.collectionRG + self.collectionBY
        player_pebbles = collectionBYRG
        bank_pebbles = collectionBYRG
        equation = Equation(lhs=self.collectionRG, rhs=self.collectionBY, directed=True)

        result = RuleBook.tradable_equation(equation, player_pebbles, bank_pebbles)
        self.assertEqual(len(result), 2)
        lhs_rhs_pair = [(eq.lhs, eq.rhs) for eq in result]
        self.assertIn((equation.rhs, equation.lhs), lhs_rhs_pair)  # RHS -> LHS trade
        self.assertIn((equation.lhs, equation.rhs), lhs_rhs_pair)  # LHS -> RHS trade

    def test_tradable_equation_insufficient_player_pebbles(self):
        """Test that trade can happen from RHS -> LHS if player and bank have sufficient pebbles."""
        # Player has enough pebbles for RHS, bank has enough pebbles for LHS
        collectionBYRG = self.collectionRG + self.collectionBY
        player_pebbles = PebbleCollection(pebbles=(self.blue, self.green))
        bank_pebbles = collectionBYRG
        equation = Equation(
            lhs=PebbleCollection(pebbles=(self.red, self.green)),
            rhs=PebbleCollection(pebbles=(self.blue, self.yellow)),
            directed=True,
        )

        # Check that the trade is possible RHS -> LHS
        result = RuleBook.tradable_equation(equation, player_pebbles, bank_pebbles)
        self.assertEqual(len(result), 0)

    def test_tradable_equation_insufficient_bank_pebbles(self):
        collectionBYRG = self.collectionRG + self.collectionBY
        bank_pebbles = PebbleCollection(pebbles=(self.blue, self.green))
        player_pebbles = collectionBYRG
        equation = Equation(
            lhs=PebbleCollection(pebbles=(self.red, self.green)),
            rhs=PebbleCollection(pebbles=(self.blue, self.yellow)),
            directed=True,
        )

        # Check that the trade is possible RHS -> LHS
        result = RuleBook.tradable_equation(equation, player_pebbles, bank_pebbles)
        self.assertEqual(len(result), 0)

    def test_tradable_equation_insufficient_bank_and_player_pebbles(self):
        """Test that trade can happen from RHS -> LHS if player and bank have sufficient pebbles."""
        # Player has enough pebbles for RHS, bank has enough pebbles for LHS
        bank_pebbles = self.collectionB
        player_pebbles = self.collectionR
        equation = Equation(
            lhs=PebbleCollection(pebbles=(self.red, self.green)),
            rhs=PebbleCollection(pebbles=(self.blue, self.yellow)),
            directed=True,
        )

        # Check that the trade is possible RHS -> LHS
        result = RuleBook.tradable_equation(equation, player_pebbles, bank_pebbles)
        self.assertEqual(len(result), 0)

    def test_validate_exchange_request_valid(self):
        """Test that a valid exchange request passes validation."""
        playerR = PlayerState(id=1, wallet=self.collectionR, score=0)
        turn_state = TurnState(
            bank=self.collectionRGWBY,
            active_player=playerR,
            player_scores=[],
            cards=self.cards_RGWBY,
        )
        equations_list = [self.eqR_B]
        result = RuleBook.validate_exchange_request(turn_state, equations_list)
        self.assertTrue(result)

    def test_validate_exchange_request_valid_2eq(self):
        """Test that a valid exchange request 2 eq."""
        playerR = PlayerState(id=1, wallet=self.collectionR, score=0)
        turn_state = TurnState(
            bank=self.collectionRGWBY,
            active_player=playerR,
            player_scores=[],
            cards=self.cards_RGWBY,
        )
        equations_list = [self.eqR_B, self.eqB_G]
        result = RuleBook.validate_exchange_request(turn_state, equations_list)
        self.assertTrue(result)

    def test_validate_exchange_request_valid_3eq(self):
        """Test that a valid exchange request 3eq."""
        playerR = PlayerState(id=1, wallet=self.collectionR, score=0)
        turn_state = TurnState(
            bank=self.collectionRGWBY,
            active_player=playerR,
            player_scores=[],
            cards=self.cards_RGWBY,
        )
        equations_list = [self.eqR_B, self.eqB_G, self.eqG_R]
        result = RuleBook.validate_exchange_request(turn_state, equations_list)
        self.assertTrue(result)

    def test_validate_exchange_request_valid_4eq(self):
        """Test that a valid exchange request 4eq."""
        playerR = PlayerState(id=1, wallet=self.collectionR, score=0)
        turn_state = TurnState(
            bank=self.collectionRGWBY,
            active_player=playerR,
            player_scores=[],
            cards=self.cards_RGWBY,
        )
        equations_list = [self.eqR_B, self.eqB_G, self.eqG_R, self.eqR_B]
        result = RuleBook.validate_exchange_request(turn_state, equations_list)
        self.assertTrue(result)

    def test_validate_exchange_request_invalid_5eq(self):
        """Test that an invalid exchange request that request 5 eqs"""
        playerR = PlayerState(id=1, wallet=self.collectionRGWBY, score=0)
        turn_state = TurnState(
            bank=self.collectionRGWBY,
            active_player=playerR,
            player_scores=[],
            cards=self.cards_RGWBY,
        )
        equations_list = [self.eqR_B, self.eqB_G, self.eqG_R, self.eqR_B, self.eqY_G]
        result = RuleBook.validate_exchange_request(turn_state, equations_list)
        self.assertFalse(result)

    def test_validate_exchange_request_invalid_1eq_insufficient_wallet(self):
        """Test that an invalid exchange request that overdraw wallet during exchange"""
        playerR = PlayerState(id=1, wallet=self.collectionR, score=0)
        turn_state = TurnState(
            bank=self.collectionRGWBY,
            active_player=playerR,
            player_scores=[],
            cards=self.cards_RGWBY,
        )
        equations_list = [self.eqB_G]
        result = RuleBook.validate_exchange_request(turn_state, equations_list)
        self.assertFalse(result)

    def test_validate_exchange_request_invalid_4eq_insufficient_wallet(self):
        """Test that an invalid exchange request that overdraw wallet during exchange"""
        playerR = PlayerState(id=1, wallet=self.collectionR, score=0)
        turn_state = TurnState(
            bank=self.collectionRGWBY,
            active_player=playerR,
            player_scores=[],
            cards=self.cards_RGWBY,
        )
        equations_list = [self.eqR_B, self.eqB_G, self.eqG_Y, self.eqR_B]
        result = RuleBook.validate_exchange_request(turn_state, equations_list)
        self.assertFalse(result)

    def test_validate_exchange_request_invalid_4eq_insufficient_bank(self):
        """Test that an invalid exchange request where bank is out of pebbles during exchanges"""
        playerR = PlayerState(id=1, wallet=self.collectionRGWBY, score=0)
        turn_state = TurnState(
            bank=self.collectionRGWBY,
            active_player=playerR,
            player_scores=[],
            cards=self.cards_RGWBY,
        )
        equations_list = [self.eqR_B, self.eqB_G, self.eqR_B, self.eqR_B]
        result = RuleBook.validate_exchange_request(turn_state, equations_list)
        self.assertFalse(result)

    def test_validate_exchange_request_empty(self):
        """Test that an empty exchange request is always valid."""
        equations_list = []
        playerRGB = PlayerState(id=1, wallet=self.collectionRGWBY, score=0)
        turn_state = TurnState(
            bank=self.collectionRGWBY,
            active_player=playerRGB,
            player_scores=[],
            cards=self.cards_RGWBY,
        )
        result = RuleBook.validate_exchange_request(turn_state, equations_list)
        self.assertTrue(result)

    def test_can_purchase_card_true(self):
        result = RuleBook.can_purchase_card(self.happy_cardRGWBY, self.collectionRGWBY)
        self.assertTrue(result)

    def test_can_purchase_card_false(self):
        result = RuleBook.can_purchase_card(self.happy_cardRGWBY, self.collectionRGGBB)
        self.assertFalse(result)

    def test_valid_purchase_request_success(self):
        """Test a valid purchase request."""
        playerRGB = PlayerState(id=1, wallet=self.collectionRGWBY, score=0)
        turn_state = TurnState(
            bank=self.collectionRGWBY,
            active_player=playerRGB,
            player_scores=[],
            cards=self.cards_RGWBY,
        )
        self.cards = Cards(cards=[self.happy_cardRGWBY])
        result = RuleBook.valid_purchase_request(turn_state, self.cards)
        self.assertTrue(result)

    def test_valid_purchase_request_failure_insuffient_wallet(self):
        """Test an invalid purchase request where player try to purchase a card with insufficint wallet"""
        self.cards = Cards(cards=[self.happy_cardRGGBY])
        playerRGB = PlayerState(id=1, wallet=self.collectionRGWBY, score=0)
        turn_state = TurnState(
            bank=self.collectionRGWBY,
            active_player=playerRGB,
            player_scores=[],
            cards=self.cards_RGWBY,
        )
        result = RuleBook.valid_purchase_request(turn_state, self.cards)
        self.assertFalse(result)

    def test_valid_purchase_request_failure_not_visible(self):
        """Test an invalid purchase request where player try to purchase a card that is not visible"""
        self.cards = Cards(cards=[self.happy_cardRGGBY])
        playerRGB = PlayerState(id=1, wallet=self.collectionRGWBY, score=0)
        turn_state = TurnState(
            bank=self.collectionRGWBY,
            active_player=playerRGB,
            player_scores=[],
            cards=self.cards_RGWBY,
        )
        result = RuleBook.valid_purchase_request(turn_state, self.cards)
        self.assertFalse(result)

    def test_valid_purchase_request_multiple_success(self):
        collectionsRRGGWWBBYY = self.collectionRGWBY + self.collectionRGWBY
        playerRGB = PlayerState(id=1, wallet=collectionsRRGGWWBBYY, score=0)
        turn_state = TurnState(
            bank=self.collectionRGWBY,
            active_player=playerRGB,
            player_scores=[],
            cards=self.cards_RGWBY,
        )
        self.cards = Cards(cards=[self.happy_cardRGWBY, self.sad_cardRGWBY])
        result = RuleBook.valid_purchase_request(turn_state, self.cards)
        self.assertTrue(result)

    def test_valid_purchase_request_multiple_failure_not_visible(self):
        """Test an invalid purchase request with multiple cards with one of them is not visible"""
        collectionsRRGGWWBBYY = self.collectionRGWBY + self.collectionRGWBY
        playerRGB = PlayerState(id=1, wallet=collectionsRRGGWWBBYY, score=0)
        turn_state = TurnState(
            bank=self.collectionRGWBY,
            active_player=playerRGB,
            player_scores=[],
            cards=self.cards_RGWBY,
        )
        self.cards = Cards(cards=[self.happy_cardRGWBY, self.happy_cardRGGBY])
        result = RuleBook.valid_purchase_request(turn_state, self.cards)
        self.assertFalse(result)

    def test_valid_purchase_request_multiple_failure_insufficient_wallet(self):
        """Test an invalid purchase request with multiple cards with one of them is not visible"""
        collectionsRRGGWWBBYY = self.collectionRGWBY + self.collectionRGGBB
        playerRGB = PlayerState(id=1, wallet=collectionsRRGGWWBBYY, score=0)
        turn_state = TurnState(
            bank=self.collectionRGWBY,
            active_player=playerRGB,
            player_scores=[],
            cards=self.cards_RGWBY,
        )
        self.cards = Cards(cards=[self.happy_cardRGWBY, self.sad_cardRGWBY])
        result = RuleBook.valid_purchase_request(turn_state, self.cards)
        self.assertFalse(result)

    def test_validate_purchase_request_empty(self):
        """Test that an empty purcahse request is always valid."""
        collectionsRRGGWWBBYY = self.collectionRGWBY + self.collectionRGGBB
        playerRGB = PlayerState(id=1, wallet=collectionsRRGGWWBBYY, score=0)
        turn_state = TurnState(
            bank=self.collectionRGWBY,
            active_player=playerRGB,
            player_scores=[],
            cards=self.cards_RGWBY,
        )
        cards = Cards(cards=[])
        result = RuleBook.valid_purchase_request(turn_state, cards)
        self.assertTrue(result)

    def test_score_if_bought_happy_0_left(self):
        """Test score_if_bought method calculates correct score. 0 pebbles left"""
        player_pebbles = self.collectionRGWBY
        score = self.happy_cardRGWBY.score_if_bought(player_pebbles)
        self.assertEqual(score, 8)

        player_pebbles = self.collectionRGGBY
        score = self.happy_cardRGGBY.score_if_bought(player_pebbles)
        self.assertEqual(score, 8)

    def test_score_if_bought_happy_1_left(self):
        """Test score_if_bought method calculates correct score. 1 pebble left"""
        player_pebbles = self.collectionRGWBY + PebbleCollection(
            list_of_pebbles=[self.red]
        )
        score = self.happy_cardRGWBY.score_if_bought(player_pebbles)
        self.assertEqual(score, 5)

        player_pebbles = self.collectionRGGBY + PebbleCollection(
            list_of_pebbles=[self.blue]
        )
        score = self.happy_cardRGGBY.score_if_bought(player_pebbles)
        self.assertEqual(score, 5)

    def test_score_if_bought_happy_2_left(self):
        """Test score_if_bought method calculates correct score. 2 pebble left"""
        player_pebbles = self.collectionRWB + self.collectionRGBY
        score = self.happy_cardRGWBY.score_if_bought(player_pebbles)

        self.assertEqual(score, 3)

        player_pebbles = self.collectionRGBY + PebbleCollection(
            list_of_pebbles=[self.green, self.blue, self.red]
        )
        score = self.happy_cardRGGBY.score_if_bought(player_pebbles)

        self.assertEqual(score, 3)

    def test_score_if_bought_happy_3_left(self):
        """Test score_if_bought method calculates correct score."""
        player_pebbles = self.collectionRGWBY + self.collectionRWB
        score = self.happy_cardRGWBY.score_if_bought(player_pebbles)

        self.assertEqual(score, 2)
        player_pebbles = self.collectionRGGBY + self.collectionRWB
        score = self.happy_cardRGWBY.score_if_bought(player_pebbles)

        self.assertEqual(score, 2)

    def test_score_if_bought_sad_0_left(self):
        """Test score_if_bought method calculates correct score."""
        player_pebbles = self.collectionRGWBY
        score = self.sad_cardRGWBY.score_if_bought(player_pebbles)

        self.assertEqual(score, 5)

        player_pebbles = self.collectionRGGBY
        score = self.sad_cardRGGBY.score_if_bought(player_pebbles)

        self.assertEqual(score, 5)

    def test_score_if_bought_sad_1_left(self):
        """Test score_if_bought method calculates correct score."""
        player_pebbles = self.collectionRGWBY + PebbleCollection(
            list_of_pebbles=[self.red]
        )
        score = self.sad_cardRGWBY.score_if_bought(player_pebbles)

        self.assertEqual(score, 3)

        player_pebbles = self.collectionRGGBY + PebbleCollection(
            list_of_pebbles=[self.blue]
        )
        score = self.sad_cardRGGBY.score_if_bought(player_pebbles)

        self.assertEqual(score, 3)

    def test_score_if_bought_sad_2_left(self):
        """Test score_if_bought method calculates correct score."""
        player_pebbles = self.collectionRWB + self.collectionRGBY
        score = self.sad_cardRGWBY.score_if_bought(player_pebbles)

        self.assertEqual(score, 2)

        player_pebbles = self.collectionRGBY + PebbleCollection(
            list_of_pebbles=[self.green, self.blue, self.red]
        )
        score = self.sad_cardRGGBY.score_if_bought(player_pebbles)
        self.assertEqual(score, 2)

    def test_score_if_bought_sad_3_left(self):
        """Test score_if_bought method calculates correct score."""
        player_pebbles = self.collectionRGWBY + self.collectionRWB
        score = self.sad_cardRGWBY.score_if_bought(player_pebbles)

        self.assertEqual(score, 1)
        player_pebbles = self.collectionRGGBY + self.collectionRWB
        score = self.sad_cardRGGBY.score_if_bought(player_pebbles)

        self.assertEqual(score, 1)

    def test_score_if_bought_happy_3left(self):
        wallet = self.collectionRGWBY + self.collectionRGWBY
        score = RuleBook.score_if_bought(self.happy_cardRGWBY, wallet)
        self.assertEqual(score, 2)

    def test_score_if_bought_happy_3left(self):
        wallet = self.collectionRGWBY
        score = RuleBook.score_if_bought(self.happy_cardRGWBY, wallet)
        self.assertEqual(score, 8)

    def test_draw_bank_pebble(self):
        red = Pebble(color=PebbleColor.RED)
        green = Pebble(color=PebbleColor.GREEN)
        blue = Pebble(color=PebbleColor.BLUE)
        yellow = Pebble(color=PebbleColor.YELLOW)
        BRRGBY = [blue, red, red, green, blue, yellow]
        GBY = [green, blue, yellow]
        collection_empty = PebbleCollection(pebbles=tuple())
        collection_BRRGBY = PebbleCollection(pebbles=tuple(BRRGBY))
        collection_GBY = PebbleCollection(pebbles=tuple(GBY))
        self.assertIsNone(RuleBook.draw_bank_pebble(collection_empty))
        self.assertEqual(len(collection_BRRGBY.pebbles), 6)
        self.assertEqual(RuleBook.draw_bank_pebble(collection_BRRGBY), red)
        self.assertEqual(RuleBook.draw_bank_pebble(collection_BRRGBY), red)
        self.assertEqual(RuleBook.draw_bank_pebble(collection_BRRGBY), blue)
        self.assertEqual(len(collection_BRRGBY.pebbles), 3)
        self.assertEqual(collection_BRRGBY, collection_GBY)


if __name__ == "__main__":
    unittest.main()
