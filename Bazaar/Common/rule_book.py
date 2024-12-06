from Bazaar.Common.cards import Cards, Card
from Bazaar.Common.data import MAX_EXCHANGE_DEPTH, CARD_REWARDS, WIN_SCORE
from Bazaar.Common.equations import Equation, Equations
from Bazaar.Common.pebble import PebbleCollection, Pebble
from typing import List, Optional, Tuple
from copy import copy

from Bazaar.Common.turn_state import TurnState


class RuleBook:
    """
    Contains common rules used to validate player-to-referee action requests.
    """

    @staticmethod
    def __can_trade_equation_side(
        equation,
        trade_left_side: bool,
        player_pebbles: PebbleCollection,
        bank: PebbleCollection,
    ) -> bool:
        """
        Checks if the player can use the given side of the equation based on the given pebble wallet and pebble bank dictionaries.

        :param equation: the equation the player wishes to use for exchange
        :param trade_left_side: True to check whether the equation can be used from left to right, False if trading from right to left.
        :param player_pebbles: Dictionary of player pebbles.
        :param bank: Dictionary of bank pebbles.
        :returns: True if the equation can be used in the give direction.
        :rtype: bool
        """
        if trade_left_side:
            return equation.lhs.subset_of(player_pebbles) and equation.rhs.subset_of(
                bank
            )
        else:
            return equation.rhs.subset_of(player_pebbles) and equation.lhs.subset_of(
                bank
            )

    @staticmethod
    def can_trade_equation(
        equation: Equation, player_wallet: PebbleCollection, bank: PebbleCollection
    ) -> bool:
        """
        Determines if the given equation can be used for a trade based on the player's wallet and the bank.

        :param equation: The equation the player wishes to use for exchange.
        :type equation: Equation
        :param player_wallet: The PebbleCollection representing the player's current wallet.
        :type player_wallet: PebbleCollection
        :param bank: The PebbleCollection representing the bank's current pebbles.
        :type bank: PebbleCollection
        :return: True if the equation can be used for a trade, False otherwise.
        :rtype: bool
        """
        directional_equations = RuleBook.tradable_equation(equation, player_wallet, bank)
        result = equation in directional_equations
        return result

    @staticmethod
    def tradable_equation(
        equation: Equation, player_wallet: PebbleCollection, bank: PebbleCollection
    ) -> List[Equation]:
        """
        Generate a list of tradable directional equations by checking a equation both LHS -> RHS and RHS -> LHS.
        Also ensures the bank has enough pebbles to give to the player on the opposite side.

        :param equation: the equation the player wishes to use for exchange
        :data equation: Equation
        :param player_wallet: Dictionary of player's pebbles.
        :param bank: Dictionary of pebbles the bank has.
        :return: A list of directed Equation instances the player can use to trade.
        Each equation in the list can only be traded from left to right. (i.e. if the equation can be used either way,
        returned list will look like [LHS -> RHS, RHS -> LHS], while equation only usable from right to left will return
        [RHS -> LHS])
        :rtype: List[Equation]
        """
        usable_equations = []
        if RuleBook.__can_trade_equation_side(equation, True, player_wallet, bank):
            usable_equations.append(
                Equation(lhs=equation.lhs, rhs=equation.rhs, directed=True)
            )
        if RuleBook.__can_trade_equation_side(equation, False, player_wallet, bank):
            usable_equations.append(
                Equation(lhs=equation.rhs, rhs=equation.lhs, directed=True)
            )
        return usable_equations

    @staticmethod
    def __validate_equations(
        equations: list[Equation], wallet: PebbleCollection, bank: PebbleCollection
    ) -> Optional[Tuple[PebbleCollection, PebbleCollection]]:
        """
        check if a list of Equation can be performed in order with given bank and wallet at the beginning.

        :param equations: list of equation player request to exchange in this turn. Player request to draw a pebble if no equation
        :data equations: Equations
        :param wallet:player's wallet
        :data equations: PebbleCollection
        :param bank: bank state
        :data bank: PebbleCollection
        :return: None if exchange sequence is invalid, player wallet and bank after applying exchanges if valid.
        :rtype: Optional[Tuple[PebbleCollection, PebbleCollection]]
        """
        current_wallet = copy(wallet)
        current_bank = copy(bank)
        for eq in equations:
            if not RuleBook.can_trade_equation(eq, current_wallet, current_bank):
                return None
            current_wallet, current_bank = eq.trade_equation(
                current_wallet, current_bank
            )
        return current_wallet, current_bank

    @staticmethod
    def validate_exchange_request(
        turn_state: TurnState, rules: List[Equation], equations: Equations
    ) -> Optional[Tuple[PebbleCollection, PebbleCollection]]:
        """
        Validate the exchange request from player in this turn of the game. Return true if
        the exchange can be performed, false otherwise.

        :param turn_state: current turn state
        :type turn_state: TurnState
        :param rules: list of equation player request to exchange in this turn. Player request to draw a pebble if no equation
        :type rules: List[Equation]
        :param equations: list of equations available to players in the game
        :type equations: Equations
        :return: None if exchange sequence is invalid, player wallet and bank after applying exchanges if valid.
        :rtype: Optional[Tuple[PebbleCollection, PebbleCollection]]
        """
        current_bank = copy(turn_state.bank)
        active_player_wallet = copy(turn_state.active_player_wallet)
        if len(rules) == 0:
            return active_player_wallet, current_bank
        if len(rules) > MAX_EXCHANGE_DEPTH:
            return None
        if not all([rule in equations.equations for rule in rules]):
            return None
        return RuleBook.__validate_equations(rules, active_player_wallet, current_bank)

    @staticmethod
    def can_purchase_card(card, player_wallet: PebbleCollection) -> bool:
        """
        Checks whether the given player wallet has enough pebbles to buy the given card.

        :param card: the card the player intends to purchase
        :type card: Card
        :param player_wallet: the player wallet to check against
        :type player_wallet: PebbleCollection
        :returns: True if the card can be purchased, False otherwise
        """
        return card.pebbles.subset_of(player_wallet)

    @staticmethod
    def __validate_cards(
        purchase_sequence: Cards,
        visible_cards: Cards,
        wallet: PebbleCollection,
        bank: PebbleCollection,
    ) -> Optional[Tuple[PebbleCollection, PebbleCollection]]:
        """
        Check if a list of cards can be purchased in order with the given bank and wallet.

        :param purchase_sequence: PurchaseSequence containing a list of cards player requested to purchase in this turn.
        Player requests to skip purchasing if it is empty.
        :type purchase_sequence: Cards
        :param visible_cards: Cards visible to the active player
        :type visible_cards: Cards
        :param wallet: player's wallet
        :type wallet: PebbleCollection
        :param bank: bank state
        :type bank: PebbleCollection
        :return: None if cards cannot be purchased, player's wallet and bank after purchases otherwise
        :rtype: Optional[Tuple[PebbleCollection, PebbleCollection]]
        """
        current_wallet = wallet
        current_bank = bank
        for card in purchase_sequence.cards:
            if (
                not RuleBook.can_purchase_card(card, current_wallet)
                or not card in visible_cards.cards
            ):
                return None
            current_wallet, current_bank = card.purchase(current_wallet, current_bank)
        return current_wallet, current_bank

    @staticmethod
    def valid_purchase_request(
        turn_state: TurnState, purchase_sequence: Cards
    ) -> Optional[Tuple[PebbleCollection, PebbleCollection]]:
        """
         Validate the purchase request from the active player.

        :param turn_state: current turn state
        :type turn_state: TurnState
        :param cards: list of cards player request to exchange in this turn
        :type cards: Cards
        :return: None if the purchase request is invalid, player wallet and bank after purchases otherwise
        :rtype: Optional[Tuple[PebbleCollection, PebbleCollection]]
        """

        current_bank = turn_state.bank
        active_player_wallet = turn_state.active_player_wallet
        visible_cards = turn_state.cards
        if purchase_sequence.is_empty():
            return active_player_wallet, current_bank
        return RuleBook.__validate_cards(
            purchase_sequence, visible_cards, active_player_wallet, current_bank
        )

    @staticmethod
    def valid_draw_pebble_request(
        turn_state: TurnState,
    ) -> Optional[Tuple[PebbleCollection, PebbleCollection]]:
        """
         Validate a draw pebble request from the active player. Return None if the bank is empty.
         Return updated bank and wallet if possible

        :param turn_state: current turn state
        :type turn_state: TurnState
        :return: None if the purchase request is invalid, player wallet and bank after purchases otherwise
        :rtype: Optional[Tuple[PebbleCollection, PebbleCollection]]
        """

        current_bank = turn_state.bank
        active_player_wallet = turn_state.active_player_wallet
        if not current_bank.pebbles:
            return None
        drawn_pebble = PebbleCollection(
            pebbles=tuple([RuleBook.draw_bank_pebble(current_bank)])
        )
        return (active_player_wallet + drawn_pebble, current_bank - drawn_pebble)

    @staticmethod
    def score_if_bought(card: Card, player_wallet: PebbleCollection) -> int:
        """
        Returns the number of points this card would add to the player's score if bought.

        :param card: card to be purchased
        :data card: Card
        :param player_wallet: the player wallet to check against, as a PebbleCollection instance
        :type player_wallet: PebbleCollection

        :returns: number of points this card would add to the player's score if bought
        :rtype: int
        """

        if not RuleBook.can_purchase_card(card, player_wallet):
            return 0

        remaining_wallet = player_wallet - card.pebbles
        remaining_pebbles = len(remaining_wallet.pebbles)
        remaining_pebbles = 3 if remaining_pebbles > 3 else remaining_pebbles

        return CARD_REWARDS.get((remaining_pebbles, card.happy_face), 0)

    @staticmethod
    def draw_bank_pebble(bank: PebbleCollection) -> Optional[Pebble]:
        """
        Draws a pebble from the given bank in a deterministic manner.

        :param bank: bank available to players to draw the pebble from
        :type bank: PebbleCollection
        :return: Pebble from the bank, None if no more pebbles are available to draw.
        :rtype: Optional[Pebble]
        """
        return bank.draw_pebble()

    @staticmethod
    def is_game_over(game_state) -> bool:
        """Is the current game over?"""
        # All players have been kicked
        if not game_state.players:
            return True

        # A player has 20 points at the end of its turn
        if game_state.players[-1].score >= WIN_SCORE:
            return True

        # No more cards available for purchase
        if game_state.visibles.is_empty():
            return True

        # The bank is empty and no player can buy a card.
        if game_state.is_bank_empty() and not game_state.can_any_player_buy_any_card():
            return True

        return False

    @staticmethod
    def get_highest_score(game_state) -> list["PlayerState"]:
        """ "
        get a list of players with the  highest score. return empty list if there is no player

        :param game_state: current game state
        :type game_state:GameState
        """
        if not game_state.players or len(game_state.players) == 0:
            return []
        players = game_state.players
        highest_score = max(player.score for player in players)
        return [player for player in players if player.score == highest_score]

    @staticmethod
    def usa_bonus(game_state):
        if not game_state.players or len(game_state.players) == 0:
            return game_state
        players = game_state.players
        for player in players:
            if RuleBook.can_give_usa(player.cards):
                player.score += 10

    @staticmethod
    def can_give_usa(cards) -> bool:
        for card in cards:
            rep = card.__str__()
            if "red" in rep and "blue" in rep and "white" in rep:
                return True
        return False

    @staticmethod
    def sey_bonus(game_state):
        if not game_state.players or len(game_state.players) == 0:
            return game_state
        players = game_state.players
        for player in players:
            if RuleBook.can_give_sey(player.cards):
                player.score += 50
    @staticmethod
    def can_give_sey(cards):
        for card in cards:
            rep = card.__str__()
            if "white" in rep and "blue" in rep and "yellow" in rep and "red" in rep and "green" in rep:
                return True
        return False


