# Base class for all drawable components
from typing import List, Dict, Optional

from pydantic import BaseModel

from Bazaar.Common.equations import Equation
from Bazaar.Common.pebble import PebbleCollection


class DrawableComponent:
    def draw(self, board: "Board"):
        """Draw the component on the board. To be implemented by subclasses."""
        raise NotImplementedError


class Board:
    """Interface for Board implementations."""

    def draw_pebble(self, color: str, x: int, y: int, radius: int = 20):
        """Draw a single pebble (circle) with a black outline."""
        raise NotImplementedError("This method should be overridden.")

    def draw_card(self, pebbles: List[str], happy_face: bool = False):
        raise NotImplementedError("This method should be overridden.")

    def draw_equation(self, equation: Equation):
        """Draw an equation with pebbles on each side connected by an equals sign."""
        raise NotImplementedError("This method should be overridden.")

    def draw_bank(self, bank: PebbleCollection):
        """Draw bank with each pebble followed by the count in a line"""
        raise NotImplementedError("This method should be overridden.")

    def draw_playerstate(
        self,
        player_id: int,
        wallet: PebbleCollection,
        score: int,
    ):
        raise NotImplementedError("This method should be overridden.")

    def show(self):
        """Display the board."""
        raise NotImplementedError("This method should be overridden.")

    def show_input(self, input_stream):
        """Reads JSON objects from the given input stream and processes them,then display the board."""
        raise NotImplementedError("This method should be overridden.")
