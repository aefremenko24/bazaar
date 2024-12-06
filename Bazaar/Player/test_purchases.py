import unittest

from Bazaar.Common.pebble import Pebble, PebbleColor, PebbleCollection
from purchases import (
    PurchaseSequence,
    PurchaseSequences,
    find_all_possible_purchase,
    search_all_possible,
    add_if_better,
)
from Bazaar.Common.cards import Card, Cards

red_pebble = Pebble(color=PebbleColor.RED)
blue_pebble = Pebble(color=PebbleColor.BLUE)
green_pebble = Pebble(color=PebbleColor.GREEN)
yellow_pebble = Pebble(color=PebbleColor.YELLOW)
white_pebble = Pebble(color=PebbleColor.WHITE)


class TestPurchaseSequence(unittest.TestCase):
    def setUp(self):
        # Initialize pebbles of different colors
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

        self.cards_RGWBY = Cards(cards=[self.happy_cardRGWBY, self.sad_cardRGWBY])
        self.cards_RGGBY = Cards(cards=[self.happy_cardRGGBY, self.sad_cardRGGBY])

        # Define a bank for testing
        self.bank = PebbleCollection(
            pebbles=(self.red, self.green, self.blue, self.yellow, self.white)
        )

    def test_find_all_possible_purchases_one_card_purchase(self):
        """
        Test find_all_possible_purchase with cards that can be purchased with the initial wallet.
        """
        wallet = self.collectionRGWBY
        candidates = find_all_possible_purchase(self.cards_RGWBY, wallet, self.bank)
        self.assertTrue(len(candidates) == 1)

        for purchase in candidates:
            self.assertIsInstance(purchase, PurchaseSequence)
            # Check that the wallet has been updated correctly
            self.assertTrue(
                all(card in self.cards_RGWBY for card in purchase.sequence.cards)
            )

    def test_find_all_possible_purchases_no_valid(self):
        """
        Test find_all_possible_purchase with a wallet that cannot purchase any cards.
        """
        wallet = PebbleCollection(pebbles=(self.red,))
        candidates = find_all_possible_purchase(self.cards_RGWBY, wallet, self.bank)

        # Assert that no purchase sequences were found because the wallet lacks enough pebbles
        self.assertEqual(len(candidates), 0)

    def test_find_all_possible_purchases_two_purchase(self):
        """
        Test find_all_possible_purchase with cards that can be purchased with the initial wallet in a optimal order.
        """
        wallet = self.collectionRGWBY + self.collectionRGWBY
        candidates = find_all_possible_purchase(self.cards_RGWBY, wallet, self.bank)
        print(candidates)
        self.assertTrue(len(candidates[0].sequence.cards) == 2)

        for purchase in candidates:
            self.assertIsInstance(purchase, PurchaseSequence)
            self.assertTrue(
                all(card in self.cards_RGWBY for card in purchase.sequence.cards)
            )

        self.assertEqual(candidates[0].sequence.cards[0], self.happy_cardRGWBY)
        self.assertEqual(candidates[0].sequence.cards[1], self.sad_cardRGWBY)

    def test_find_all_possible_purchases_two_purchase_tw0_candidates(self):
        """
        Test find_all_possible_purchase with cards that can be purchased with the initial wallet in a optimal order.
        """
        wallet = self.collectionRGWBY + self.collectionRGGBY
        two_cards = Cards(cards=[self.happy_cardRGWBY, self.happy_cardRGGBY])
        candidates = find_all_possible_purchase(two_cards, wallet, self.bank, "purchase-points")
        print(candidates)
        self.assertEqual(len(candidates),2)
        self.assertTrue(len(candidates[0].sequence.cards) == 2)
        self.assertTrue(len(candidates[1].sequence.cards) == 2)
        expected1 = PurchaseSequence(
            sequence=Cards(cards= [self.happy_cardRGWBY, self.happy_cardRGGBY]),
            points=10,
            wallet=PebbleCollection(),
            bank = self.bank+ self.collectionRGWBY + self.collectionRGGBY
        )
        expected2 = PurchaseSequence(
            sequence=Cards(cards=[ self.happy_cardRGGBY, self.happy_cardRGWBY]),
            points=10,
            wallet=PebbleCollection(),
            bank=self.bank+  self.collectionRGGBY +self.collectionRGWBY
        )

        self.assertEqual(expected1,candidates[0])
        self.assertEqual(expected2,candidates[1])
    def test_search_all_possible(self):
        """
        Test search_all_possible to ensure it finds sequences that improve the candidates.
        """
        wallet = PebbleCollection(pebbles=(self.red, self.green, self.blue))
        initial_purchase = PurchaseSequence(
            sequence=Cards(), points=0, wallet=wallet, bank=self.bank
        )
        candidates = []

        search_all_possible(self.cards_RGGBY, initial_purchase, candidates)

        self.assertTrue(len(candidates) == 0)
        for purchase in candidates:
            self.assertIsInstance(purchase, PurchaseSequence)
            self.assertTrue(
                all(card in self.cards_RGGBY for card in purchase.sequence.cards)
            )

    def test_add_if_better(self):
        """
        Test add_if_better to ensure it adds better scoring sequences or retains sequences with equal scores.
        """
        wallet = PebbleCollection(pebbles=(self.red, self.green, self.blue))
        purchase1 = PurchaseSequence(
            sequence=Cards(), points=5, wallet=wallet, bank=self.bank
        )
        purchase2 = PurchaseSequence(
            sequence=Cards(), points=7, wallet=wallet, bank=self.bank
        )
        purchase3 = PurchaseSequence(
            sequence=Cards(), points=7, wallet=wallet, bank=self.bank
        )
        candidates = [purchase1]

        add_if_better(candidates, purchase2)
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0].points, 7)

        add_if_better(candidates, purchase3)
        self.assertEqual(len(candidates), 2)
        self.assertTrue(purchase2 in candidates)
        self.assertTrue(purchase3 in candidates)


if __name__ == "__main__":
    unittest.main()
