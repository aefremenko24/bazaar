from collections import deque
from copy import deepcopy, copy
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict

from Bazaar.Common import equations
from Bazaar.Common.data import MAX_EQUATION_NUM
from Bazaar.Common.equations import Equations, Equation

from Bazaar.Common.pebble import init_bank, PebbleCollection
from Bazaar.Common.rule_book import RuleBook

from Bazaar.Common.turn_state import TurnState
from Bazaar.Player.purchases import PurchaseSequence
from Bazaar.Referee.game_state import GameState
from Bazaar.Referee.observer import Observer
from Bazaar.Referee.player_state import PlayerState
from Bazaar.Common.cards import Cards
from Bazaar.Player.mechanism import Mechanism
from typing import List, Optional

"""
The referee module implements a state machine that advances through game phases until the game is over.
The module will perform the following validations and kick players that fail any one of them:
- Has the player requested a pebble only when the bank has enough pebbles to give?
- Has the player only traded the equations available in the game and tradeable with their wallet and bank?
- Has the player only purchased cards from the visible deck that they are able to purchase with their wallet? 
"""


class State(BaseModel):
    """
    Base class for all phases of state.

    :param game_state: current game state
    :type game_state: GameState
    :param equations: equations available to trade
    :type equations: Equation
    :param kicked_players: players that have been kicked out of the game
    :type kicked_player: List[PlayerState]
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    game_state: GameState = None
    equations: Equations = None
    kicked_players: List[PlayerState] = Field(default_factory=list)

    def handle(self):
        """
        Handles the transition between different phases of the game.
        """
        raise NotImplementedError("handle method should be overridden.")

    def update_gamestate_notify_player(
        self,
        invisible_deck: Cards,
        visible: Cards,
        players: deque[PlayerState],
        bank: PebbleCollection,
    ) -> GameState:
        """
        Create a new game state with the given fields and update the players with the new turn states.

        :param invisible_deck: invisible cards
        :type invisible_deck: Cards
        :param visible: visible cards
        :type visible: Cards
        :param players: players in the game
        :type players: List[PlayerState]
        :param bank: current bank
        :type bank: PebbleCollection
        :return: new game state
        :rtype: GameState
        """
        new_game_state = GameState(
            bank=bank,
            visibles=visible,
            invisible_deck=invisible_deck,
            players=players,
            equations=self.equations,
        )
        return new_game_state

    def kick_n_advance(self):
        """
        Kick the active player, update game state, and advance to the next phase.
        """
        from Bazaar.Common.rule_book import RuleBook
        new_kicked = self.game_state.kick_active_player()
        self.game_state = self.update_gamestate_notify_player(
            self.game_state.invisible_deck,
            self.game_state.visibles,
            self.game_state.players,
            self.game_state.bank,
        )
        self.kicked_players.append(new_kicked)
        if RuleBook.is_game_over(self.game_state):
            return OverState(
                game_state=self.game_state,
                equations=self.equations,
                kicked_players=self.kicked_players,
            )
        return ExchangeState(
            game_state=self.game_state, equations=self.equations, kicked_players=self.kicked_players
        )


class InitState(State):
    """
    Initial state of the game, setting up the game and advance to ExchangeState with the first player.
    Or continue to player a game if pass in  a game state
    """

    def set_initial_state(
        self,
        players: List[Mechanism],
        equations: Equations,
        game_state: GameState = None,
    ) -> GameState:
        """
        Set up the initial phase using the given GameState.
        If no game state is given, initializes a new game state.

        :param players: list of player mechanisms
        :type players: List[Mechanism]
        :param equations: equations used in the game
        :type players: Equations
        :param game_state: game state to be used
        :type game_state: Optional[GameState]
        :return: initial game state
        :rtype: GameState
        """
        self.game_state = game_state

        if not self.game_state:
            self.game_state = InitState.__create_game_state(players, equations)

        self.game_state.equations = equations
        self.game_state.fill_actors(players)

        for player in copy(players):
            try:
                player.setup(self.game_state.equations)
            except Exception:
                self.kicked_players.append(self.get_player_state(player))
                self.game_state.kick_player_by_actor(player)

        return self.game_state

    @staticmethod
    def get_player_state(player: Mechanism) -> PlayerState:
        """
        Initialize a player state with a given mechanism.

        :param player: mechanism to be used by the player
        :type player: Mechanism
        :return: initial player state with empty wallet and 0 score
        :rtype: PlayerState
        """
        player_state = PlayerState()
        player_state.actor = player
        return player_state

    @staticmethod
    def __create_game_state(players: List[Mechanism], equations: Equations) -> GameState:
        """
        Initializes the start-of-the-game game state.

        :param equations: Equations used for running the game.
        :type equations: Equations
        :param players: list of player mechanisms
        :type players: List[Mechanism]
        :return: game state for the beginning of the game
        :rtype: GameState
        """
        bank = init_bank()
        all_cards = Cards.generate_random()
        visible_cards = Cards(cards=all_cards.cards[-4:])
        invisible_cards = Cards(cards=all_cards.cards[:-4])
        player_deque = deque([InitState.get_player_state(player) for player in players])
        return GameState(
            equations=equations,
            bank=bank,
            visibles=visible_cards,
            invisible_deck=invisible_cards,
            players=player_deque,
        )

    def handle(self):
        """ "
        Advance to exchange state, where the active player will be asked to provide exchanges..

        :return: new exchange state
        :rtype: ExchangeState
        """
        return ExchangeState(
            game_state=self.game_state,
            equations=self.game_state.equations,
            kicked_players=self.kicked_players,
        )


class ExchangeState(State):
    def handle(self):
        """
        Ask the player to request a pebble or provide exchanges, then handle transition from ExchangesState to PurchaseState.

        :return: purchase state that ask player to purchase
        :rtype: PurchaseState
        """
        turn_state = self.game_state.extract_turnstate()

        pebbleTuple = self.__get_exchange_from_player(turn_state)
        if not pebbleTuple:
            return self.kick_n_advance()
        wallet, bank = pebbleTuple
        return self.__update_n_advance(wallet, bank)

    def __get_exchange_from_player(
        self, turn_state: TurnState
    ) -> Optional[tuple[PebbleCollection, PebbleCollection]]:
        """
        Ask the player to make an exchange action and output the updated or original wallet and bank.
        If the action is a list of non-empty equations,player request to exchanges with such equations. If the action is
        an empty list, player request to draw a pebble. If the action is None, player request to skip the turn.
        Return None if player's actions is invalid.

        :param turn_state: current turn state
        :type turn_state: TurnState
        :return: updated wallet and bank
        :rtype: tuple[PebbleCollection, PebbleCollection]
        """
        current_player = self.game_state.get_active_player()
        player_mechanism = current_player.actor
        try:
            rules = player_mechanism.request_pebble_or_trades(turn_state)
        except Exception:
            return None
        if rules and len(rules) > 0:
            return self.__validate_exchange_and_remove_cards(turn_state, rules)
        elif len(rules) == 0:
            return self.__validate_draw_pebble(turn_state)
        return current_player.wallet, turn_state.bank

    def __validate_exchange_and_remove_cards(
        self, turn_state: TurnState, rules: list[Equation]
    ) -> Optional[tuple[PebbleCollection, PebbleCollection]]:
        """
        Validate a request to trade a sequence of equations and return the updated wallet and bank.
        If legal, also remove the bottom card in the visible deck.
        Return None if illegal.

        :param turn_state: current turn state
        :type turn_state: TurnState
        :param rules: list of directed equations to use for trading
        :type rules: list[Equation]
        :return: updated wallet and bank if legal, None otherwise
        :rtype: Optional[tuple[PebbleCollection, PebbleCollection]]
        """
        from Bazaar.Common.rule_book import RuleBook
        pebbleTuple = RuleBook.validate_exchange_request(
            turn_state, rules, self.equations
        )
        if pebbleTuple:
            if len(self.game_state.invisible_deck.cards) > 0:
                self.game_state.invisible_deck.cards.pop()
            elif len(self.game_state.visibles.cards) > 0:
                self.game_state.visibles.cards.pop()
        return pebbleTuple

    def __validate_draw_pebble(
        self, turn_state: TurnState
    ) -> Optional[tuple[PebbleCollection, PebbleCollection]]:
        """
        Validate a request to draw a pebble and return the updated wallet and bank if the move is legal.

        :param turn_state: current turn state
        :type turn_state: TurnState
        :return: updated wallet and bank if the move is legal, None otherwise
        :rtype: Optional[tuple[PebbleCollection, PebbleCollection]]
        """
        from Bazaar.Common.rule_book import RuleBook
        return RuleBook.valid_draw_pebble_request(turn_state)

    def __update_n_advance(
        self, wallet: PebbleCollection, bank: PebbleCollection
    ):
        """
        Update the player's state after it trades, notify other players about the update, check if the game is over.
        Advance to the next state if the game is not over.

        :param turn_state: current turn state
        :type turn_state: TurnState
        :param wallet: player's wallet
        :type wallet: PebbleCollection
        :param bank: player's bank
        :type bank: PebbleCollection
        :return: PurchaseState if the game is not over, OverState otherwise
        :rtype: PurchaseState or OverState
        """
        from Bazaar.Common.rule_book import RuleBook
        active_player = self.game_state.get_active_player()
        new_playerState = PlayerState(
            wallet=wallet,
            score=active_player.score,
            actor=active_player.actor,
        )
        self.game_state.players[0] = new_playerState
        self.game_state = self.update_gamestate_notify_player(
            self.game_state.invisible_deck,
            self.game_state.visibles,
            self.game_state.players,
            bank,
        )
        if RuleBook.is_game_over(self.game_state):
            return OverState(
                game_state=self.game_state,
                equations=self.equations,
                kicked_players=self.kicked_players,
            )
        return PurchaseState(
            game_state=self.game_state,
            equations=self.equations,
            kicked_players=self.kicked_players,
        )


class PurchaseState(State):
    score: int = 0

    def handle(self):
        """
        Ask the player to provide a sequence of cards to trade, validate, then advance to the next state.
        """
        turn_state = self.game_state.extract_turnstate()

        pebbleTuple, cards = self.__get_purchase_from_player(turn_state)

        if not pebbleTuple:
            return self.kick_n_advance()
        wallet, bank = pebbleTuple
        return self.__update_n_advance(turn_state, wallet, bank, cards)

    def __get_purchase_from_player(
        self, turn_state: TurnState
    ) -> Optional[tuple[PebbleCollection, PebbleCollection]]:
        """
        Ask the player to make a purchase action and output the updated wallet and bank.
        Return None if one of the player's actions is invalid and the player is kicked.

        :param turn_state: current turn state
        :type turn_state: TurnState
        :return: updated wallet and bank
        :rtype: tuple[PebbleCollection, PebbleCollection]
        """
        current_player = self.game_state.get_active_player()
        player_mechanism = current_player.actor
        try:
            cards = player_mechanism.request_cards(turn_state)
        except Exception:
            return None
        if cards:
            self.score = cards.points
            return self.__validate_purchase_and_remove_cards(turn_state, cards)
        else:
            return None

    def __validate_purchase_and_remove_cards(
        self, turn_state: TurnState, cards: PurchaseSequence
    ) -> Optional[tuple[PebbleCollection, PebbleCollection]]:
        """
        Validate a request to purchase a sequence of cards and return the updated wallet and bank.
        If legal, also remove the bottom card in the visible deck.
        Return None if illegal.

        :param turn_state: current turn state
        :type turn_state: TurnState
        :param rules: list of directed equations to use for trading
        :type rules: list[Equation]
        :return: updated wallet and bank if legal, None otherwise
        :rtype: Optional[tuple[PebbleCollection, PebbleCollection]]
        """
        from Bazaar.Common.rule_book import RuleBook
        pebbleTuple = RuleBook.valid_purchase_request(turn_state, cards.sequence)
        if pebbleTuple:
            card_num = len(cards.sequence.cards)
            for card in cards.sequence.cards:
                self.game_state.visibles.cards.remove(card)
            if len(self.game_state.invisible_deck.cards) > 0:
                num_to_draw = min(card_num, len(self.game_state.invisible_deck.cards))
                for _ in range(num_to_draw):
                    card = self.game_state.invisible_deck.cards.pop(0)
                    self.game_state.visibles.add_card(card)

        return pebbleTuple, cards

    def __update_n_advance(
        self, turn_state: TurnState, wallet: PebbleCollection, bank: PebbleCollection, cards: PurchaseSequence
    ):
        """
        Update the player's state after it trades, notify other players about the update, check if the game is over.
        Advance to the next state if the game is not over.

        :param turn_state: current turn state
        :type turn_state: TurnState
        :param wallet: player's wallet
        :type wallet: PebbleCollection
        :param bank: player's bank
        :type bank: PebbleCollection
        :return: ExchangeState if the game is not over, OverState otherwise
        :rtype: ExchangeState or OverState
        """
        from Bazaar.Common.rule_book import RuleBook
        active_player = self.game_state.get_active_player()
        new_score = active_player.score + self.score
        new_playerState = PlayerState(
            wallet=wallet,
            score=new_score,
            cards= active_player.cards.extend(cards.sequence.cards),
            actor=active_player.actor,
        )
        self.game_state.players[0] = new_playerState
        self.game_state.next_turn()
        self.game_state = self.update_gamestate_notify_player(
            self.game_state.invisible_deck,
            self.game_state.visibles,
            self.game_state.players,
            bank,
        )
        if RuleBook.is_game_over(self.game_state):
            return OverState(
                game_state=self.game_state,
                equations=self.equations,
                kicked_players=self.kicked_players,
            )
        return ExchangeState(
            game_state=self.game_state,
            equations=self.equations,
            kicked_players=self.kicked_players,
        )


class OverState(State):
    def get_winner_n_kicked(self):
        """
        Return the winner and players that cheated and were kicked.
        """
        from Bazaar.Common.rule_book import RuleBook
        return (RuleBook.get_highest_score(self.game_state), self.kicked_players)

    def handle(self):
        """
        No transition in overstate, return itself.
        """
        return self


class BonusType(Enum):
    RWB = "RWB"
    SEY = "SEY"

class Referee(BaseModel):
    equations: Optional[Equations] = None
    bonus: Optional[BonusType] = None
    observers: List[Observer] = Field(default_factory=list)

    def notify_result(
        self,
        winners: List[PlayerState],
        kicked: List[PlayerState],
        players: deque[PlayerState],
    ) -> (List[PlayerState], List[PlayerState]):
        """
        Notify remaining players in the game whether they win or not.
        Returns the final list of winners and kicked players in case players have been kicked during this step.

        :param winners: winners
        :type winners:list[PlayerState]
        :param kicked: player that been kicked during the game
        :type kicked: list[PlayerState]
        :param players: all remaining players
        :type players:deque[PlayerState]
        :return: winners and kicked players
        :rtype: list[PlayerState], list[PlayerState]
        """
        final_winners = copy(winners)
        final_kicked = copy(kicked)
        if len(final_winners) == 0:
            return final_winners, final_kicked

        for player in winners:
            if player in winners:
                try:
                    player.actor.win(True)
                except:
                    final_kicked.append(player)
                    final_winners.remove(player)
                    if len(final_winners) == 0:
                        break
            elif player not in kicked:
                try:
                    player.actor.win(False)
                except:
                    final_kicked.append(player)
        if len(final_winners) == 0:
            new_winners = self.get_new_winner(players,final_kicked)
            return self.notify_result(new_winners,final_kicked,players)
        return final_winners, final_kicked

    # Deque[PlayerState] List[PlayerState] -> List[PlayerState]
    # finds a new winner of players that remain in the game after the current winner has been kicked
    def get_new_winner(self, players: deque[PlayerState], kicked: List[PlayerState]):
        unkicked = []
        for player in players:
            if not player.actor.name in [kick.actor.name for kick in kicked]:
                unkicked.append(player)
        if not unkicked:
            return []
        highest_score = max(player.score for player in unkicked)
        return [player for player in unkicked if player.score == highest_score]

    def init_game_state(
        self, players: List[Mechanism], game_state: GameState = None
    ) -> State:
        """
         Sets up the initial state for the state machine. Generates equations if there is no equations currently and
         sends them to the players.
         Game state is optional provided for testing purposes.

         :param players: all player
         :type players: List[Mechanism]
         :param game_state: GameState provided for testing purposes
         :type game_state: Optional[GameState]
         :return: InitState
        """
        state = InitState()
        state.set_initial_state(players, self.equations, game_state)
        return state

    def execute_game(
        self, players: List[Mechanism], game_state: GameState = None
    ) -> tuple[list[PlayerState], list[PlayerState]]:
        """
        Plays the game until the game is over. Game state is optional provided for testing purposes.

        :param players: list of player mechanisms
        :type players: list[Mechanism]
        :param game_state: game state
        :type game_state: GameState
        :return: winners and kicked players
        :rtype: tuple[list[PlayerState], list[PlayerState]]
        """
        if not self.equations:
            self.equations = Equations.generate_random(MAX_EQUATION_NUM)

        state = self.init_game_state(players, game_state)

        winners, kicked = self.handle_turns(state)

        winners, kicked = self.notify_result(winners, kicked, state.game_state.players)
        return winners, kicked

    def handle_turns(self, state: State) -> tuple[list[PlayerState], list[PlayerState]]:
        """
        Handles turns in the current game until the game is over.
        The .handle() method in each state will change the states in the following order:
        InitState -> ExchangeState -> PurchaseState -> OverState
        In any of the above states, the game may be deemed over by the referee and the transition to OverState will happen.

        :param state: current state of the game
        :type state: State
        :return: winners and kicked players
        :rtype: tuple[list[PlayerState], list[PlayerState]]
        """
        while not isinstance(state, OverState):
            state = state.handle()
            self.update_observers(state.game_state)
        if self.bonus == BonusType.RWB:
            from Bazaar.Common.rule_book import RuleBook
            RuleBook.usa_bonus(state)
        if self.bonus == BonusType.SEY:
            from Bazaar.Common.rule_book import RuleBook
            RuleBook.sey_bonus(state)
        state.handle()
        self.observers_game_over()
        return state.get_winner_n_kicked()

    def update_observers(self, game_state: GameState) -> None:
        """
        Refers to each Observer object in the observers list to notify them about the updated GameState.

        :param game_state: updated game state to be sent to the observers
        :type game_state: GameState
        """
        for observer_index, observer in enumerate(self.observers):
            try:
                observer.update(game_state)
            except Exception:
                self.observers.pop(observer_index)

    def observers_game_over(self) -> None:
        """
        Notifies each observer that the game is over and no more game states will be sent.
        """
        for observer_index, observer in enumerate(self.observers):
            try:
                observer.game_over()
            except Exception:
                self.observers.pop(observer_index)

    def register_observer(self, observer: Observer) -> None:
        """
        Adds the given observer to the observers list.

        :param observer: observer to register
        :type observer: Observer
        """
        self.observers.append(observer)