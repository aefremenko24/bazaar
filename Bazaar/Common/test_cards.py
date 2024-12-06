import json
import unittest
from collections import Counter

import pydantic_core
from pydantic import ValidationError

from Bazaar.Common.cards import *
from Bazaar.Common.pebble import Pebble, PebbleCollection


class TestCards(unittest.TestCase):
    def setUp(self):
        self.red = Pebble(color=PebbleColor.RED)
        self.green = Pebble(color=PebbleColor.GREEN)
        self.blue = Pebble(color=PebbleColor.BLUE)
        self.yellow = Pebble(color=PebbleColor.YELLOW)
        self.white = Pebble(color=PebbleColor.WHITE)

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

    def test_pebble_count_valid(self):
        """Test that a card with exactly PEBBLE_COUNT pebbles is valid."""
        card = Card(pebbles=self.collectionRGWBY, happy_face=False)
        self.assertEqual(len(card.pebbles.pebbles), 5)

    def test_pebble_count_invalid(self):
        """Test that a card with more or fewer than 5 pebbles raises an error."""
        invalid_pebble_collection = PebbleCollection(
            list_of_pebbles=[self.red, self.green, self.blue]
        )
        with self.assertRaises(ValueError) as context:
            Card(pebbles=invalid_pebble_collection, happy_face=True)

    def test_can_purchase_card_true(self):
        """Test can_purchase_card method when the card can be bought."""
        player_pebbles = PebbleCollection(
            list_of_pebbles=[self.red, self.green, self.blue, self.white, self.yellow]
        )
        self.assertTrue(self.happy_cardRGWBY.can_purchase_card(player_pebbles))

    def test_can_purchase_card_true_larger_wallet(self):
        """Test can_purchase_card method when the card can be bought."""
        player_pebbles = PebbleCollection(
            list_of_pebbles=[
                self.red,
                self.green,
                self.blue,
                self.white,
                self.blue,
                self.yellow,
                self.yellow,
            ]
        )
        self.assertTrue(self.happy_cardRGWBY.can_purchase_card(player_pebbles))

    def test_can_purchase_card_false(self):
        """Test can_purchase_card method when the card cannot be bought."""
        player_pebbles = PebbleCollection(list_of_pebbles=[self.red, self.white])
        self.assertFalse(self.happy_cardRGWBY.can_purchase_card(player_pebbles))

    def test_can_purchase_card_false_five(self):
        """Test can_purchase_card method when the card cannot be bought."""
        player_pebbles = PebbleCollection(
            list_of_pebbles=[self.red, self.white, self.blue, self.yellow, self.yellow]
        )
        self.assertFalse(self.happy_cardRGWBY.can_purchase_card(player_pebbles))

    def test_purchase_card_empty_wallet(self):
        """Test purchase method correctly updates the player's wallet and the bank."""
        player_pebbles = PebbleCollection(
            list_of_pebbles=[self.red, self.green, self.white, self.blue, self.yellow]
        )
        bank_pebbles = PebbleCollection(
            list_of_pebbles=[self.blue, self.yellow, self.white]
        )
        updated_player_pebbles, updated_bank_pebbles = self.happy_cardRGWBY.purchase(
            player_pebbles, bank_pebbles
        )

        expected_player_pebbles = PebbleCollection(list_of_pebbles=[])
        expected_bank_pebbles = bank_pebbles + self.collectionRGWBY

        self.assertEqual(
            Counter(updated_player_pebbles.pebbles),
            Counter(expected_player_pebbles.pebbles),
        )
        self.assertEqual(
            Counter(updated_bank_pebbles.pebbles),
            Counter(expected_bank_pebbles.pebbles),
        )

    def test_purchase_card_4_left_wallet(self):
        """Test purchase method correctly updates the player's wallet and the bank."""
        player_pebbles = self.collectionRGWBY + self.collectionRGBY
        bank_pebbles = PebbleCollection(
            list_of_pebbles=[self.blue, self.yellow, self.white]
        )
        updated_player_pebbles, updated_bank_pebbles = self.happy_cardRGWBY.purchase(
            player_pebbles, bank_pebbles
        )

        expected_player_pebbles = self.collectionRGBY
        expected_bank_pebbles = bank_pebbles + self.collectionRGWBY

        self.assertEqual(
            Counter(updated_player_pebbles.pebbles),
            Counter(expected_player_pebbles.pebbles),
        )
        self.assertEqual(
            Counter(updated_bank_pebbles.pebbles),
            Counter(expected_bank_pebbles.pebbles),
        )

    def test_purchase_card_3_left_wallet(self):
        """Test purchase method correctly updates the player's wallet and the bank."""
        player_pebbles = self.collectionRGWBY + self.collectionRRB
        bank_pebbles = PebbleCollection(
            list_of_pebbles=[self.blue, self.yellow, self.white]
        )
        updated_player_pebbles, updated_bank_pebbles = self.happy_cardRGWBY.purchase(
            player_pebbles, bank_pebbles
        )

        expected_player_pebbles = self.collectionRRB
        expected_bank_pebbles = bank_pebbles + self.collectionRGWBY

        self.assertEqual(
            Counter(updated_player_pebbles.pebbles),
            Counter(expected_player_pebbles.pebbles),
        )
        self.assertEqual(
            Counter(updated_bank_pebbles.pebbles),
            Counter(expected_bank_pebbles.pebbles),
        )

    def test_generate(self):
        print(Card.generate_random())

    def test_serialize(self):
        card = Card.generate_random()
        print(card.serialize())

        cards = Cards.generate_random(20)
        print(cards.serialize())

    def test_card_equality_True(self):
        happy_cardRGWBY_copy = Card(pebbles=self.collectionRGWBY, happy_face=True)
        self.assertEqual(self.happy_cardRGWBY, happy_cardRGWBY_copy)

        collectionRGWBY_copy = PebbleCollection(
            list_of_pebbles=[self.red, self.green, self.white, self.blue, self.yellow]
        )
        happy_cardRGWBY_copy2 = Card(pebbles=collectionRGWBY_copy, happy_face=True)
        self.assertEqual(self.happy_cardRGWBY, happy_cardRGWBY_copy2)
        sad_cardRGWBY_copy = Card(pebbles=self.collectionRGWBY, happy_face=False)
        self.assertEqual(self.sad_cardRGWBY, sad_cardRGWBY_copy)

        sad_cardRGWBY_copy2 = Card(pebbles=collectionRGWBY_copy, happy_face=False)
        self.assertEqual(self.sad_cardRGWBY, sad_cardRGWBY_copy2)

    def test_card_equality_False(self):
        self.assertNotEqual(self.sad_cardRGWBY, self.happy_cardRGWBY)

        collectionRGWBY_copy = PebbleCollection(
            list_of_pebbles=[self.red, self.green, self.white, self.blue, self.yellow]
        )
        happy_cardRGWBY_copy1 = Card(pebbles=collectionRGWBY_copy, happy_face=True)
        self.assertNotEqual(self.sad_cardRGWBY, self.happy_cardRGWBY)
        self.assertNotEqual(self.happy_cardRGWBY, self.happy_cardRGGBY)
        self.assertNotEqual(self.sad_cardRGWBY, self.sad_cardRGGBY)

    def test_card_frozen(self):
        collectionRGWBY = PebbleCollection(
            list_of_pebbles=[self.red, self.green, self.white, self.blue, self.yellow]
        )
        happy_card = Card(pebbles=collectionRGWBY, happy_face=True)
        self.assertEqual(happy_card.pebbles, collectionRGWBY)
        collectionRGWBY = self.collectionRGBY
        self.assertNotEqual(happy_card.pebbles, collectionRGWBY)
        self.assertEqual(happy_card.pebbles, self.collectionRGWBY)

        # test that trying to modify the pebbles raises an error
        with self.assertRaises(pydantic_core.ValidationError):
            happy_card.pebbles = self.collectionRGBY
        self.assertEqual(happy_card.pebbles, self.collectionRGWBY)

        # test that trying to modify the pebbles raises an error
        with self.assertRaises(pydantic_core.ValidationError):
            happy_card.happy_face = False
        self.assertEqual(happy_card.happy_face, True)


