import unittest
from collections import Counter

import pydantic_core

from pebble import *


class TestPebbleMethods(unittest.TestCase):

    def test_pebble_str(self):
        """Test the __str__ method of Pebble class."""
        red_pebble = Pebble(color=PebbleColor.RED)
        green_pebble = Pebble(color=PebbleColor.GREEN)
        yellow_pebble = Pebble(color=PebbleColor.YELLOW)
        blue_pebble = Pebble(color=PebbleColor.BLUE)
        white_pebble = Pebble(color=PebbleColor.WHITE)

        self.assertEqual(str(red_pebble), "r")
        self.assertEqual(str(green_pebble), "g")
        self.assertEqual(str(yellow_pebble), "y")
        self.assertEqual(str(blue_pebble), "b")
        self.assertEqual(str(white_pebble), "w")


class TestPebbleCollection(unittest.TestCase):

    def setUp(self):
        self.red = Pebble(color=PebbleColor.RED)
        self.green = Pebble(color=PebbleColor.GREEN)
        self.blue = Pebble(color=PebbleColor.BLUE)
        self.yellow = Pebble(color=PebbleColor.YELLOW)

        self.collection1 = PebbleCollection(pebbles=tuple([self.red, self.green]))
        self.collection2 = PebbleCollection(pebbles=tuple([self.blue, self.yellow]))
        self.collection3 = PebbleCollection(
            pebbles=tuple([self.red, self.green, self.blue])
        )
        self.empty_collection = PebbleCollection(pebbles=tuple())

    def test_add_pebble_collections(self):
        """Test adding two PebbleCollection instances."""
        result = self.collection1 + self.collection2
        expected = PebbleCollection(
            pebbles=tuple([self.red, self.green, self.blue, self.yellow])
        )
        self.assertEqual(result, expected)

    def test_invalid_addition(self):
        """Test that adding an invalid type raises a TypeError."""
        with self.assertRaises(TypeError):
            _ = self.collection1 + 5

    def test_subtract_pebble_collections(self):
        """Test subtracting one PebbleCollection from another."""
        result = self.collection3 - self.collection1
        expected = PebbleCollection(pebbles=tuple([self.blue]))
        self.assertEqual(result, expected)

        # Test subtracting when not enough pebbles are present
        result = self.collection1 - self.collection3
        self.assertEqual(result, self.collection1)
        # Test subtracting when they have the same pebble
        result = self.collection1 - self.collection1
        expected = PebbleCollection(pebbles=tuple())
        self.assertEqual(result, expected)

    def test_invalid_subtraction(self):
        """Test that subtracting an invalid type raises a TypeError."""
        with self.assertRaises(TypeError):
            _ = self.collection1 - 5

    def test_equality_of_pebble_collections(self):
        """Test the equality operator for PebbleCollection."""
        collection1_copy = PebbleCollection(pebbles=tuple([self.green, self.red]))
        self.assertEqual(self.collection1, collection1_copy)
        self.assertNotEqual(self.collection1, self.collection2)

        # check the order of equations for pebbles should not matter
        collection1_copy_diff_ordered = PebbleCollection(
            pebbles=tuple([self.red, self.green])
        )
        self.assertEqual(self.collection1, collection1_copy_diff_ordered)

        collection3_copy_diff_ordered = PebbleCollection(
            pebbles=tuple([self.blue, self.green, self.red])
        )
        self.assertEqual(self.collection3, collection3_copy_diff_ordered)

    def test_subset_of_pebble_collections(self):
        """Test if a PebbleCollection is a subset of another."""
        collection_subset = PebbleCollection(pebbles=tuple([self.green]))
        self.assertTrue(collection_subset.subset_of(self.collection1))
        self.assertFalse(self.collection1.subset_of(self.collection2))
        # Case where collection1 is not a subset (same pebbles, different amount)
        collection3 = PebbleCollection(pebbles=tuple([self.red, self.red]))
        collection4 = PebbleCollection(pebbles=tuple([self.red]))
        self.assertFalse(collection3.subset_of(collection4))

        # Case where collections are equal
        collection3_copy = PebbleCollection(
            pebbles=tuple([self.red, self.green, self.blue])
        )
        self.assertTrue(collection3_copy.subset_of(self.collection3))

        # Case where collection is empty (empty set is a subset of any set)
        collection_empty = PebbleCollection(pebbles=tuple())
        self.assertTrue(collection_empty.subset_of(self.collection2))
        self.assertTrue(collection_empty.subset_of(self.collection1))

        # Case where other collection is empty
        self.assertFalse(self.collection1.subset_of(collection_empty))

    def test_pebble_collection_list_str(self):
        """Test the __str__ method of PebbleCollection class."""
        list_allpebbles = list_of_all_pebbles()
        four_red = PebbleCollection(
            pebbles=tuple(
                [
                    self.red,
                    self.red,
                    Pebble(color=PebbleColor.RED),
                    self.red,
                ]
            )
        )

        self.assertEqual(list_allpebbles.__list_str__(), ["b", "g", "r", "w", "y"])
        self.assertEqual(self.collection1.__list_str__(), ["g", "r"])
        self.assertEqual(self.collection2.__list_str__(), ["b", "y"])
        self.assertEqual(four_red.__list_str__(), ["r", "r", "r", "r"])

    def test_less_than_comparison(self):
        """Test the less than comparison between PebbleCollection instances."""
        smaller_collection = PebbleCollection(pebbles=tuple([self.red]))
        collection3_copy = PebbleCollection(
            pebbles=tuple([self.red, self.green, self.blue])
        )
        # case where collectionsa are equal
        self.assertFalse(collection3_copy < self.collection3)
        self.assertTrue(smaller_collection < self.collection1)
        self.assertFalse(self.collection1 < smaller_collection)

    def test_empty_collection(self):
        """Test that an empty PebbleCollection works as expected."""
        result = self.empty_collection + self.collection1
        self.assertEqual(result, self.collection1)

        result = self.empty_collection - self.collection1
        self.assertEqual(result, self.empty_collection)

    def test_list_of_all_pebbles(self):
        """Test that list_of_all_pebbles returns all pebbles."""
        result = list_of_all_pebbles()
        expected_colors = {
            PebbleColor.RED.value,
            PebbleColor.GREEN.value,
            PebbleColor.BLUE.value,
            PebbleColor.YELLOW.value,
            PebbleColor.WHITE.value,
        }
        result_colors = set([pebble.color for pebble in result.pebbles])
        self.assertEqual(result_colors, expected_colors)

    def test_pebblecollection_frozen(self):
        red = Pebble(color=PebbleColor.RED)
        green = Pebble(color=PebbleColor.GREEN)
        blue = Pebble(color=PebbleColor.BLUE)
        yellow = Pebble(color=PebbleColor.YELLOW)
        listRGBY = tuple([red, green, blue, yellow])

        collectionRGBY = PebbleCollection(pebbles=tuple(listRGBY))
        # try to mutate list
        self.assertEqual(collectionRGBY.pebbles, listRGBY)
        listRGBY_copy = tuple([red, green, blue, yellow])
        listRGBY = tuple([red, green, blue, blue, blue, blue, yellow])
        self.assertEqual(len(listRGBY), 7)
        self.assertNotEqual(collectionRGBY.pebbles, listRGBY)
        self.assertEqual(collectionRGBY.pebbles, listRGBY_copy)
        # try to mutate an item in the list
        red = Pebble(color=PebbleColor.GREEN)
        listRGBY = tuple([red, green, blue, yellow])
        self.assertEqual(red, green)
        self.assertNotEqual(collectionRGBY.pebbles, listRGBY)
        self.assertEqual(collectionRGBY.pebbles, listRGBY_copy)

    def test_draw_pebble(self):
        red = Pebble(color=PebbleColor.RED)
        green = Pebble(color=PebbleColor.GREEN)
        blue = Pebble(color=PebbleColor.BLUE)
        yellow = Pebble(color=PebbleColor.YELLOW)
        BRRGBY = [blue, red, red, green, blue, yellow]
        GBY = [green, blue, yellow]
        collection_empty = PebbleCollection(pebbles=tuple())
        collection_BRRGBY = PebbleCollection(pebbles=tuple(BRRGBY))
        collection_GBY = PebbleCollection(pebbles=tuple(GBY))
        self.assertIsNone(collection_empty.draw_pebble())
        self.assertEqual(len(collection_BRRGBY.pebbles), 6)
        self.assertEqual(collection_BRRGBY.draw_pebble(), red)
        self.assertEqual(collection_BRRGBY.draw_pebble(), red)
        self.assertEqual(collection_BRRGBY.draw_pebble(), blue)
        self.assertEqual(len(collection_BRRGBY.pebbles), 3)
        self.assertEqual(collection_BRRGBY, collection_GBY)

    def test_init_bank(self):
        bank = init_bank()
        self.assertEqual(len(bank.pebbles), 100)
        red = Pebble(color=PebbleColor.RED)
        green = Pebble(color=PebbleColor.GREEN)
        blue = Pebble(color=PebbleColor.BLUE)
        yellow = Pebble(color=PebbleColor.YELLOW)
        white = Pebble(color=PebbleColor.WHITE)
        self.assertEqual(bank.pebbles.count(red), 20)
        self.assertEqual(bank.pebbles.count(green), 20)
        self.assertEqual(bank.pebbles.count(blue), 20)
        self.assertEqual(bank.pebbles.count(yellow), 20)
        self.assertEqual(bank.pebbles.count(white), 20)


if __name__ == "__main__":
    unittest.main()
