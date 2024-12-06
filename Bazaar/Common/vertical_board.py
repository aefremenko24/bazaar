import sys
import math
from collections import Counter

import ijson
from typing import List, Optional, Dict
import os

import pydantic
from PIL import Image, ImageDraw as image_draw
from PIL.ImageDraw import ImageDraw
import tkinter as tk
from io import StringIO

from pydantic import BaseModel, ConfigDict, SkipValidation, Field

from Bazaar.Common.equations import Equation, Equations
from Bazaar.Common.pebble import PebbleCollection, Pebble
from game_interface import Board


# Tkinter GUI for drawing
class SingleBoard(Board):
    CANVAS_WIDTH: int = 600
    CANVAS_HEIGHT: int = 8000
    current_y: int = 20  # Keeps track of where to draw the next object
    PADDING: int = 50
    root: tk.Tk = None
    canvas: tk.Canvas = None
    image: Image = None
    image_draw: ImageDraw = None

    def __init__(self, **data):
        super().__init__(**data)
        self.image = Image.new("RGB", (self.CANVAS_WIDTH, self.CANVAS_HEIGHT), "white")
        self.image_draw = image_draw.Draw(self.image)

    def _update_scroll_region(self):
        """Update the scroll region based on the current Y position"""
        if self.current_y > self.CANVAS_HEIGHT:
            self.canvas.config(scrollregion=(0, 0, self.CANVAS_WIDTH, self.current_y))

    def draw_pebble(self, color: str, x: int, y: int, radius: int = 20):
        """Draw a single pebble (circle) with a black outline"""
        if self.canvas:
            self.canvas.create_oval(
                x - radius,
                y - radius,
                x + radius,
                y + radius,
                fill=color,
                outline="black",
                width=2,
            )
        if self.image_draw:
            self.image_draw.ellipse(
                [x - radius, y - radius, x + radius, y + radius],
                outline="black",
                fill=Pebble.get_rgb(color),
            )

    def draw_equation(self, equation: Equation):
        """Draw an equation with pebbles on each side connected by an equals sign"""
        x = self.PADDING
        gap = 50
        for color in equation.lhs.pebbles:
            self.draw_pebble(color, x, self.current_y)
            x += gap

        if self.canvas:
            self.canvas.create_text(x, self.current_y, text="=", font=("Arial", 24))
        if self.image_draw:
            self.image_draw.text((x, self.current_y - 12), "=", fill="black")

        x += gap

        for color in equation.rhs.pebbles:
            self.draw_pebble(color, x, self.current_y)
            x += gap

        self.current_y += gap  # Move down after drawing the equation
        self._update_scroll_region()  # Make it scrollable if needed

    def draw_equations(self, equations: Equations):
        """
        Renders equations provided on this board.

        :param equations: Equations object to be rendered
        :type equations: Equations
        """
        for equation in equations.equations:
            self.draw_equation(equation)

    def draw_card(self, pebbles: List[str], happy_face: bool = False):
        """Draw a card with a rectangle and 5 pebbles arranged in a circle"""
        x_start, x_end = self.PADDING, 350
        y_start = self.current_y
        y_end = y_start + 400

        # Draw card rectangle
        if self.canvas:
            self.canvas.create_rectangle(
                x_start, y_start, x_end, y_end, outline="black", width=2
            )
        if self.image_draw:
            self.image_draw.rectangle([x_start, y_start, x_end, y_end], outline="black")

        center_x = (x_start + x_end) // 2
        center_y = (y_start + y_end) // 2
        radius = 100

        # Arrange 5 pebbles in a circular manner
        angle_step = 2 * math.pi / 5  # 360 degrees / 5 pebbles
        for i, color in enumerate(pebbles):
            angle = i * angle_step
            pebble_x = center_x + radius * math.cos(angle)  # X position on the circle
            pebble_y = center_y + radius * math.sin(angle)  # Y position on the circle
            self.draw_pebble(color, pebble_x, pebble_y)

        if happy_face:
            self.canvas.create_text(center_x, center_y, text="😊", font=("Arial", 40))

        self.current_y += 420
        self._update_scroll_region()

    def draw_bank(self, bank: PebbleCollection):
        """Draws the bank of colored pebbles along with their counts."""
        self._draw_pebble_dic(50, bank)
        self._update_scroll_region()

    def _draw_pebble_dic(self, x, bank: PebbleCollection):

        y = self.current_y

        for pebble, count in Counter(bank.pebbles).items():
            # Draw the colored pebble
            self.draw_pebble(pebble.color, x, y)

            # Display the count next to the pebble
            if self.canvas:
                self.canvas.create_text(
                    x + 40, y, text=f"{count}", font=("Arial", 16), anchor="w"
                )
            if self.image_draw:
                self.image_draw.text((x + 40, y - 10), str(count), fill="black")

            # Move down to draw the next pebble and count
            y += 50

        self.current_y = y + 20  # Update current_y for subsequent components

    def draw_playerstate(
        self,
        player_id: int,
        wallet: PebbleCollection,
        score: int,
        reachability: Optional[str] = None,
    ):
        """Draws the player's state on the board."""
        x = self.PADDING
        y = self.current_y

        # Draw player ID
        if self.canvas:
            self.canvas.create_text(
                x, y, text=f"Player ID: {player_id}", font=("Arial", 16), anchor="w"
            )
        if self.image_draw:
            self.image_draw.text((x, y - 10), f"Player ID: {player_id}", fill="black")

        y += 30
        self.current_y = y

        # Draw player's wallet
        if self.canvas:
            self.canvas.create_text(
                x, y, text="Wallet:", font=("Arial", 16), anchor="w"
            )
        if self.image_draw:
            self.image_draw.text((x, y - 10), "Wallet:", fill="black")
        self.current_y = y + 30
        self._draw_pebble_dic(x + x / 2, wallet)

        # Draw player score
        y = self.current_y
        if self.canvas:
            self.canvas.create_text(
                x, y, text=f"Score: {score}", font=("Arial", 16), anchor="w"
            )
        if self.image_draw:
            self.image_draw.text((x, y - 10), f"Score: {score}", fill="black")

        y += 30

        # Draw reachability, if available
        if reachability:
            if self.canvas:
                self.canvas.create_text(
                    x,
                    y,
                    text=f"Reachability: {reachability}",
                    font=("Arial", 16),
                    anchor="w",
                )
            if self.image_draw:
                self.image_draw.text(
                    (x, y - 10), f"Reachability: {reachability}", fill="black"
                )

        # Update the board's current_y for the next component
        self.current_y = y + 50
        self._update_scroll_region()

    def draw_score(self, scores: List[int]):
        """Draws a list of scores in a line with text "Scores: " at the very top of the canvas."""
        x = self.PADDING  # Starting x coordinate
        y = self.current_y
        x_gap = 50

        # Draw the label "Scores: "
        if self.canvas:
            self.canvas.create_text(
                x, y, text="Scores: ", font=("Arial", 16), anchor="w"
            )
            x += x_gap * 2  # Move x to the right after drawing "Scores: "

        if self.image_draw:
            self.image_draw.text((x, y - 10), "Scores: ", fill="black")
            x += x_gap

        # Draw each score with a small space in between
        for score in scores:
            if self.canvas:
                self.canvas.create_text(
                    x, y, text=str(score), font=("Arial", 16), anchor="w"
                )
            if self.image_draw:
                self.image_draw.text((x, y - 10), str(score), fill="black")
            x += x_gap  # Move x to the right for the next score

        self.current_y = max(self.current_y, y + 30)  # Update current_y if needed
        self._update_scroll_region()

    def save_image(self, directory: str = "Tmp", name: str = "the-image"):
        if '.' in name:
            name = name.split('.')[0]
        try:
            self.check_directory(directory)
            self.image.save(f"{directory}/{name}.png", "PNG")
        except Exception as e:
            print(f"Error saving image {name}: {e}")

    def check_directory(self, directory: str = "/Tmp"):
        """
        Checks if the given directory exists. If not, creates it.

        :param directory: The directory to check.
        :type directory: str
        """
        if not directory[0] == '/':
            directory = '/' + directory
        launch_directory = os.getcwd()
        if not os.path.isdir(launch_directory + directory):
            os.mkdir(launch_directory + directory)

    def create_canvas(self):
        self.root = tk.Tk()
        self.root.title("Cards and Equations Window")

        self.canvas = tk.Canvas(
            self.root, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT
        )
        scrollbar = tk.Scrollbar(
            self.root, orient="vertical", command=self.canvas.yview
        )
        self.canvas.config(yscrollcommand=scrollbar.set)

        # Pack the canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Configure scroll region
        self.canvas.config(scrollregion=(0, 0, self.CANVAS_WIDTH, self.CANVAS_HEIGHT))

    def show(self):
        """Start the Tkinter main loop."""
        self.root.mainloop()

    def show_input(self, input_string=None):
        if input_string:
            # If an input string is provided, convert it to a stream
            input_stream = StringIO(input_string)
        else:
            # Otherwise, default to using stdin
            input_stream = sys.stdin
        self.process_input(input_stream)
        self.root.mainloop()

    def process_input(self, input_stream):
        """Reads JSON objects from the given input stream and processes them."""
        for obj in ijson.items(input_stream, "", multiple_values=True):
            if isinstance(obj, list) and len(obj) > 0 and isinstance(obj[0], list):
                # This means we have an array of equations in the new format
                for equation in obj:
                    if len(equation) == 2:
                        rhs, lhs = equation
                        self.draw_equation(lhs, rhs)
            elif "pebbles" in obj:
                self.draw_card(obj["pebbles"], obj.get("happy_face", False))

    def clear_canvas(self):
        """
        Clears everything that is currently on the canvas.
        """
        self.current_y = 20
        self.canvas.delete("all")
        self.image_draw.rectangle((0, 0, self.CANVAS_WIDTH, self.CANVAS_HEIGHT), fill=(255, 255, 255))


if __name__ == "__main__":
    board = SingleBoard()

    # You can either show the interactive window or save the image
    if "--show" in sys.argv:
        board.show()
    else:
        board.save_image()
