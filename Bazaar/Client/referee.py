import asyncio
import json
import socket
import sys
from asyncio import StreamReader, StreamWriter
from typing import List, Optional

import ijson

from Bazaar.Common.equations import Equations
from Bazaar.Player.exchanges import Exchange
from Bazaar.Player.mechanism import Mechanism
from Bazaar.Player.purchases import PurchaseSequence
from Bazaar.Server.server import Server
from Bazaar.Common.turn_state import TurnState

MNAME = 0
ARGUMENTS = 1

class ProxyReferee:
    """
    Communicates the requests received from the players with the server.
    """
    def __init__(self, player: Mechanism):
        self.player: Mechanism = player
        self.reader: Optional[StreamReader] = None
        self.writer: Optional[StreamWriter] = None

    async def start_ref(self, reader: StreamReader, writer: StreamWriter):
        """
        Connects the referee to the server and starts processing the requests until the connection is lost/closed.
        """
        self.reader = reader
        self.writer = writer

        while True:
            data = await reader.read(1024)
            if not data:
                raise Exception("Connection lost.")
            response = self.handle(data.decode("utf-8"))
            if response:
                writer.write(response.encode("utf-8"))
                await writer.drain()

    def send_message(self, message: str):
        """
        Sends a message to the client using its StreamWriter.

        :param message: Message to be sent.
        """
        try:
            self.writer.write(message.encode('utf-8'))
            asyncio.create_task(self.writer.drain())
        except Exception as e:
            raise Exception(f"Error sending message: {message}", e)

    def handle(self, message: str):
        """
        Handles messages received from the server following the remote interactions protocol.

        :param message: Message received from the server.
        :returns: Output received from the player for the method call corresponding to the message received.
        """
        request_list = list(ijson.items(message, "", multiple_items=True))

        if not request_list or not isinstance(request_list, list):
            return None
        if request_list[MNAME] == "name":
            return self.handle_name(request_list[ARGUMENTS])
        elif request_list[ARGUMENTS] == "setup":
            return self.handle_setup(request_list[ARGUMENTS])
        elif request_list[ARGUMENTS] == "request-pebble-or-trades":
            return self.handle_request_pt(request_list[ARGUMENTS])
        elif request_list[ARGUMENTS] == "request-cards":
            return self.handle_rc(request_list[ARGUMENTS])
        elif request_list[ARGUMENTS] == "win":
            return self.handle_win(request_list[ARGUMENTS])
        else:
            print("Invalid request. Suing the server.")
            self.writer.close()

    def validate_name_arguments(self, message_arguments: List[str]) -> bool:
        """
        Validates that the argument for the "name" MCall is a single string.

        :param message_arguments: Arguments received from the server.
        """
        if (not message_arguments
                or not isinstance(message_arguments, list)
                or len(message_arguments) != 1
                or not isinstance(message_arguments[0], str)
                or not len(message_arguments[0]) > 0):
            return False
        return True

    def handle_name(self, message_arguments: List[str]):
        """
        Handles the server's "name" request with the player.

        :param message_arguments: Arguments received from the server.
        """
        if self.validate_name_arguments(message_arguments):
            name = message_arguments[0]
            self.player.name = name
        else:
            raise ValueError("Invalid name arguments")

    def validate_setup_arguments(self, message_arguments: List[list]) -> bool:
        """
        Validates that the argument for the "setup" MCall is a single list of *Equations.

        :param message_arguments: Arguments received from the server.
        """
        if (not message_arguments
                or not isinstance(message_arguments, list)
                or not len(message_arguments) == 1
                or not isinstance(message_arguments[0], list)):
            return False
        return True

    def handle_setup(self, message_arguments: List[list]):
        """
        Handles the server's "setup" request with the player.

        :param message_arguments: Arguments received from the server.
        """
        if self.validate_setup_arguments(message_arguments):
            equations = Equations.deserialize(message_arguments[0])
            self.player.setup(equations)
        else:
            raise ValueError("Invalid setup arguments")

    def validate_handle_request_pt(self, message_arguments: dict):
        """
        Validates that the argument for the "request-pebble-or-trades" MCall is a dictionary representing a TurnState.

        :param message_arguments: Arguments received from the server.
        """
        if (not message_arguments
            or not isinstance(message_arguments, dict)
            or not TurnState.validate_deserialize_data(message_arguments[0])):
            return False
        return True

    def handle_request_pt(self, message_arguments: dict):
        """
        Handles the server's "request-pebble-or-trades" request with the player.
        """
        if self.validate_handle_request_pt(message_arguments):
            turn_state = TurnState.deserialize(message_arguments[0])
            exchanges = self.player.request_pebble_or_trades(turn_state)
            self.send_message(json.dumps(Exchange.serialize(exchanges)))
        else:
            raise ValueError("Invalid request pebble or exchange arguments")

    def validate_handle_rc(self, message_arguments: dict):
        """
        Validates that the argument for the "request-cards" MCall is a dictionary representing a TurnState.

        :param message_arguments: Arguments received from the server.
        """
        if (not message_arguments
            or not isinstance(message_arguments, dict)
            or not TurnState.validate_deserialize_data(message_arguments[0])):
            return False
        return True

    def handle_rc(self, message_arguments: dict):
        """
        Handles the server's "request-cards" request with the player.
        """
        if self.validate_handle_request_pt(message_arguments):
            turn_state = TurnState.deserialize(message_arguments[0])
            cards = self.player.request_cards(turn_state)
            self.send_message(json.dumps(PurchaseSequence.serialize(cards)))
        else:
            raise ValueError("Invalid request cards arguments")


    def validate_handle_win(self, message_arguments: List[bool]):
        """
        Validates that the argument for the "win" MCall is a single boolean value.

        :param message_arguments: Arguments received from the server.
        """
        if (not message_arguments
                or not isinstance(message_arguments, list)
                or len(message_arguments) != 1
                or not isinstance(message_arguments[0], bool)):
            return False
        return True

    def handle_win(self, message_arguments: List[bool]):
        """
        Handles the server's "win" request with the player.

        :param message_arguments: Arguments received from the server.
        """
        if self.validate_handle_win(message_arguments):
            win_value = message_arguments[0]
            self.player.win(win_value)
        else:
            raise ValueError("Invalid win arguments")