class TestCards(unittest.TestCase):

    def setUp(self):
        """
        Setup test data before each test case.
        """
        self.red = Pebble(color=PebbleColor.RED)
        self.green = Pebble(color=PebbleColor.GREEN)
        self.blue = Pebble(color=PebbleColor.BLUE)
        self.yellow = Pebble(color=PebbleColor.YELLOW)
        self.white = Pebble(color=PebbleColor.WHITE)

        self.collectionRRGGW = PebbleCollection(
            pebbles=tuple([self.red, self.green, self.red, self.green, self.white])
        )
        self.collectionBY = PebbleCollection(pebbles=tuple([self.blue, self.yellow]))
        self.collectionRGW = PebbleCollection(
            pebbles=tuple([self.red, self.green, self.white])
        )
        self.collectionRWB = PebbleCollection(
            pebbles=tuple([self.red, self.white, self.blue])
        )

        self.cardRRGGW = Card(pebbles=self.collectionRRGGW, happy_face=True)
        self.cardRGWBY = Card(
            pebbles=self.collectionRGW + self.collectionBY, happy_face=False
        )
        self.cardRWBBY = Card(
            pebbles=self.collectionRWB + self.collectionBY, happy_face=False
        )

        self.cards = Cards(cards=[self.cardRRGGW, self.cardRGWBY, self.cardRWBBY])

    def test_cards_initialization(self):
        """
        Test the initialization of Cards with valid Card instances.
        """
        self.assertEqual(len(self.cards.cards), 3)
        self.assertIn(self.cardRRGGW, self.cards.cards)
        self.assertIn(self.cardRGWBY, self.cards.cards)

    def test_cards_generate_random(self):
        random_cards = Cards.generate_random(5)
        self.assertEqual(len(random_cards.cards), 5)
        self.assertIsInstance(random_cards.cards[0], Card)

    def test_find_matching_cards(self):

        player_wallet = PebbleCollection(
            pebbles=[self.red, self.red, self.green, self.green, self.white]
        )
        matching_cards = self.cards.find_matching_cards(player_wallet)

        self.assertEqual(len(matching_cards.cards), 1)
        self.assertIn(self.cardRRGGW, matching_cards.cards)

    def test_find_matching_cards_empty(self):
        player_wallet = PebbleCollection(
            pebbles=[self.red, self.green, self.white]
        )
        matching_cards = self.cards.find_matching_cards(player_wallet)

        self.assertEqual(len(matching_cards.cards), 0)

    def test_find_matching_cards_2(self):
        player_wallet = PebbleCollection(
            pebbles=[
                self.red,
                self.red,
                self.green,
                self.green,
                self.white,
                self.blue,
                self.yellow,
            ]
        )
        matching_cards = self.cards.find_matching_cards(player_wallet)

        self.assertEqual(len(matching_cards.cards), 2)
        self.assertIn(self.cardRRGGW, matching_cards.cards)
        self.assertIn(self.cardRGWBY, matching_cards.cards)

    def test_is_empty(self):

        empty_cards = Cards(cards=[])
        self.assertTrue(empty_cards.is_empty())

        non_empty_cards = Cards(cards=[self.cardRRGGW])
        self.assertFalse(non_empty_cards.is_empty())

    def test_cards_sorted(self):
        """
        Test the sorted method to ensure that Cards are sorted by pebbles and happy face.
        """
        sorted_cards = self.cards.sorted()
        self.assertEqual(len(sorted_cards.cards), 3)

        self.assertEqual(sorted_cards.cards[0], self.cardRWBBY)

    def test_cards_serialization(self):
        """
        Test the serialization and deserialization of Cards.
        """
        serialized_cards = self.cards.serialize()
        self.assertEqual(len(serialized_cards), 3)
        self.assertIsInstance(serialized_cards[0], dict)

        deserialized_cards = Cards.deserialize(serialized_cards)
        self.assertEqual(len(deserialized_cards.cards), 3)
        self.assertEqual(deserialized_cards.cards[0], self.cardRRGGW)

    def test_cards_lt(self):
        """
        Test the __lt__ method for comparing two Cards objects by length and pebbles.
        """
        shorter_cards = Cards(cards=[self.cardRRGGW])
        self.assertTrue(shorter_cards < self.cards)

        same_length_cards = Cards(
            cards=[self.cardRRGGW, self.cardRGWBY, self.cardRWBBY]
        )
        self.assertFalse(same_length_cards < self.cards)

        # bigger card at same index but same lengh
        cardRWBBY = Card(
            pebbles=self.collectionRWB + self.collectionBY, happy_face=True
        )

        bigger_card_length = Cards(cards=[self.cardRRGGW, self.cardRRGGW,self.cardRGWBY])
        self.assertFalse(bigger_card_length < self.cards)

    def test_cards_contains(self):
        self.assertIn(self.cardRGWBY, self.cards)

    def test_invalid_card_count(self):
        """
        Test that Cards cannot be initialized with more than 20 cards or less than 0 cards.
        """
        with self.assertRaises(ValidationError):
            too_many_cards = Cards(cards=[self.cardRRGGW] * 21)



if __name__ == "__main__":
    unittest.main(argv=[""], exit=False)
