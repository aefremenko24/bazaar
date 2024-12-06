#!/usr/bin/env python3.9

import os
import sys


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from Bazaar.Referee.observer import Observer
from Bazaar.Common.equations import Equations
from Bazaar.Referee.game_state import GameState
from Bazaar.Referee.referee import Referee

from Bazaar.Player.mechanism import deserialize_actors, serialize_actors
import json, ijson

def main(attach_observer: bool = False):
    json_values = []

    for obj in ijson.items(sys.stdin.buffer, "", buf_size=1, multiple_values=True):
        json_values.append(obj)

    actors = deserialize_actors(json_values[0])
    equations = Equations.deserialize(json_values[1])
    game_state = GameState.deserialize(json_values[2])

    referee = Referee(equations=equations)
    if attach_observer:
        observer = Observer()
        observer.show = True
        referee.register_observer(observer)

    winners, kicked = referee.execute_game(players=actors, game_state=game_state)
    winner_names = sorted([winner.actor.name for winner in winners])
    kicked_names = sorted([kicked.actor.name for kicked in kicked])

    json.dump(winner_names, sys.stdout)
    json.dump(kicked_names, sys.stdout)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--show":
        main(True)
    else:
        main(False)
