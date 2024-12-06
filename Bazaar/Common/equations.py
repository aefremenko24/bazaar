import json
import random

from collections import Counter
from pydantic import BaseModel, model_validator, conlist, conset
from typing import List, Dict, Tuple

from Bazaar.Common.data import MIN_EQUATION_SIZE, MAX_EQUATION_SIZE
from Bazaar.Common.pebble import Pebble, PebbleColor, PebbleCollection
from copy import copy


class Equation(BaseModel):
    """Represents an equation that can be used to trade pebbles."""

    lhs: PebbleCollection
    rhs: PebbleCollection
    directed: bool = False

    model_config = {
        "frozen": True  # This prevents any modification of the attributes after initialization
    }

    @model_validator(mode="before")
    def pre_validation(cls, values):
        return cls.validate_equation(values)

    @classmethod
    def validate_equation(cls, v):
        """
        NOTE:it is made a classmethod to match the context in which it's used, specifically within model_validator when doing pre-validation at the class level.
        It is used to perform validation before an instance is created. It is essentially a class-level operation where the code don't have an instance (self) available yet.
        Ensure lhs and rhs are valid PebbleCollections, validate their lengths, and check for unique colors on both sides.
        """

        lhs = v.get("lhs")
        rhs = v.get("rhs")

        cls._validate_pebble_collection_instance(lhs, rhs)
        cls._validate_length(lhs)
        cls._validate_length(rhs)
        cls._validate_unique_colors(lhs, rhs)

        return v

    @staticmethod
    def _validate_pebble_collection_instance(lhs, rhs):
        if not isinstance(lhs, PebbleCollection) or not isinstance(
            rhs, PebbleCollection
        ):
            raise TypeError("lhs and rhs must be instances of PebbleCollection")

    @staticmethod
    def _validate_length(collection: PebbleCollection):
        length = len(collection.pebbles)
        if not MIN_EQUATION_SIZE <= length <= MAX_EQUATION_SIZE:
            raise ValueError(
                f"each side of PebbleCollection must have between {MIN_EQUATION_SIZE} and "
                f"{MAX_EQUATION_SIZE} pebbles."
            )

    @staticmethod
    def _validate_unique_colors(lhs: PebbleCollection, rhs: PebbleCollection):
        lhs_colors = {pebble.color for pebble in lhs.pebbles}
        rhs_colors = {pebble.color for pebble in rhs.pebbles}
        if lhs_colors & rhs_colors:
            raise ValueError(
                "Each side of the equation must have different colored pebbles."
            )

    @classmethod
    def generate_random(cls):
        all_pebbles = [Pebble(color=PebbleColor(color)) for color in PebbleColor]

        lhs_size = random.randint(MIN_EQUATION_SIZE, MAX_EQUATION_SIZE)
        lhs = tuple(random.choice(all_pebbles) for _ in range(lhs_size))
        lhs_colors = {pebble.color for pebble in lhs}

        available_pebbles_for_rhs = tuple(
            pebble for pebble in all_pebbles if pebble.color not in lhs_colors
        )
        rhs_size = random.randint(MIN_EQUATION_SIZE, MAX_EQUATION_SIZE)
        rhs = tuple(random.choice(available_pebbles_for_rhs) for _ in range(rhs_size))

        return cls(
            lhs=PebbleCollection(pebbles=lhs),
            rhs=PebbleCollection(pebbles=rhs),
            directed=False,
        )

    def trade_equation(
        self, player_pebbles: PebbleCollection, bank: PebbleCollection
    ) -> Tuple[PebbleCollection, PebbleCollection]:
        """
        Executes a trade of the equation by removing the pebbles from the LHS and adding colors from the
        RHS to/from the player wallet, but only if the trade is possible (i.e., the player has enough pebbles for the trade).


        :param player_pebbles: PebbleCollection representing player's pebbles before the trade.
        :param bank: PebbleCollection representing bank's pebbles before the trade.
        :returns: Tuple containing two PebbleCollection: updated player pebbles and updated bank pebbles after the trade.
        :rtype: Tuple[PebbleCollection, PebbleCollection]
        """
        player_pebbles_copy = PebbleCollection(pebbles=tuple(player_pebbles.pebbles))
        bank_copy = PebbleCollection(pebbles=tuple(bank.pebbles))
        if self.directed:
            player_pebbles_copy -= self.lhs
            player_pebbles_copy += self.rhs
            bank_copy -= self.rhs
            bank_copy += self.lhs
        return (player_pebbles_copy, bank_copy)

    def to_list(self) -> List[List[str]]:
        """
        Converts the equation to a list of two lists. First list represents left side and second equation represents right side.

        :returns: A list of two lists of strings each containing serializations of pebbles on each side.
        :rtype: List[List[str]]
        """
        return [
            [pebble.serialize() for pebble in self.lhs.pebbles],
            [pebble.serialize() for pebble in self.rhs.pebbles],
        ]

    @staticmethod
    def validate_deserialize_data(data: list) -> bool:
        """
        Validates that the dictionary used to deserialize this object is valid

        :param data: Equation data stored as a list of the shape [*Pebbles, *Pebbles], each item indicating an equation side
        :type data: list
        :return: True if data is valid, False otherwise
        """
        try:
            assert len(data) == 2
            for side in data:
                assert PebbleCollection.validate_deserialize_data(side)
            return True
        except AssertionError:
            return False

    @classmethod
    def deserialize(cls, data: list, directed: bool = False):
        """
        Deserializes the Equation object from a list

        :param data: Equation data stored as a list of the shape [*Pebbles, *Pebbles], each item indicating an equation side
        :type data: list
        :param directed: True if the equation is directed (Rule), False otherwise
        :type directed: bool
        :return: Equation object deserialized from the list
        :rtype: Equation
        """
        if not Equation.validate_deserialize_data(data):
            raise Exception("Invalid Equation data provided.")
        lhs = PebbleCollection.deserialize(data[0])
        rhs = PebbleCollection.deserialize(data[1])
        try:
            return Equation(lhs=lhs, rhs=rhs, directed=directed)
        except:
            raise Exception("Invalid Equation data provided.")

    def serialize(self) -> list:
        """
        Converts this Equation to a list representation of the shape [*Pebbles, *Pebbles], each item indicating an equation side.

        :returns: a list representation of the equation
        :rtype: list
        """
        return [
            PebbleCollection.serialize(self.lhs),
            PebbleCollection.serialize(self.rhs),
        ]

    def __str__(self):
        """
        Converts this Equation to a string representation.

        :returns: a string representation of the Equation instance.
        :rtype: str
        """
        return f"Equation: {' '.join(str(pebble) for pebble in self.lhs.pebbles)} = {' '.join(str(pebble) for pebble in self.rhs.pebbles)}"

    def __eq__(self, other):
        """Checks if two equations are equal. Equations can go in both directions."""
        if not isinstance(other, Equation):
            return False
        if self.directed and other.directed:
            return self.lhs == other.lhs and self.rhs == other.rhs
        else:
            return (self.lhs == other.lhs and self.rhs == other.rhs) or (
                self.lhs == other.rhs and self.rhs == other.lhs
            )

    def __hash__(self):
        """Hashing an equation."""
        # Convert lhs and rhs to frozenset to ignore order
        lhs_set = frozenset(self.lhs.pebbles)
        rhs_set = frozenset(self.rhs.pebbles)

        # Hash both sides and sort the results to ensure consistency in order
        sides = (lhs_set, rhs_set)
        return hash(tuple(sorted(sides, key=lambda x: hash(x))))

    def __lt__(self, other):
        """
        Overrides the less than comparison function for the Equation class.
        Here, equation self is less than other equation if the pebbles on the left-hand side
        of self (as a wallet) are less than the pebbles on the left-hand side of other, or if the
        pebbles on the right hand side of self are less than those of other, assuming left sides are equal.

        :param other: other Equation to compare to.
        :type other: Equation
        :return: True if this equation is less than other, False otherwise.
        :rtype: bool
        """
        if not isinstance(other, Equation):
            raise TypeError("Other Equation must be of type Equation.")
        if self.lhs == other.lhs:
            return self.rhs < other.rhs
        return self.lhs < other.lhs



