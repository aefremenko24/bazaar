import asyncio
import json
import re
import sys
from typing import Optional, Tuple

from Bazaar.Client.referee import ProxyReferee
from Bazaar.Player.mechanism import Mechanism
from Bazaar.Common.turn_state import TurnState
from Bazaar.Server.server import DEFAULT_HOST

MIN_PORT_NUM = 1024
MAX_PORT_NUM = 65353
SIZE_POLICY = "purchase-size"
POINTS_POLICY = "purchase-points"

class Client:
    """
    TCP-connects a player (or several players) to a server.
    """
    def __init__(self):
        self.reader: asyncio.StreamReader = None
        self.writer: asyncio.StreamWriter = None
        self.player_mechanism: Mechanism = None
        self.referee: ProxyReferee = None

    def start_client(self, name: str = None, policy: str = None, port: int = None):
        """
        Starts the client using asyncio.run().

        :param name: The name of the player to be connected.
        :param policy: The policy of the player.
        :param port: The port number to be connected to.
        """
        asyncio.run(self.run(name, policy, port))

    async def run(self, name: str = None, policy: str = None, port: int = None):
        """
        Runs the game until completion and closes the server when done.

        :param name: The name of the player to be connected.
        :param policy: The policy of the player.
        :param port: The port number to be connected to.
        """
        name = self.prompt_name() if not name else name
        policy = self.prompt_policy() if not policy else policy
        port = self.prompt_port() if not port else port
        host = DEFAULT_HOST

        self.player_mechanism = self.init_mechanism(name, policy)
        self.referee = self.init_proxy_referee(self.player_mechanism)

        try:
            await self.connect(port=port, host=host)
            await self.sign_up(name)
        except Exception as e:
            print(f"Failed to sign up with the server. Closing the connection. Error Message: {e}")
            if self.writer:
                self.writer.close()

    def init_mechanism(self, name: str, policy: str) -> Mechanism:
        """
        Initializes the player Mechanism with the given name and policy.
        """
        return Mechanism(name=name, policy=policy)

    def init_proxy_referee(self, player: Mechanism) -> ProxyReferee:
        """
        Initializes the Proxy Referee with the given player Mechanism
        """
        return ProxyReferee(player=player)

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
        if not re.fullmatch("^[a-zA-Z0-9]+$", name):
            print("Name must contain only alphanumeric characters.")
            return False
        return True

    def prompt_name(self) -> str:
        """
        Prompts the player to enter their name.

        :returns: The player's name.
        """
        name = input("Enter the name you'd like to use in the game: ")
        while not self.validate_name(name):
            name = input("Invalid name. Please try again: ")
        return str(name)

    def prompt_policy(self) -> str:
        """
        Prompts the player to enter their policy.

        :returns: The player's policy (one of 'purchase-points' or 'purchase-size').
        """
        print("""Which policy would you like your AI player to use? (1 or 2)
        1. Maximize the number of points received in one turn.
        2. Maximize the number of cards bought in one turn.""")
        policy_choice = int(input())

        while not policy_choice in [1, 2]:
            policy_choice = int(input("Invalid option. Please try again: "))
        policy = POINTS_POLICY if policy_choice == 1 else SIZE_POLICY

        return policy

    def prompt_port(self) -> int:
        """
        Prompts the player to enter the port to connect the client to and sets it in the self.port field.
        """
        port = input(f"Enter the port to connect to (in range {MIN_PORT_NUM}-{MAX_PORT_NUM}): ")
        while not int(port) >= MIN_PORT_NUM and int(port) <= MAX_PORT_NUM:
            port = input(f"Invalid port. Please try again: ")
        return int(port)

    def prompt_host(self) -> str:
        """
        Prompts the player to enter the host to connect the client to and sets it in the self.host field.
        """
        host = input(f"Enter the host to connect to: ")
        while not host:
            host = input(f"Invalid host. Please try again: ")
        return host

    async def connect(self, port: int, host: str):
        """
        Initializes the TCP connection to the server.

        :param port: The port to connect to.
        :param host: The host to connect to.
        """
        try:
            self.reader, self.writer = await asyncio.open_connection(host=host, port=port)
            print(f"You are connected to the server. Port: {port}, Host: {host}")
        except Exception as e:
            raise Exception(f"Failed to connect to the server: {e}")

    async def sign_up(self, name: str):
        """
        Sends the player's name to the server to register.

        :param name: The player's name.
        """
        if not self.writer:
            raise ConnectionError("No connection established to sign up.")

        self.writer.write(name.encode('utf-8'))
        await self.writer.drain()

    async def wait_for_server(self):
        """
        Once the client and server are up, client waits fro the server to send something until the end of time.
        """
        while True:
            try:
                data = await asyncio.wait_for(self.reader.read(1024), timeout=99999)
                data = data.decode("utf-8")
                json.dump(data, sys.stdout)
            except:
                pass