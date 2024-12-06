import unittest

from Bazaar.Common.vertical_board import SingleBoard
from Bazaar.Player.mechanism import Mechanism
from Bazaar.Referee.observer import Observer
from Bazaar.Referee.referee import Referee


class TestObserver(unittest.TestCase):
    def setUp(self):
        self.observerNoShow = Observer(show=False)
        self.observerDoShow = Observer(show=True)
        self.referee = Referee()
        self.player1 = Mechanism(name="Mandy", policy="purchase-size")
        self.player2 = Mechanism(name="Richard", policy="purchase-points")
        self.players = [self.player1, self.player2]

    def testObserverNoShow(self):
        self.referee.register_observer(self.observerNoShow)
        self.referee.execute_game(self.players)

    def testObserverDoShow(self):
        self.referee.register_observer(self.observerDoShow)
        self.referee.execute_game(self.players)