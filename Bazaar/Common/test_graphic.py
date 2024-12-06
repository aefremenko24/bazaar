import unittest


from Bazaar.Common.cards import Card, Cards
from Bazaar.Common.equations import Equation, Equations
from Bazaar.Common.pebble import Pebble, PebbleColor, PebbleCollection

from Bazaar.Common.vertical_board import SingleBoard

REDP = Pebble(color=PebbleColor.RED)
BLUEDP = Pebble(color=PebbleColor.BLUE)
GREENP = Pebble(color=PebbleColor.GREEN)
YELLOWP = Pebble(color=PebbleColor.YELLOW)

EQ = Equation(lhs=PebbleCollection(pebbles=(REDP, GREENP)), rhs=PebbleCollection(pebbles=(BLUEDP, YELLOWP)))
EQ1 = Equation(
    lhs=PebbleCollection(pebbles=(Pebble(color=PebbleColor.GREEN), Pebble(color=PebbleColor.GREEN))),
    rhs=PebbleCollection(pebbles=(Pebble(color=PebbleColor.WHITE), Pebble(color=PebbleColor.YELLOW)))
)
EQ2 = Equation(
    lhs=PebbleCollection(pebbles=tuple([
        Pebble(color=PebbleColor.GREEN),
        Pebble(color=PebbleColor.GREEN),
        Pebble(color=PebbleColor.GREEN),
        Pebble(color=PebbleColor.GREEN),
    ])),
    rhs=PebbleCollection(pebbles=tuple([
        Pebble(color=PebbleColor.WHITE),
        Pebble(color=PebbleColor.YELLOW),
        Pebble(color=PebbleColor.WHITE),
        Pebble(color=PebbleColor.YELLOW),
    ])),
)
EQUATIONS = Equations(equations=[EQ, EQ1, EQ2])
CARD = Card(pebbles=PebbleCollection(pebbles=(REDP, REDP, REDP, BLUEDP, BLUEDP)), happy_face=False)
CARDSMILE = Card(pebbles=PebbleCollection(pebbles=(REDP, GREENP, REDP, BLUEDP, BLUEDP)), happy_face=True)
CARDSMILE2 = Card(pebbles=PebbleCollection(pebbles=(REDP, REDP, REDP, BLUEDP, BLUEDP)), happy_face=True)
CARDSMILE3 = Card(pebbles=PebbleCollection(pebbles=(REDP, YELLOWP, GREENP, YELLOWP, BLUEDP)), happy_face=True)
TWOCARDS = Cards(cards=[CARD, CARDSMILE])
THREECARDS = Cards(cards=[CARD, CARDSMILE, CARDSMILE2])
FOURCARDS = Cards(cards=[CARD, CARDSMILE, CARDSMILE2, CARDSMILE3])
BOARD = SingleBoard()


class GraphicTest(unittest.TestCase):
    """
    Testing graphics with Tkinter.
    """

    def testDrawEquation(self):
        BOARD.create_canvas()
        EQ.draw(BOARD)
        BOARD.show()
        print(EQ.serialize)

    def testDrawEquations(self):
        BOARD.create_canvas()
        EQUATIONS.draw(BOARD)
        BOARD.show()

    def testCard(self):
        BOARD.create_canvas()
        CARD.draw(BOARD)
        BOARD.show()

    def testCardWithSmile(self):
        BOARD.create_canvas()
        CARDSMILE.draw(BOARD)
        BOARD.show()

    def testDrawCard(self):
        CARD.draw(BOARD)
        BOARD.create_canvas()
        THREECARDS.draw(BOARD)
        BOARD.show()

    def testDrawCardandEquations(self):
        CARD.draw(BOARD)
        BOARD.create_canvas()
        THREECARDS.draw(BOARD)
        EQUATIONS.draw(BOARD)
        BOARD.show()


"""gameBoardTest"""
