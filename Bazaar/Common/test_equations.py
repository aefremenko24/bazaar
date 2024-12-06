import json
import unittest
from collections import Counter

import pydantic_core
from pydantic import ValidationError

from Bazaar.Common.equations import Equation, Equations
from Bazaar.Common.pebble import Pebble, PebbleColor, PebbleCollection

MIN_EQUATION_SIZE = 1
MAX_EQUATION_SIZE = 4


class TestEquation(unittest.TestCase):

    def setUp(self):
        self.red = Pebble(color=PebbleColor.RED)
        self.green = Pebble(color=PebbleColor.GREEN)
        self.blue = Pebble(color=PebbleColor.BLUE)
        self.yellow = Pebble(color=PebbleColor.YELLOW)
        self.white = Pebble(color=PebbleColor.WHITE)

        self.collectionRG = PebbleCollection(pebbles=tuple([self.red, self.green]))
        self.collectionBY = PebbleCollection(pebbles=tuple([self.blue, self.yellow]))
        self.collectionRGB = PebbleCollection(
            pebbles=tuple([self.red, self.green, self.blue])
        )
        self.empty_collection = PebbleCollection(pebbles=())

    def test_validate_equation_valid(self):
        """Test with valid lhs and rhs having different colors and valid lengths."""

        lhs = PebbleCollection(
            pebbles=(
                Pebble(color=PebbleColor.RED),
                Pebble(color=PebbleColor.GREEN),
            )
        )
        rhs = PebbleCollection(
            pebbles=(
                Pebble(color=PebbleColor.BLUE),
                Pebble(color=PebbleColor.YELLOW),
            )
        )
        equation = Equation(lhs=lhs, rhs=rhs)
        self.assertEqual(equation.lhs, lhs)
        self.assertEqual(equation.rhs, rhs)

    def test_validate_equation_invalid_length(self):
        """Test that an exception is raised if lhs or rhs is outside the valid length."""
        lhs = PebbleCollection(pebbles=(Pebble(color=PebbleColor.RED)))
        rhs = PebbleCollection(
            pebbles=tuple([Pebble(color=PebbleColor.BLUE)] * 5)
        )  # Invalid length (5 pebbles)

        with self.assertRaises(ValidationError) as context:
            Equation(lhs=lhs, rhs=rhs)
        self.assertIn("must have between 1 and 4 pebbles", str(context.exception))
        rhs = PebbleCollection(pebbles=tuple([Pebble(color=PebbleColor.RED)]))
        lhs = PebbleCollection(pebbles=tuple([Pebble(color=PebbleColor.BLUE)] * 5))
        with self.assertRaises(ValidationError) as context:
            Equation(lhs=lhs, rhs=rhs)
        self.assertIn("must have between 1 and 4 pebbles", str(context.exception))

    def test_validate_equation_same_colors(self):
        """Test that an exception is raised if lhs and rhs have overlapping colors."""
        lhs = PebbleCollection(
            pebbles=tuple([
                Pebble(color=PebbleColor.RED),
                Pebble(color=PebbleColor.GREEN),
            ])
        )
        rhs = PebbleCollection(
            pebbles=tuple([
                Pebble(color=PebbleColor.RED),
                Pebble(color=PebbleColor.BLUE),
            ])
        )  # 'RED' is common

        with self.assertRaises(ValidationError) as context:
            Equation(lhs=lhs, rhs=rhs)
        self.assertIn(
            "Each side of the equation must have different colored pebbles",
            str(context.exception),
        )

    def test_invalid_pebble_collection_instance(self):
        """Test that an exception is raised if lhs or rhs is not a PebbleCollection."""
        lhs = [Pebble(color=PebbleColor.RED), Pebble(color=PebbleColor.GREEN)]
        rhs = PebbleCollection(
            pebbles=tuple([
                Pebble(color=PebbleColor.BLUE),
                Pebble(color=PebbleColor.YELLOW),
            ])
        )
        values = {"lhs": lhs, "rhs": rhs}

        with self.assertRaises(TypeError) as context:
            Equation.validate_equation(values)
        self.assertIn(
            "lhs and rhs must be instances of PebbleCollection", str(context.exception)
        )

    def test_equation_equality_directed(self):
        """Test equality of directed equations."""
        eq1 = Equation(lhs=self.collectionRG, rhs=self.collectionBY, directed=True)
        eq2 = Equation(lhs=self.collectionRG, rhs=self.collectionBY, directed=True)

        self.assertTrue(eq1 == eq2)
        eq2 = Equation(lhs=self.collectionRG, rhs=self.collectionBY, directed=False)
        self.assertTrue(eq1 == eq2)

    def test_equation_inequality_different_lhs_rhs(self):
        """Test inequality of directed equations with different lhs or rhs."""
        eq1 = Equation(lhs=self.collectionRG, rhs=self.collectionBY, directed=True)
        collection2_altered = PebbleCollection(
            pebbles=tuple([self.blue, self.yellow, self.yellow])
        )
        eq2 = Equation(lhs=self.collectionRG, rhs=collection2_altered, directed=True)

        self.assertFalse(eq1 == eq2)

    def test_equation_equality_undirected(self):
        """Test equality of undirected equations (both directions)."""
        eq1 = Equation(lhs=self.collectionRG, rhs=self.collectionBY, directed=False)
        eq2 = Equation(lhs=self.collectionBY, rhs=self.collectionRG, directed=False)
        collection2_copy = PebbleCollection(pebbles=tuple([self.blue, self.yellow]))
        eq3 = Equation(lhs=self.collectionRG, rhs=self.collectionBY)
        eq4 = Equation(lhs=collection2_copy, rhs=self.collectionRG, directed=False)
        self.assertTrue(eq1 == eq2)
        self.assertTrue(eq1 == eq3)
        self.assertTrue(eq1 == eq4)

    def test_trade_equation_valid(self):
        """
        Test that a valid trade correctly updates both player and bank pebble collections.
        """
        lhs = self.collectionRG
        rhs = self.collectionBY
        equation = Equation(lhs=lhs, rhs=rhs, directed=True)

        player_pebbles = PebbleCollection(
            pebbles=tuple([self.red, self.green, self.white])
        )
        bank_pebbles = PebbleCollection(
            pebbles = tuple([self.blue, self.yellow, self.white])
        )
        updated_player_pebbles, updated_bank_pebbles = equation.trade_equation(
            player_pebbles, bank_pebbles
        )

        # Expected results
        expected_player_pebbles = PebbleCollection(
            pebbles=tuple([self.white, self.blue, self.yellow])
        )
        expected_bank_pebbles = PebbleCollection(
            pebbles=tuple([self.white, self.red, self.green])
        )

        # Verify the trade result
        self.assertEqual(
            Counter(updated_player_pebbles.pebbles),
            Counter(expected_player_pebbles.pebbles),
        )
        self.assertEqual(
            Counter(updated_bank_pebbles.pebbles),
            Counter(expected_bank_pebbles.pebbles),
        )

    def test_trade_equation_directed(self):
        """
        Test that a directed equation only allows trades from LHS to RHS.
        """
        lhs = self.collectionRG
        rhs = self.collectionBY
        equation = Equation(lhs=lhs, rhs=rhs, directed=True)

        player_pebbles = PebbleCollection(
            pebbles=tuple([self.red, self.green, self.white])
        )
        bank_pebbles = PebbleCollection(
            pebbles=tuple([self.blue, self.yellow, self.white])
        )

        updated_player_pebbles, updated_bank_pebbles = equation.trade_equation(
            player_pebbles, bank_pebbles
        )

        expected_player_pebbles = PebbleCollection(
            pebbles=tuple([self.white, self.blue, self.yellow])
        )
        expected_bank_pebbles = PebbleCollection(
            pebbles=tuple([self.white, self.red, self.green])
        )

        self.assertEqual(
            Counter(updated_player_pebbles.pebbles),
            Counter(expected_player_pebbles.pebbles),
        )
        self.assertEqual(
            Counter(updated_bank_pebbles.pebbles),
            Counter(expected_bank_pebbles.pebbles),
        )

    def test_trade_equation_undirected(self):
        """
        Test that an undirected equation does not allow trades and both player and bank pebble collections remain unchanged.
        """
        lhs = self.collectionRG
        rhs = self.collectionBY
        equation = Equation(lhs=lhs, rhs=rhs, directed=False)

        player_pebbles = PebbleCollection(
            pebbles=tuple([self.red, self.green, self.white])
        )
        bank_pebbles = PebbleCollection(
            pebbles=tuple([self.blue, self.yellow, self.white])
        )

        initial_player_pebbles = PebbleCollection(
            pebbles=tuple(player_pebbles.pebbles)
        )
        initial_bank_pebbles = PebbleCollection(
            pebbles=tuple(bank_pebbles.pebbles)
        )

        updated_player_pebbles, updated_bank_pebbles = equation.trade_equation(
            player_pebbles, bank_pebbles
        )

        # remain unchanged
        self.assertEqual(
            Counter(updated_player_pebbles.pebbles),
            Counter(initial_player_pebbles.pebbles),
        )
        self.assertEqual(
            Counter(updated_bank_pebbles.pebbles), Counter(initial_bank_pebbles.pebbles)
        )



    def test_equation_frozen_test(self):
        collectionBY = PebbleCollection(pebbles=(self.blue, self.yellow))
        collectionRG = PebbleCollection(pebbles=(self.red, self.green))
        eqBY_RG = Equation(lhs=collectionBY, rhs=collectionRG)

        self.assertEqual(eqBY_RG.lhs, collectionBY)
        self.assertEqual(eqBY_RG.rhs, collectionRG)
        collectionBY_copy = PebbleCollection(pebbles=(self.blue, self.yellow))
        collectionBY = PebbleCollection(
            pebbles=(self.blue, self.yellow, self.yellow)
        )
        self.assertNotEqual(eqBY_RG.lhs, collectionBY)
        self.assertEqual(eqBY_RG.lhs, collectionBY_copy)

        collectionRG_copy = PebbleCollection(pebbles=(self.red, self.green))
        collectionRG = PebbleCollection(
            pebbles=(self.blue, self.yellow, self.yellow)
        )
        self.assertNotEqual(eqBY_RG.rhs, collectionRG)
        self.assertEqual(eqBY_RG.rhs, collectionRG_copy)

        # test that trying to modify the pebbles raises an error
        with self.assertRaises(pydantic_core.ValidationError):
            eqBY_RG.lhs = collectionRG
        self.assertEqual(eqBY_RG.lhs, collectionBY_copy)

        # test that trying to modify the pebbles raises an error
        with self.assertRaises(pydantic_core.ValidationError):
            eqBY_RG.rhs = collectionBY
        self.assertEqual(eqBY_RG.rhs, collectionRG_copy)


