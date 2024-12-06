import json
from enum import Enum
from typing import Literal, List, runtime_checkable, Optional
from collections import Counter
import random
from typing import Tuple
from pydantic import BaseModel, conlist
from copy import copy

__PEBBLE_ORDER__ = ["red", "white", "blue", "green", "yellow"]


class PebbleColor(str, Enum):
    """
    Pebble color choices.
    """

    RED = "red"
    WHITE = "white"
    BLUE = "blue"
    GREEN = "green"
    YELLOW = "yellow"

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, PebbleColor):
            return self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def __lt__(self, other):
        if self == other:
            return False
        for elem in PebbleColor:
            if self == elem:
                return True
            elif other == elem:
                return False
        raise RuntimeError("This should never happen")

    def __le__(self, other):
        if self == other:
            return True
        return self < other

    def __gt__(self, other):
        return not (self < other)

    def __ge__(self, other):
        if self == other:
            return True
        return not (self < other)


class Pebble(BaseModel):
    """
    A single pebble.
    """

    color: PebbleColor

    class Config:
        use_enum_values = True

    def serialize(self):
        """
        Serialize the Pebble object to just the color string.
        """
        return self.color

    def draw(self, canvas, x, y):
        """Draws a pebble on the canvas at the specified (x, y) coordinates."""
        canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill=self.color.value)

    def __str__(self):
        """return first letter of its color"""
        return str(self.color)

    def __eq__(self, other):
        """
        Checks if two pebbles are equal by comparing their colors.

        :param other: Another Pebble object.
        :return: True if both pebbles have the same color, False otherwise.
        """
        return isinstance(other, Pebble) and self.color == other.color

    def __hash__(self):
        """
        Returns a hash of the pebble based on its color, making it usable in sets and as dict keys.

        :return: Hash of the Pebble object.
        """
        return hash(self.color)

    def __lt__(self, other) -> bool:
        """
        Overrides the default implementation of less than comparison between two Pebble instances.

        :param other: other instance of the Pebble class.
        :returns: True if the color of this Pebble is alphabetically smaller than other, False otherwise.
        :rtype: bool
        """
        if self == other:
            return False
        for elem in __PEBBLE_ORDER__:
            if self.color == elem:
                return True
            elif other.color == elem:
                return False
        raise RuntimeError("This should never happen")

    @staticmethod
    def get_rgb(color) -> Tuple[int, int, int]:
        """
        Returns an RGB tuple corresponding to this pebble.

        :return: tuple of (RED, GREEN, BLUE)
        :rtype: Tuple[int, int, int]
        """
        mapping = {
            "red": (255, 0, 0),
            "white": (255, 255, 255),
            "blue": (0, 0, 255),
            "green": (0, 255, 0),
            "yellow": (255, 255, 0),
        }
        return mapping[color]