class Equations(BaseModel):
    """Represents a collection of Equation."""

    equations: conlist(Equation, min_length=0, max_length=10)

    @classmethod
    def generate_random(cls, count):
        """
        Generates equations randomly.
        :param count: Number of equations to generate.
        :return: Returns new Equations.
        """
        equations = []
        while len(equations) < count:
            equation = Equation.generate_random()
            while equation in equations:
                equation = Equation.generate_random()
            equations.append(equation)
        return cls(equations=equations)

    def filter_equations(
        self, player_pebbles: PebbleCollection, bank: PebbleCollection
    ) -> List[Equation]:
        """
        Returns the subset of the equations where they can be used to trade given the pebbles you have.

        :param player_pebbles: the pebbles you have.
        :param bank: the pebbles the bank has.
        :return: Equations that can be used to trade.
        """
        from Bazaar.Common.rule_book import RuleBook

        usable_directed_equations = []
        for equation in self.equations:
            usable_trades = RuleBook.tradable_equation(equation, player_pebbles, bank)
            usable_directed_equations += usable_trades
        return usable_directed_equations

    @staticmethod
    def validate_deserialize_data(data: list) -> bool:
        """
        Validates that every element in the list used to deserialize this object is a valid Equation list

        :param data: Equations data stored as a list of Equation data elements
        :type data: list
        :return: True if each element in the list is a proper Equation data, False otherwise
        """
        try:
            assert all(
                [Equation.validate_deserialize_data(element) for element in data]
            )
            return True
        except AssertionError:
            return False

    @classmethod
    def deserialize(cls, data: list, directed: bool = False):
        """
        Deserializes the Equations list data into an Equations object.

        :param data: Equations data stored as a list
        :type data: list
        :param directed: True if equations are directed (Rules), False otherwise
        :type directed: bool
        :return: Equation objects stored as an Equations object
        :rtype: Equations
        """
        if not Equations.validate_deserialize_data(data):
            raise Exception("Invalid Equations data provided.")
        list_of_equations = [
            Equation.deserialize(equation_data, directed) for equation_data in data
        ]
        try:
            return cls(equations=list_of_equations)
        except:
            raise Exception("Invalid Equations data provided.")

    def serialize(self) -> list:
        """
        Serializes the Equations data into a list of Equation objects.

        :return: Equations data stored as a list
        :rtype: list
        """
        return [equation.serialize() for equation in self.equations]