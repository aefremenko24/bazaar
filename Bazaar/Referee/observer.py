import json
import shutil
from copy import copy
from operator import index
from typing import List
import os

import pygame
from pydantic.v1.utils import ROOT_KEY
from pygame import K_ESCAPE
import tkinter
from tkinter import simpledialog

pygame.init()
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from pydantic import BaseModel, ConfigDict
from Bazaar.Common.vertical_board import SingleBoard
from Bazaar.Referee.game_state import GameState
from Bazaar.Common.render import render_game_state, render_text, __FONT_LARGE__, filename_popup

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIRECTORY = ROOT_DIR + "/Tmp/"

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 900
WHITE_COLOR = (255, 255, 255)
class Observer(BaseModel):
    """
    A component with which dev ops can watch and inspect a game from a referee’s perspective.
    Observer serves two purposes:
    - Saves the states it receives as PNG files in a directory called Tmp/, using the names "0.png", "1.png", and so on.
    - Displays the states it receives as images in a graphical user interface (GUI) with three interaction capabilities:
    next, previous, and save.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    is_game_over: bool = False
    show: bool = False
    states: List[GameState] = []
    current_view: int = 0
    screen: pygame.Surface = None
    popup_open: bool = False

    #TODO: adding the observable results in a circular import

    def __init__(self, **data) -> None:
        """
        Constructor for the observer class. Observable of type Referee must be provided at class initialization.

        :param board: the SingleBoard object used for rendering the game states.
        :type board: SingleBoard
        :param is_game_over: True if the game is over and no more states will become available, False otherwise.
        :type is_game_over: bool
        :param state_index: the index of the current state of the board, used for saving images (0.png, 1.png, etc.)
        :type state_index: int
        :param observable: the observable object which this observer is attached to.
        :type observable: Referee
        :param show: True if the state received should be shown in a GUI, False otherwise
        :type show: bool
        """
        super().__init__(**data)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.fill(WHITE_COLOR)
        self.check_tmp_directory()
        self.clear_tmp_folder()

    def check_events(self) -> bool:
        """
        Checks for updates in events sent to the current pygame instance.

        :return: False if the user decided to quit the observer view, True otherwise.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                self.show_next()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                self.show_prev()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.popup_open:
                filename = filename_popup(self.screen)
                self.save_to_json(filename)
                self.show_next()
        return True

    def update(self, game_state: GameState) -> None:
        """
        Saves the states it receives as PNG files in the Tmp/ directory under the {state_index}.png name.
        Provided a show argument of True, displays the states it receives as images in a graphical user interface (GUI).

        :param game_state: the current game state
        :type game_state: GameState
        """
        self.states.append(copy(game_state))
        self.check_events()
        self.screen.fill(WHITE_COLOR)
        render_game_state(game_state=game_state, screen=self.screen, index=len(self.states) - 1)
        pygame.display.update()
        pygame.image.save(self.screen, f"{SAVE_DIRECTORY}{len(self.states) - 1}.png")

    def show_next(self):
        """
        Shows the next state of the game, if it is available.
        """
        if self.current_view < len(self.states) - 1 and self.show:
            self.current_view += 1
            self.screen.fill(WHITE_COLOR)
            render_game_state(self.states[self.current_view], self.screen, index=self.current_view)
            pygame.display.update()

    def show_prev(self):
        """
        Shows the previous state of the game, if it is available.
        """
        if self.current_view > 0  and self.show:
            self.current_view -= 1
            self.screen.fill(WHITE_COLOR)
            render_game_state(self.states[self.current_view], self.screen, index=self.current_view)
            pygame.display.update()

    def game_over(self):
        """
        Alerts this observer that no more states will become available.
        Used by the referee when it shuts down.
        """
        pygame.display.update()
        pygame.image.save(self.screen, f"{SAVE_DIRECTORY}{len(self.states) - 1}.png")
        while self.check_events() and self.show:
            pass

    def save_to_json(self, filename=str(len(states))):
        """
        Saves the game state being currently viewed as a JSON.
        """
        if '.' in filename:
            filename = filename.split('.')[0]
        filename = filename.replace(" ", "_")
        if self.states:
            saved_gs = self.states[self.current_view]
            json_format = saved_gs.serialize()
            json_gs = json.dumps(json_format)
            file = open(filename + ".json",'w')
            file.write(json_gs)
            file.close()

    def check_tmp_directory(self):
        """
        Checks if the Tmp directory exists in the repo and creates it if it doesn't.
        """
        if not os.path.isdir(SAVE_DIRECTORY):
            os.mkdir(SAVE_DIRECTORY)

    def clear_tmp_folder(self):
        """
        Clears the contents of the Tmp directory before writing to it.
        """
        for filename in os.listdir(SAVE_DIRECTORY):
            file_path = os.path.join(SAVE_DIRECTORY, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))