class PebbleCollection(BaseModel):
    pebbles: tuple = tuple()

    def __add__(self, other):
        """
        Overrides the add function of the PebbleCollection class.

        :param other: other instance of PebbleCollection to be added to this instance
        :type other: PebbleCollection
        :returns: new instance of PebbleCollection with other Pebble instances added to this
        :rtype: PebbleCollection
        :raises: TypeError if other is not an instance of PebbleCollection
        """
        if isinstance(other, PebbleCollection):
            this_list_of_pebbles = list(copy(self.pebbles))
            other_list_of_pebbles = list(other.pebbles)
            return PebbleCollection(pebbles=(tuple(this_list_of_pebbles + other_list_of_pebbles)))
        else:
            raise TypeError("The second argument is not of type PebbleCollection")

    def __sub__(self, other):
        """
        Overrides the subtract function of the PebbleCollection class.

        :param other: other instance of PebbleCollection to be subtracted from this instance
        :type other: PebbleCollection
        :returns: new instance of PebbleCollection with other Pebble instances subtracted from this,
        or this PebbleCollection if there are not enough pebbles to subtract.
        :rtype: PebbleCollection
        :raises: TypeError if other is not an instance of PebbleCollection
        """
        if not isinstance(other, PebbleCollection):
            raise TypeError("The second argument is not of type PebbleCollection")

        new_list_of_pebbles = list(copy(self.pebbles))
        for pebble in other.pebbles:
            if pebble not in new_list_of_pebbles:
                return PebbleCollection(pebbles=self.pebbles)
            else:
                new_list_of_pebbles.remove(pebble)

        return PebbleCollection(pebbles=tuple(new_list_of_pebbles))

    def __eq__(self, other):
        """Overrides the equal function of the PebbleCollection class.

        :param other: other instance of PebbleCollection to be compared to this instance
        :type other: PebbleCollection
        :returns: True if this PebbleCollection contains the same pebbles as the other one (disregard the order),
        False otherwise
        :rtype: bool
        """
        return Counter(self.pebbles) == Counter(other.pebbles)

    def __hash__(self):
        """
        Overrides the hash function of the PebbleCollection class.

        :returns: Hash of the Pebble collection.
        """
        return hash(self.pebbles)

    def __list_str__(self):
        """covert the list_of_pebble to a list of sorted string representation of pebble in lexicographical order.
        A string representation of pebble is the first letter of pebble color"""

        return sorted([str(pebble) for pebble in self.pebbles])

    def __lt__(self, other) -> bool:
        """
        Overrides the default implementation of less than comparison between two pebble collections.
        The comparison first check the size of pebbles, then compare the string representation of pebbles
        lexicographically if the size are the same.

        :param other: other instance of the PebbleCollection class.
        :returns: True if this PebbleCollection is smaller than other pebble collection, False otherwise.
        :rtype: bool
        """
        if not isinstance(other, PebbleCollection):
            raise TypeError("The second argument is not of type PebbleCollection")
        if len(self.pebbles) == len(other.pebbles):
            return self.__list_str__() < other.__list_str__()

        return len(self.pebbles) < len(other.pebbles)

    def subset_of(self, other) -> bool:
        """
        Checks if this PebbleCollection is subset of another PebbleCollection.
        NOTE: using counter to take account of the number of same color

        :param other: other instance of PebbleCollection to be subset of
        :type other: PebbleCollection
        :returns: True if this PebbleCollection is subset of other PebbleCollection, False otherwise
        :rtype: bool
        """
        self_counter = Counter(self.pebbles)
        other_counter = Counter(other.pebbles)
        for pebble, count in self_counter.items():
            if other_counter[pebble] < count:
                return False

        return True

    @staticmethod
    def validate_deserialize_data(data: list) -> bool:
        """
        Validates the list used to deserialize the PebbleCollection object.

        :param data: PebbleCollection data stored as a list, where each element is one of "red", "white", "blue", "green", "yellow"
        :type data: list
        :return: True if each element in the list is one of "red", "white", "blue", "green", "yellow", False otherwise
        """
        all_colors = [color.value for color in PebbleColor]
        try:
            assert all([pebble in all_colors for pebble in data])
            return True
        except AssertionError:
            return False

    @classmethod
    def deserialize(cls, data: list):
        """
        Deserializes the pebble list data into a PebbleCollection object.

        :param data: pebbles data stored as a list
        :type data: list
        :return: pebbles stored as a PebbleCollection object
        :rtype: PebbleCollection
        """
        if not PebbleCollection.validate_deserialize_data(data):
            raise Exception("Invalid PebbleCollection data provided.")
        pebbles = (Pebble(color=PebbleColor(color)) for color in data)
        newPebbleColllection = cls(pebbles=pebbles)
        return newPebbleColllection

    def serialize(self) -> list:
        """
        Serializes the PebbleCollection data into a list.

        :return: pebbles data stored as a list
        :rtype: list
        """
        return [pebble.serialize() for pebble in self.pebbles]

    def draw_pebble(self) -> Optional[Pebble]:
        """
        Draws a pebble from this pebble collection in a deterministic manner.
        Specifically, iterates through the sequence of colors in order (red, white, blue, green, yellow) and,
        if a pebble of that color is available, picks it.

        :return: A pebble from this pebble collection, None if no more pebbles are available to draw.
        :rtype: Optional[Pebble]
        """
        if not self.pebbles:
            return None
        sorted_pebbles = sorted(self.pebbles)
        pebble = sorted_pebbles[0]
        self.pebbles = tuple(sorted_pebbles[1:])
        return pebble

    def add_pebble(self, pebble: Pebble):
        """
        Adds a pebble to this collection.

        :param pebble: pebble to be added to this collection
        :type pebble: Pebble
        """
        if not pebble or not isinstance(pebble, Pebble):
            raise TypeError("Pebble must be of type Pebble")
        self.pebbles = self.pebbles + tuple([pebble])

    @classmethod
    def generate_random(cls, size: int):
        """
        Generates a random PebbleCollection object with a specified number of random pebbles.

        :param size: number of pebbles to add to the collection.
        :type size: int
        :return: PebbleCollection object with random pebbles.
        :rtype: PebbleCollection
        """
        all_pebbles = [Pebble(color=color) for color in PebbleColor]
        pebbles=tuple(random.choices(all_pebbles, k=size))
        return cls(pebbles=pebbles)


def list_of_all_pebbles() -> PebbleCollection:
    """
    Returns a PebbleCollection of Pebble instances of all available colors.

    :returns: PebbleCollection containing Pebble instances of all available colors.
    :rtype: PebbleCollection
    """
    return PebbleCollection(pebbles=[Pebble(color=color) for color in PebbleColor])


def init_bank() -> PebbleCollection:
    """
    Generates a PebbleCollection representing the state of the bank at the beginning of the game, with 20 pebbles of each color.

    :return: PebbleCollection of size 100 representing the state of the bank at the beginning of the game.
    :rtype: PebbleCollection
    """
    all_pebbles = []
    for color in PebbleColor:
        all_pebbles += [Pebble(color=color) for _ in range(20)]
    return PebbleCollection(pebbles=tuple(all_pebbles))
