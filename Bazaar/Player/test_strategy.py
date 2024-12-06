import unittest

from Bazaar.Common.cards import Card
from Bazaar.Common.equations import Equation
from Bazaar.Common.pebble import *


class TestStrategy(unittest.TestCase):

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
