# Directory _Referee_

## Purpose
This directory contains files and data models that will be available to the referee of the Bazaar game to use.

## Files and Directories:

- **\_\_init\_\_.py**: marks this directory on disk as a Python package directory.
- **game_state.py**: data representation of the state of the Bazaar game known to the referee.
- **test_game_state.py**: tests for game_state.py.
- **player_state.py**: data representation of the state of a singular player in the Bazaar game known to the referee.
- **purchases.py**: data representation for representing the purchases of cards.
- **game_state_board.py**: contains methods for drawing the game state interface of the Bazaar game.
- **test_game_state_board.py**: tests for game_state_board.py.
- **referee.py**: data representation for representing the referee in the game.
- **test_referee.py**: tests for referee.py
- **observer.py**: data representation for representing the observer in the game.
- **test_observer.py**: tests for observer.py

To run the tests, run the files beginning with "test" with Python. E.g. ``python3 ./Referee/test_game_state.py``.