class TestEquations(unittest.TestCase):
    def setUp(self):
        # Setting up reusable pebbles for the tests
        self.red = Pebble(color=PebbleColor.RED)
        self.green = Pebble(color=PebbleColor.GREEN)
        self.blue = Pebble(color=PebbleColor.BLUE)
        self.yellow = Pebble(color=PebbleColor.YELLOW)
        self.white = Pebble(color=PebbleColor.WHITE)
        self.equations = Equations(
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
                    lhs=PebbleCollection(pebbles=(self.red, self.blue)),
                    rhs=PebbleCollection(pebbles=(self.yellow, self.yellow)),
                ),
            }
        )

    def test_no_equations(self):
        """
        Tests cases where no equations can be used due to insufficient colors.
        Verifies that the result is an empty list.
        """
        """
              Tests cases where no equations can be used due to insufficient colors.
              Verifies that the result is an empty list.
              """
        equations = Equations(
            equations={
                Equation(
                    lhs=PebbleCollection(pebbles=(self.red, self.green)),
                    rhs=PebbleCollection(pebbles=(self.blue, self.yellow)),
                ),
                Equation(
                    lhs=PebbleCollection(pebbles
                                         =(self.green, self.green)),
                    rhs=PebbleCollection(pebbles
                                         =(self.white, self.yellow)),
                ),
                Equation(
                    lhs=PebbleCollection(pebbles
                                         =(self.red, self.blue)),
                    rhs=PebbleCollection(pebbles
                                         =(self.yellow, self.yellow)),
                ),
            }
        )

        my_colors = PebbleCollection(pebbles
                                     =(self.red, self.red))
        bank = PebbleCollection(
            pebbles
            =(
                self.red,
                self.red,
                self.green,
                self.green,
                self.green,
                self.blue,
            )
        )
        expected = []
        self.assertCountEqual(equations.filter_equations(my_colors, bank), expected)

    def test_generate(self):
        print(Equations.generate_random(2))

    def test_generate_random_equation(self):
        """
        test Generate a random equation, Check that the lhs and rhs have appropriate sizes,
        Check that the lhs and rhs do not have overlapping colors
        """

        equation = Equation.generate_random()

        self.assertGreaterEqual(
            len(equation.lhs.pebbles),
            MIN_EQUATION_SIZE,
            "LHS is smaller than MIN_EQUATION_SIZE",
        )
        self.assertLessEqual(
            len(equation.lhs.pebbles),
            MAX_EQUATION_SIZE,
            "LHS is larger than MAX_EQUATION_SIZE ",
        )
        self.assertGreaterEqual(
            len(equation.rhs.pebbles),
            MIN_EQUATION_SIZE,
            "RHS is smaller than MIN_EQUATION_SIZE",
        )
        self.assertLessEqual(
            len(equation.rhs.pebbles),
            MAX_EQUATION_SIZE,
            "RHS is larger than MAX_EQUATION_SIZE",
        )

        lhs_colors = {pebble.color for pebble in equation.lhs.pebbles}
        rhs_colors = {pebble.color for pebble in equation.rhs.pebbles}
        self.assertTrue(
            lhs_colors.isdisjoint(rhs_colors),
            "LHS and RHS should not have overlapping colors",
        )

    def test_random_equation_properties(self):
        # Generate multiple random equations to test the random behavior
        for _ in range(100):  # Test with 100 random equations
            equation = Equation.generate_random()

            # Ensure LHS and RHS are not empty
            self.assertTrue(equation.lhs, "LHS should not be empty")
            self.assertTrue(equation.rhs, "RHS should not be empty")

            # Ensure LHS and RHS have different colors
            lhs_colors = {pebble.color for pebble in equation.lhs.pebbles}
            rhs_colors = {pebble.color for pebble in equation.rhs.pebbles}
            self.assertTrue(
                lhs_colors.isdisjoint(rhs_colors),
                "LHS and RHS should not have overlapping colors",
            )

    def test_generate_random_equations_count(self):
        """
        Test that the number of generated equations matches the count specified.
        """
        count = 5
        equations = Equations.generate_random(count)
        self.assertEqual(
            len(equations.equations),
            count,
            f"Expected {count} equations, but got {len(equations.equations)}.",
        )
        count = 10
        equations = Equations.generate_random(count)
        self.assertEqual(
            len(equations.equations),
            count,
            f"Expected {count} equations, but got {len(equations.equations)}.",
        )
        count = 0
        equations = Equations.generate_random(count)
        self.assertEqual(
            len(equations.equations), 0, "Expected 0 equations but got more."
        )

    def test_generate_random_exceeds_max_length(self):
        """
        Test that generating more equations than the max length (10) raises a ValidationError.Check the error message
        as well
        """
        count = 20
        with self.assertRaises(ValidationError) as context:
            Equations.generate_random(count)
        self.assertIn("at most 10 items", str(context.exception))

    def test_generate_random_equations_validity(self):
        """
        Test that each generated equation is valid and adheres to the rules. For each equations, vaalidate lhs and rhs
        sizes and no overlap in colors
        """
        count = 10
        equations = Equations.generate_random(count)
        for eq in equations.equations:

            self.assertGreaterEqual(
                len(eq.lhs.pebbles),
                MIN_EQUATION_SIZE,
                "LHS size is less than minimum allowed.",
            )
            self.assertLessEqual(
                len(eq.lhs.pebbles),
                MAX_EQUATION_SIZE,
                "LHS size exceeds maximum allowed.",
            )
            self.assertGreaterEqual(
                len(eq.rhs.pebbles),
                MIN_EQUATION_SIZE,
                "RHS size is less than minimum allowed.",
            )
            self.assertLessEqual(
                len(eq.rhs.pebbles),
                MAX_EQUATION_SIZE,
                "RHS size exceeds maximum allowed.",
            )

            lhs_colors = {pebble.color for pebble in eq.lhs.pebbles}
            rhs_colors = {pebble.color for pebble in eq.rhs.pebbles}
            self.assertEqual(
                len(lhs_colors & rhs_colors), 0, "LHS and RHS have overlapping colors."
            )

    def test_generate_random_equations_no_duplicates(self):
        """
        Test that there are no duplicate equations in the generated set.
        """
        count = 10
        equations = Equations.generate_random(count)
        equations_set = set(equations.equations)
        self.assertEqual(
            len(equations_set),
            len(equations.equations),
            "There are duplicate equations in the generated set.",
        )

    def test_generate_random_equations_no_duplicates_100(self):
        """
        Test that there are no duplicate equations in the generated set, for 100 times
        """
        count = 10
        for _ in range(100):
            equations = Equations.generate_random(count)
            equations_set = set(equations.equations)
            self.assertEqual(
                len(equations_set),
                len(equations.equations),
                "There are duplicate equations in the generated set.",
            )

    def test_filter_equations_with_sufficient_pebbles(self):
        """
        Tests that equations can be filtered correctly when the player and bank have enough pebbles.
        """
        equations = Equations(
            equations={
                Equation(
                    lhs=PebbleCollection(pebbles
                                         =(self.red, self.green)),
                    rhs=PebbleCollection(pebbles
                                         =(self.blue, self.yellow)),
                ),
                Equation(
                    lhs=PebbleCollection(pebbles
                                         =(self.green, self.green)),
                    rhs=PebbleCollection(pebbles
                                         =(self.white, self.yellow)),
                ),
                Equation(
                    lhs=PebbleCollection(pebbles
                                         =(self.red, self.blue)),
                    rhs=PebbleCollection(pebbles
                                         =(self.yellow, self.yellow)),
                ),
            }
        )

        # case: one euqation one side
        player_pebbles = PebbleCollection(pebbles
                                          =(self.red, self.green))
        bank_pebbles = PebbleCollection(pebbles
                                        =(self.blue, self.yellow))

        filtered_equations = equations.filter_equations(player_pebbles, bank_pebbles)

        expected_equations = [
            Equation(
                lhs=PebbleCollection(pebbles
                                     =(self.red, self.green)),
                rhs=PebbleCollection(pebbles
                                     =(self.blue, self.yellow)),
                directed=True,
            )
        ]

        self.assertEqual(len(filtered_equations), len(expected_equations))
        for eq in filtered_equations:
            self.assertIn(eq, expected_equations)

    def test_filter_equations_with_sufficient_pebbles_both_sides(self):
        """
        Tests the filtering of equations with various sets of available colors.
        Verifies that only usable equations are returned based on color availability.
        """
        # Create the equations set using PebbleCollection instances and Equation class with conset

        player_pebbles_1 = PebbleCollection(
            pebbles
            =(self.red, self.green, self.blue, self.yellow)
        )
        player_pebbles_2 = PebbleCollection(
            pebbles
            =(self.red, self.green, self.green, self.blue, self.yellow)
        )

        bank_pebbles_1 = PebbleCollection(
            pebbles
            =(self.red, self.green, self.blue, self.yellow)
        )

        # case: one equation both sides
        filtered_equations = self.equations.filter_equations(
            player_pebbles_1, bank_pebbles_1
        )

        expected_equations = [
            Equation(
                lhs=PebbleCollection(pebbles
                                     =(self.red, self.green)),
                rhs=PebbleCollection(pebbles
                                     =(self.blue, self.yellow)),
                directed=True,
            ),
            Equation(
                lhs=PebbleCollection(pebbles
                                     =(self.blue, self.yellow)),
                rhs=PebbleCollection(pebbles
                                     =(self.red, self.green)),
                directed=True,
            ),
        ]

        self.assertEqual(len(filtered_equations), len(expected_equations))
        for eq in filtered_equations:
            self.assertIn(eq, expected_equations)

        # case one equation both side, one equation one side
        bank_pebbles_1 = PebbleCollection(
            pebbles
            =(self.red, self.green, self.blue, self.yellow, self.white)
        )
        filtered_equations = self.equations.filter_equations(
            player_pebbles_2, bank_pebbles_1
        )

        expected_equations = [
            Equation(
                lhs=PebbleCollection(pebbles
                                     =(self.red, self.green)),
                rhs=PebbleCollection(pebbles
                                     =(self.blue, self.yellow)),
                directed=True,
            ),
            Equation(
                lhs=PebbleCollection(pebbles
                                     =(self.blue, self.yellow)),
                rhs=PebbleCollection(pebbles
                                     =(self.red, self.green)),
                directed=True,
            ),
            Equation(
                lhs=PebbleCollection(pebbles
                                     =(self.green, self.green)),
                rhs=PebbleCollection(pebbles
                                     =(self.white, self.yellow)),
                directed=True,
            ),
        ]
        self.assertEqual(len(filtered_equations), len(expected_equations))
        for eq in filtered_equations:
            self.assertIn(eq, expected_equations)

        # case: all equations both sides
        player_pebbles_1 = PebbleCollection(
            pebbles
            =(
                self.red,
                self.green,
                self.green,
                self.blue,
                self.yellow,
                self.yellow,
                self.white,
            )
        )
        bank_pebbles_1 = PebbleCollection(
            pebbles
            =(
                self.red,
                self.green,
                self.green,
                self.blue,
                self.yellow,
                self.yellow,
                self.white,
            )
        )
        filtered_equations = self.equations.filter_equations(
            player_pebbles_1, bank_pebbles_1
        )

        expected_equations = [
            Equation(
                lhs=PebbleCollection(pebbles
                                     =(self.red, self.green)),
                rhs=PebbleCollection(pebbles
                                     =(self.blue, self.yellow)),
                directed=True,
            ),
            Equation(
                lhs=PebbleCollection(pebbles
                                     =(self.blue, self.yellow)),
                rhs=PebbleCollection(pebbles
                                     =(self.red, self.green)),
                directed=True,
            ),
            Equation(
                lhs=PebbleCollection(pebbles
                                     =(self.green, self.green)),
                rhs=PebbleCollection(pebbles
                                     =(self.white, self.yellow)),
                directed=True,
            ),
            Equation(
                lhs=PebbleCollection(pebbles
                                     =(self.white, self.yellow)),
                rhs=PebbleCollection(pebbles
                                     =(self.green, self.green)),
                directed=True,
            ),
            Equation(
                lhs=PebbleCollection(pebbles
                                     =(self.red, self.blue)),
                rhs=PebbleCollection(pebbles
                                     =(self.yellow, self.yellow)),
                directed=True,
            ),
            Equation(
                lhs=PebbleCollection(pebbles
                                     =(self.yellow, self.yellow)),
                rhs=PebbleCollection(pebbles
                                     =(self.red, self.blue)),
                directed=True,
            ),
        ]
        self.assertEqual(len(filtered_equations), len(expected_equations))
        for eq in filtered_equations:
            self.assertIn(eq, expected_equations)

    def test_filter_equations_with_insufficient_bank(self):
        """
        Tests the filtering of equations with various sets of available colors.
        Verifies that only usable equations are returned based on color availability.
        """
        # Create the equations set using PebbleCollection instances and Equation class with conset

        player_pebbles_1 = PebbleCollection(
            pebbles
            =(self.red, self.green, self.blue, self.yellow)
        )

        bank_pebbles_1 = PebbleCollection(
            pebbles
            =(self.red, self.blue, self.yellow)
        )

        # case: one equation both sides, but bank insuffcient
        filtered_equations = self.equations.filter_equations(
            player_pebbles_1, bank_pebbles_1
        )

        expected_equations = [
            Equation(
                lhs=PebbleCollection(pebbles
                                     =(self.red, self.green)),
                rhs=PebbleCollection(pebbles
                                     =(self.blue, self.yellow)),
                directed=True,
            ),
        ]

        self.assertEqual(len(filtered_equations), len(expected_equations))
        for eq in filtered_equations:
            self.assertIn(eq, expected_equations)
        bank_pebbles_1 = PebbleCollection(
            pebbles
            =(self.red, self.blue, self.yellow)
        )

        # case: one equation both sides, but bank insuffcient (reverse)
        bank_pebbles_1 = PebbleCollection(
            pebbles
            =(self.red, self.green, self.yellow)
        )
        filtered_equations = self.equations.filter_equations(
            player_pebbles_1, bank_pebbles_1
        )

        expected_equations = [
            Equation(
                lhs=PebbleCollection(pebbles
                                     =(self.blue, self.yellow)),
                rhs=PebbleCollection(pebbles
                                     =(self.red, self.green)),
                directed=True,
            ),
        ]

        self.assertEqual(len(filtered_equations), len(expected_equations))
        for eq in filtered_equations:
            self.assertIn(eq, expected_equations)

        # case: one equation both sides, but bank insuffcient for both side
        bank_pebbles_1 = PebbleCollection(pebbles
                                          =(self.red, self.yellow))
        filtered_equations = self.equations.filter_equations(
            player_pebbles_1, bank_pebbles_1
        )

        expected_equations = []

        self.assertEqual(len(filtered_equations), len(expected_equations))
        for eq in filtered_equations:
            self.assertIn(eq, expected_equations)


if __name__ == "__main__":
    unittest.main(argv=[""], exit=False)
