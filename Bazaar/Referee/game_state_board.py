import math
import sys
import tkinter as tk
from io import StringIO
from typing import List, Dict, Optional
from PIL import Image, ImageDraw
from Bazaar.Common.game_interface import Board


class GameStateBoard(Board):
    CANVAS_WIDTH: int = 1000
    CANVAS_HEIGHT: int = 1200
    RADIUS = 10

    def __init__(self):
        self.root = None
        self.top_frame = None
        self.middle_frame = None
        self.bottom_frame = None
        self.bank_canvas = None
        self.cards_canvas = None
        self.player_state_canvas = None
        self.current_x = 50

    def create_canvas(self):
        self.root = tk.Tk()
        self.root.title("referee game state Board Window")

        # Define frames to separate the sections
        self.top_frame = tk.Frame(
            self.root,
            width=self.CANVAS_WIDTH,
            height=self.CANVAS_HEIGHT // 2,
            bd=1,
            relief="solid",
        )
        self.bottom_frame = tk.Frame(
            self.root,
            width=self.CANVAS_WIDTH,
            height=self.CANVAS_HEIGHT // 2,
            bd=1,
            relief="solid",
        )

        # Pack frames with appropriate positioning
        self.top_frame.pack(side="top", fill="both", expand=True)
        self.bottom_frame.pack(side="bottom", fill="both", expand=True)

        # Create separate canvases for bank and cards in the top frame
        self.bank_canvas = tk.Canvas(
            self.top_frame,
            width=self.CANVAS_WIDTH // 2,
            height=self.CANVAS_HEIGHT // 4,
            bd=1,
            relief="solid",
        )
        self.cards_canvas = tk.Canvas(
            self.top_frame,
            width=self.CANVAS_WIDTH,
            height=self.CANVAS_HEIGHT // 4,
            bd=1,
            relief="solid",
        )

        # Create a canvas for player state in the bottom frame
        self.player_state_canvas = tk.Canvas(
            self.bottom_frame, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT // 2
        )

        # Place canvases into frames
        self.bank_canvas.pack(side="right", fill="both", expand=True)
        self.cards_canvas.pack(side="left", fill="both", expand=True)
        self.player_state_canvas.pack(side="bottom", fill="both", expand=True)

    def show(self):
        """Start the Tkinter main loop."""
        self.root.mainloop()

    def draw_pebble(self, color: str, x: int, y: int, radius: int = 20):
        """Draw a single pebble (circle) with a black outline"""
        pass

    def draw_bank(self, bank: Dict[str, int]):
        """Draws the bank on the bank canvas."""
        x, y = 10, 30
        gap = 40
        self.bank_canvas.create_text(
            x, y, text=f"Bank:", font=("Arial", 25), anchor="w"
        )
        y += gap
        for color, count in bank.items():
            self.bank_canvas.create_oval(
                x,
                y,
                x + self.RADIUS,
                y + self.RADIUS,
                fill=color,
                outline="black",
                width=2,
            )
            self.bank_canvas.create_text(
                x + 30, y + 10, text=str(count), anchor="w", font=("Arial", 16)
            )
            y += gap

    def draw_card(self, pebbles: List[str], happy_face: bool = False):
        """Draw a card with a rectangle and 5 pebbles arranged in a circle"""
        y_start, y_end = 50, 250
        x_start = self.current_x
        x_end = x_start + 150

        # Draw card rectangle
        self.cards_canvas.create_rectangle(
            x_start, y_start, x_end, y_end, outline="black", width=2
        )

        center_x = (x_start + x_end) // 2
        center_y = (y_start + y_end) // 2
        radius = 50

        # Arrange 5 pebbles in a circular manner
        angle_step = 2 * math.pi / 5  # 360 degrees / 5 pebbles
        for i, color in enumerate(pebbles):
            angle = i * angle_step
            pebble_x = center_x + radius * math.cos(angle)  # X position on the circle
            pebble_y = center_y + radius * math.sin(angle)  # Y position on the circle
            self.cards_canvas.create_oval(
                pebble_x - self.RADIUS,
                pebble_y - self.RADIUS,
                pebble_x + self.RADIUS,
                pebble_y + self.RADIUS,
                fill=color,
                outline="black",
                width=2,
            )

        if happy_face:
            self.cards_canvas.create_text(
                center_x, center_y, text="😊", font=("Arial", 40)
            )

        self.current_x += 170

    def _draw_pebble_dic(self, x, y, bank: Dict[str, int]):

        for color, count in bank.items():
            # Draw the colored pebble
            self.player_state_canvas.create_oval(
                x, y, x + 20, y + 20, fill=color, outline="black", width=2
            )

            # Display the count next to the pebble

            self.player_state_canvas.create_text(
                x + 40, y, text=f"{count}", font=("Arial", 16), anchor="w"
            )
            y += 30

    def draw_playerstate(
        self,
        player_id: int,
        wallet: Dict[str, int],
        score: int,
        reachability: Optional[str] = None,
    ):
        """Draws the player's state on the board."""
        gap = 30
        x, y = 30, 30

        # Draw player ID

        self.player_state_canvas.create_text(
            x, y, text=f"Player ID: {player_id}", font=("Arial", 16), anchor="w"
        )
        y += gap

        # Draw player's wallet
        self.player_state_canvas.create_text(
            x, y, text="Wallet:", font=("Arial", 16), anchor="w"
        )
        y += gap
        self._draw_pebble_dic(x + x / 2, y, wallet)
        y += gap

        # Draw player score
        y += gap * 7
        self.player_state_canvas.create_text(
            x, y, text=f"Score: {score}", font=("Arial", 16), anchor="w"
        )
        y += gap
        # Draw reachability, if available
        if reachability:
            self.player_state_canvas.create_text(
                x,
                y,
                text=f"Reachability: {reachability}",
                font=("Arial", 16),
                anchor="w",
            )

    def show_input(self, input_string=None):
        """Reads JSON objects from the given input stream and processes them, then display the board."""
        if input_string:
            # If an input string is provided, convert it to a stream
            input_stream = StringIO(input_string)
        else:
            # Otherwise, default to using stdin
            input_stream = sys.stdin
        self.process_input(input_stream)
        self.show()

    def process_input(self, input_stream):
        """Reads JSON objects from the given input stream and processes them."""
        # Assuming process_input can read JSON for cards, banks, and player states, and call respective draw methods
        # for obj in ijson.items(input_stream, "", multiple_values=True):
        #     if 'pebbles' in obj:  # Example for drawing cards
        #         self.draw_card(obj['pebbles'])
        #     elif 'wallet' in obj and 'score' in obj:  # Example for drawing player state
        #         player_state = PlayerState(**obj)
        #         self.draw_playerstate(player_state)
        #     elif isinstance(obj, dict):  # Assuming bank input as a dictionary
        #         self.draw_bank(obj)
        pass
