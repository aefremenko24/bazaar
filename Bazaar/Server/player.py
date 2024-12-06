import asyncio
from asyncio import StreamReader, StreamWriter
import json
import re

import ijson

from Bazaar.Common.equations import Equations
from Bazaar.Common.turn_state import TurnState
from Bazaar.Player.exchanges import Exchange
from Bazaar.Player.purchases import PurchaseSequence

MAX_RESPONSE_TIME = 1.0

class ProxyPlayer:
    """
    Communicates the requests received from the referee with the client.
    """
    def __init__(self, reader: StreamReader, writer: StreamWriter):
        self.name = None
        self.writer = writer
        self.reader = reader

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

    async def read_response(self) -> dict:
        """
        Waits for a response from the client for MAX_RESPONSE_TIME seconds
        and deserializes it if received.
        """
        try:
            data = await asyncio.wait_for(self.reader.read(1024), timeout=MAX_RESPONSE_TIME)
            response = list(ijson.items(data, ""))
            if not response:
                self.writer.close()
            return response[0]
        except:
            self.writer.close()

    def set_name(self, name: str) -> None:
        """
        Sets the player's name.

        :param name: The player's name.
        """
        self.name = name

    def name(self, name: str):
        """
        Sends the name for this player to the proxy referee.

        :param name: Player's name.
        """
        serialized = self.serialize_name(name)
        self.send_message(serialized)

    def setup(self, equations: Equations):
        """
        Sends the setup call to the proxy referee.

        :param equations: Equations to be sent with the setup call.
        """
        serialized = self.serialize_setup(equations)
        self.send_message(serialized)

    def request_pebble_or_trades(self, turn_state: TurnState):
        """
        Sends the request for pebble or trades to the proxy referee.

        :param turn_state: TurnState to be sent to the proxy referee.
        """
        serialized = self.serialize_request_pt(turn_state)
        self.send_message(serialized)
        received_response = dict(self.read_response())
        return Exchange.deserialize(received_response).pebble_exchanges

    def request_cards(self, turn_state: TurnState):
        """
        Sends the request for cards to the proxy referee.

        :param turn_state: TurnState to be sent to the proxy referee.
        """
        serialized = self.serialize_rc(turn_state)
        self.send_message(serialized)
        received_response = dict(self.read_response())
        return PurchaseSequence.deserialize(received_response)

    def win(self, win: bool):
        """
        Notifies the proxy referee that the player won.

        :param win: True if the player won.
        """
        serialized = self.serialize_win(win)
        self.send_message(serialized)

    def serialize_name(self, name: str):
        """
        Serialized the name method call into the proper JSON format.
        """
        name_call = "name"
        call = [name_call, [name]]
        j_call = json.dumps(call)
        return j_call

    def serialize_setup(self, equations: Equations):
        """
        Serialized the setup method call into the proper JSON format.
        """
        j_eq = equations.serialize()
        setup = "setup"
        call = [setup,[j_eq]]
        j_call = json.dumps(call)
        return j_call

    def serialize_request_pt(self, turnstate: TurnState):
        """
        Serialized the request pebble or exchanges method call into the proper JSON format.
        """
        j_turn = turnstate.serialize()
        request = "request-pebble-or-trades"
        call = [request,[j_turn]]
        j_call = json.dumps(call)
        return j_call


    def serialize_rc(self, turnstate: TurnState):
        """
        Serialized the request cards method call into the proper JSON format.
        """
        j_turn = turnstate.serialize()
        request = "request-cards"
        call = [request,[j_turn]]
        j_call = json.dumps(call)
        return j_call

    def serialize_win(self, win: bool):
        """
        Serialized the win method call into the proper JSON format.
        """
        win_call = "win"
        call = [win_call,[win]]
        j_call = json.dumps(call)
        return j_call