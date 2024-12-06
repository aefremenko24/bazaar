import asyncio
import json
import sys
from asyncio import StreamWriter, StreamReader
from sys import stdin
from typing import Optional, List, Tuple

from Bazaar.Common.equations import Equations
from Bazaar.Referee.game_state import GameState
from Bazaar.Referee.player_state import PlayerState
from Bazaar.Referee.referee import Referee, BonusType
from player import ProxyPlayer

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 15555
MAX_PLAYER_NUM = 6
MIN_PLAYER_NUM = 2
MAX_WAITING_ROUNDS = 2
MAX_SIGNUP_WAITING_TIME = 20.0
MAX_SEND_NAME_WAITING_TIME = 3.0
DEFAULT_SERVER_OUTPUT = ([],[])

class Server():
    """
    Waits for player TCP sign-ups.
    If a sufficient number of clients sign up, the server hands them to the Referee.
    When the Referee’s work is done, it returns its results to the server.
    """
    def __init__(self, port: int = DEFAULT_PORT, host: str = DEFAULT_HOST):
        self.referee: Optional[Referee] = None
        self.players: List[ProxyPlayer] = []
        self.port = port
        self.host = host

    def start_server(self):
        """
        Starts the server using asyncio.run().
        """
        winners, kicked = asyncio.run(self.run_server())
        winners_deserialized = sorted([json.loads(winner.actor.name) for winner in winners])
        kicked_deserialized = sorted([json.loads(kick.actor.name) for kick in kicked])
        output = [winners_deserialized, kicked_deserialized]
        json.dump(output, sys.stdout)

    def register_player(self, name: str, reader: StreamReader, writer: StreamWriter):
        """
        Register a player with the given name to the server.

        :param name: the name of the player.
        """
        new_proxy_player = ProxyPlayer(reader=reader, writer=writer)
        new_proxy_player.set_name(name)
        self.players.append(new_proxy_player)

    def run_game(self, bonus: BonusType = None, game_state: GameState = None, equations: Equations = None) -> Tuple[List[PlayerState], List[PlayerState]]:
        """
        Initializes a Referee object and delegates the run of the game to it.

        :param bonus: an optional Bonus specification. If it is missing, no player gets a bonus.
        :param game_state: the game state for testing purposes.
        :param equations: the equations for testing purposes.
        """
        self.referee = Referee(equations=equations, bonus=bonus)
        return self.referee.execute_game(players=self.players, game_state=game_state)

    def validate_name(self, name: str) -> bool:
        """
        Validates the name entered by the player by checking that it is a string of at least 1 character in length,
        containing only alphanumeric characters.

        :param name: The player's name.
        :returns: True if the player's name is valid, False otherwise.'
        """
        if not isinstance(name, str):
            print("Name must be a string.")
            return False
        if not len(name) > 0:
            print("Name cannot be an empty string.")
            return False
        if not name.isalpha():
            print("Name must contain only alphabetic characters.")
            return False
        return True

    def parse_name_request(self, data: bytes) -> Optional[str]:
        """
        Parses the client's sign up request as a player's name and check that the request is valid.

        :param data: The player's name as a byte stream.
        :returns: Player's name if the name is valid, None otherwise.
        """
        try:
            data = data.decode("utf-8")
            if not self.validate_name(data):
                return None
            name = json.dumps(data)
        except:
            return None
        return name

    async def handle_client(self, reader: StreamReader, writer: StreamWriter):
        """
        Handle the client's sign up request. If the client provides an invalid name or takes too long to respond,
        the connection between the client and the server is closed.
        """
        try:
            data = await asyncio.wait_for(reader.read(1024), timeout=MAX_SEND_NAME_WAITING_TIME)
            name = self.parse_name_request(data)
            if not name:
                writer.close()
            self.register_player(name, reader, writer)
        except:
            writer.close()

    async def run_server(self, bonus: BonusType = None, game_state: GameState = None, equations: Equations = None):
        """
        Starts up the server with the handle_client method as a handler and waits for
        20 seconds MAX_WAITING_ROUNDS times for 2 to 6 players to join.

        :param bonus: optional Bonus specification. If it is missing, no player gets a bonus.
        :param game_state: the game state for testing purposes.
        :param equations: the equations for testing purposes.
        """
        rounds = 0
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        while rounds < MAX_WAITING_ROUNDS and len(self.players) < MAX_PLAYER_NUM:
            await asyncio.sleep(MAX_SIGNUP_WAITING_TIME)
            if len(self.players) >= MIN_PLAYER_NUM and len(self.players) <= MAX_PLAYER_NUM:
                break
            rounds += 1

        if len(self.players) >= MIN_PLAYER_NUM:
            return self.run_game(bonus=bonus, game_state=game_state, equations=equations)
        else:
            server.close()
            return DEFAULT_SERVER_OUTPUT