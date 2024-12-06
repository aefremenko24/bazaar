# Directory _Common_

## Purpose
This directory contains files and data models that other components of this project will import and use.

## Files and Directories:

- **\_\_init\_\_.py**: marks this directory on disk as a Python package directory.
- **cards.py**: data model for cards.
- **test_cards.py**: tests for cards.py.
- **equations.py**: data model for equations.
- **test_equations.py**: tests for equations.py.
- **pebble.py**: data model for pebble and a collection of pebbles.
- **test_pebble.py**: tests for pebble.py.
- **turn_state.py**: data model for the turn state of the game.
- **data.py**: constants types and constants used in various files in this directory.
- **game_interface.py**: contains methods for drawing the user interface of the Bazaar game.
- **vertical_board.py**: contains methods for drawing the vertical board in the interface of the Bazaar game.
- **rule_book.py**: data model for the rule book representation of the game.

To run the tests, run the files beginning with "test" with Python. E.g. ``python3 ./Referee/testGameState.py``.