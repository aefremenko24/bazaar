"""
NOTE: For all rendering functions below,
increasing x_pos moves from left to right on the screen,
increasing y_pos moves from top to bottom.
"""
import math
import os
from collections import Counter, deque

import pygame

from Bazaar.Common.rule_book import RuleBook

pygame.init()
from typing import List, Dict, Tuple

__ROOT_DIR__ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from Bazaar.Common.turn_state import TurnState
from Bazaar.Referee.game_state import GameState
from Bazaar.Common.pebble import Pebble, PebbleColor, PebbleCollection
from Bazaar.Common.cards import Card, Cards
from Bazaar.Common.equations import Equation, Equations
from Bazaar.Referee.player_state import PlayerState


SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 900
__PENTAGON_POINTS__ = [(138, 108), (96, 176), (29, 150), (29, 65), (96, 39)]
__PLAYER_RENDER_WIDTH__ = 200
__PLAYER_RENDER_HEIGHT__ = 200
__BANK_RENDER_WIDTH__ = 300
__CARD_WIDTH__ = 200
__CARD_HEIGHT__ = 300
__EQUATION_HEIGHT__ = 60
__EQUATION_ITEM_WIDTH__ = 60
__MARGIN__ = 10
__FONT_SIZE_LARGE__ = 40
__FONT_SIZE_SMALL__ = 20
__FONT_LARGE__ = pygame.font.SysFont("comicsansms", __FONT_SIZE_LARGE__)
__FONT_SMALL__ = pygame.font.SysFont("comicsansms", __FONT_SIZE_SMALL__)
__RED_PEBBLE__ = pygame.image.load(__ROOT_DIR__ + "/Other/Resources/pebble_red.png")
__BLUE_PEBBLE__ = pygame.image.load(__ROOT_DIR__ + "/Other/Resources/pebble_blue.png")
__GREEN_PEBBLE__ = pygame.image.load(__ROOT_DIR__ + "/Other/Resources/pebble_green.png")
__WHITE_PEBBLE__ = pygame.image.load(__ROOT_DIR__ + "/Other/Resources/pebble_white.png")
__YELLOW_PEBBLE__ = pygame.image.load(
    __ROOT_DIR__ + "/Other/Resources/pebble_yellow.png"
)
__CARD_WITH_FACE__ = pygame.image.load(
    __ROOT_DIR__ + "/Other/Resources/empty_card_w_face.png"
)
__CARD_NO_FACE__ = pygame.image.load(
    __ROOT_DIR__ + "/Other/Resources/empty_card_no_face.png"
)
__EQUAL_SIGN__ = __FONT_LARGE__.render("=", True, (0, 0, 0))

__PEBBLE_IMAGES__ = {
    PebbleColor.RED.value: __RED_PEBBLE__,
    PebbleColor.WHITE.value: __WHITE_PEBBLE__,
    PebbleColor.BLUE.value: __BLUE_PEBBLE__,
    PebbleColor.GREEN.value: __GREEN_PEBBLE__,
    PebbleColor.YELLOW.value: __YELLOW_PEBBLE__,
}

def render_pebble_collection(
    screen: pygame.display, pebbles: PebbleCollection, x_pos: int, y_pos: int
) -> None:
    """
    Given a dictionary of pebbles, renders them on the screen, each color below the previous.
    Number of pebbles for each color is specified to the right of each row.

    :param screen: screen for the pebbles to be drawn on
    :param pebbles: dictionary of pebbles to be rendered, where keys are colors and values are quantities
    :param x_pos: x-position of the top left corner of the pebble image
    :param y_pos: y-position of the top left corner of the pebble image
    """
    pebbles_as_dict = {color : 0 for color in PebbleColor} if not pebbles.pebbles else Counter(pebbles.pebbles)
    max_pebbles = max(pebbles_as_dict.values())
    for pebble_column_index, pebble in enumerate(pebbles_as_dict.keys()):
        for pebble_number in range(pebbles_as_dict[pebble]):
            render_pebble(
                screen,
                pebble.color,
                x_pos + pebble_number * __MARGIN__,
                y_pos + pebble_column_index * (__MARGIN__ * 2),
            )
        render_text(
            screen,
            str(pebbles_as_dict[pebble]),
            __FONT_SMALL__,
            x_pos + (max_pebbles + 4) * __MARGIN__,
            y_pos + pebble_column_index * (__MARGIN__ * 2),
        )

def render_pebble(screen: pygame.display, color: str, x_pos: int, y_pos: int) -> None:
    """
    Renders a pebble image of the specified color at the given position on the screen.

    :param color: String representing color of the Pebble to be rendered
    :param screen: screen for the pebble to be drawn on
    :param x_pos: x-position of the top left corner of the pebble image to be drawn on the screen
    :param y_pos: y-position of the top left corner of the pebble image to be drawn on the screen
    """
    return screen.blit(__PEBBLE_IMAGES__[color], (x_pos, y_pos))


def render_text(
    screen: pygame.Surface, text: str, font: pygame.font = __FONT_LARGE__, x_pos: int = 0, y_pos: int = 0
):
    """
    Renders lines of text on the screen, left-aligned.

    :param screen: screen for the text to be rendered on
    :param text: string of text to be rendered, separated by \n if needed
    :param font: pygame font parameter specifying the formatting of the text
    :param x_pos: x-position of the top left corner of the text
    :param y_pos: y-position of the top left corner of the text
    """
    height = font.get_height()
    lines = text.split("\n")
    for line_index, line in enumerate(lines):
        txt_surface = font.render(line, True, (0, 0, 0))
        screen.blit(txt_surface, (x_pos, y_pos + (line_index * height)))


def render_card(card: Card, screen: pygame.display, x_pos: int, y_pos: int):
    """
    Renders the card and its pebbles on the given screen at the specified position.
    (x increases from left to right, y increases from top to bottom).

    :param card: Card instance to be rendered
    :param screen: screen to draw the card on
    :param x_pos: x-position of the top left corner of the card to be drawn on the screen
    :param y_pos: y-position of the top left corner of the card to be drawn on the screen
    """
    card_image = __CARD_WITH_FACE__ if card.happy_face else __CARD_NO_FACE__
    screen.blit(card_image, (x_pos, y_pos))
    for pebble_index in range(len(card.pebbles.pebbles)):
        pebble_color = card.pebbles.pebbles[pebble_index].color
        (x_position, y_position) = __PENTAGON_POINTS__[pebble_index]
        x_position += x_pos
        y_position += y_pos

        render_pebble(screen, pebble_color, x_position, y_position)


def render_cards(screen: pygame.display, cards: Cards, x_pos: int, y_pos: int):
    """
    Renders a stack of cards laid on top of each other, each shifted by a margin to the right from the previous.
    (x increases from left to right, y increases from top to bottom).

    :param screen: screen to render the card on
    :param cards: list of cards to render
    :param x_pos: x-position of the top left corner of the first to be drawn on the screen
    :param y_pos: y-position of the top left corner of the first to be drawn on the screen
    """
    for card_index, card in enumerate(cards.cards):
        render_card(card, screen, x_pos + card_index % 2 * __CARD_WIDTH__,
                    y_pos + math.floor(card_index / 2) * __CARD_HEIGHT__)


def render_equation(equation: Equation, screen: pygame.display, x_pos: int, y_pos: int):
    """
    Renders the equation on the given screen at the specified position.
    (x increases from left to right, y increases from top to bottom).

    :param equation: Equation instance to be rendered
    :param screen: screen for the equation to be drawn on
    :param x_pos: x-position of the top left corner of the equation to be drawn on the screen
    :param y_pos: y-position of the top left corner of the equation to be drawn on the screen
    """
    number_equation_items = len(equation.lhs.pebbles) + len(equation.rhs.pebbles) + 1
    render_equation_box(screen, x_pos, y_pos, number_equation_items)

    (eq_sign_x_position, eq_sign_y_position) = (
        x_pos + len(equation.lhs.pebbles) * __EQUATION_ITEM_WIDTH__ + __MARGIN__,
        y_pos,
    )

    render_left_side(equation, screen, x_pos, y_pos)

    screen.blit(__EQUAL_SIGN__, (eq_sign_x_position, eq_sign_y_position))

    render_right_side(equation, screen, eq_sign_x_position, y_pos)


def render_equation_box(screen: pygame.display, x_pos: int, y_pos: int, num_items: int):
    """
    Renders the grey equation background box on the given screen at the specified position.
    (x increases from left to right, y increases from top to bottom).

    :param screen: screen for the box to be drawn on
    :param x_pos: x-position of the top left corner of the box to be drawn on the screen
    :param y_pos: y-position of the top left corner of the box to be drawn on the screen
    :param num_items: number of items of the equation, will affect the width
    """
    total_equation_width = num_items * __EQUATION_ITEM_WIDTH__

    pygame.draw.rect(
        screen,
        (240, 240, 240),
        (x_pos, y_pos, total_equation_width, __EQUATION_HEIGHT__),
    )
    pygame.draw.rect(
        screen,
        (180, 180, 180),
        (x_pos, y_pos, total_equation_width, __EQUATION_HEIGHT__),
        3,
    )


def render_left_side(
    equation: Equation, screen: pygame.display, x_pos: int, y_pos: int
):
    """
    Renders the left side of the equation on the given screen at the specified position.
    (x increases from left to right, y increases from top to bottom).

    :param screen: screen for the left side to be drawn on
    :param x_pos: x-position of the top left corner of the side to be drawn on the screen
    :param y_pos: y-position of the top left corner of the side to be drawn on the screen
    """
    for pebble_index in range(len(equation.lhs.pebbles)):
        pebble_x_pos = x_pos + pebble_index * __EQUATION_ITEM_WIDTH__ + __MARGIN__
        pebble_y_pos = y_pos + __MARGIN__
        render_pebble(
            screen, equation.lhs.pebbles[pebble_index].color, pebble_x_pos, pebble_y_pos
        )


def render_right_side(
    equation: Equation, screen: pygame.display, eq_sign_x_position: int, y_pos: int
):
    """
    Renders the right side of the equation on the given screen at the specified position.
    (x increases from left to right, y increases from top to bottom).

    :param screen: screen for the right side to be drawn on
    :param eq_sign_x_position: x-position of the top left corner of the equal sign blit on the screen
    :param y_pos: y-position of the top left corner of the side to be drawn on the screen
    """
    for pebble_index in range(len(equation.rhs.pebbles)):
        pebble_x_pos = (
            eq_sign_x_position
            + __EQUATION_ITEM_WIDTH__
            + (pebble_index * __EQUATION_ITEM_WIDTH__)
        )
        pebble_y_pos = y_pos + __MARGIN__
        render_pebble(
            screen, equation.rhs.pebbles[pebble_index].color, pebble_x_pos, pebble_y_pos
        )


def render_equation_table(
    screen: pygame.display, equations: Equations, x_pos: int, y_pos: int
):
    """
    Renders a table of equations on the screen starting from the given position.
    Equations are rendered vertically, each consecutive one goes below the previous.
    (x increases from left to right, y increases from top to bottom).

    :param screen: screen for the equations to be drawn on
    :param equations: list of equations to be rendered
    :param x_pos: x-position of the top left corner of the table to be drawn on the screen
    :param y_pos: y-position of the top left corner of the table to be drawn on the screen
    """
    for equation_index in range(len(equations.equations)):
        eq_x_pos = x_pos + __MARGIN__
        eq_y_pos = y_pos + equation_index * __EQUATION_HEIGHT__ + __MARGIN__
        render_equation(equations.equations[equation_index], screen, eq_x_pos, eq_y_pos)


def render_player(
    player: PlayerState, screen: pygame.display, x_pos: int, y_pos: int
) -> None:
    """
    Renders the Player's info on the screen. Info includes: username, pebbles, and score.

    :param screen: Pygame screen to render the Player info on
    :param x_pos: x-position of the top left corner of the Player's username
    :param y_pos: y-position of the top left corner of the Player's username
    """
    render_text(screen, player.actor.name, __FONT_LARGE__, x_pos, y_pos)
    render_text(
        screen,
        f"Score: {player.score}",
        __FONT_SMALL__,
        x_pos,
        y_pos + __FONT_SIZE_LARGE__ + __MARGIN__,
    )

    render_pebble_collection(
        screen, player.wallet, x_pos, y_pos + __FONT_SIZE_LARGE__ * 2
    )


def render_player_list(
    players: deque[PlayerState], screen: pygame.display, x_pos: int, y_pos: int
):
    """
    Renders the list of players horizontally one to the right of the previous, starting at the given position.
    (x increases from left to right, y increases from top to bottom).

    :param screen: screen to render the players on
    :param x_pos: x-coordinate of the top left corner of the first player's username
    :param y_pos: y-coordinate of the top left corner of the first player's username
    """
    for player_index, player in enumerate(players):
        render_player(
            player, screen, x_pos + player_index * __PLAYER_RENDER_WIDTH__ + __MARGIN__, y_pos
        )


def render_game_state(
    game_state: GameState, screen: pygame.Surface, x_pos: int = 0, y_pos: int = 0, index: int = None
):
    """
    Renders the state of the game with the following elements: players, bank, equations, and cards.
    (x increases from left to right, y increases from top to bottom).

    :param screen: screen to render the game state on
    :param x_pos: x-coordinate of the top left corner of the first player's username
    :param y_pos: y-coordinate of the top left corner of the first player's username
    """
    if RuleBook.is_game_over(game_state):
        render_text(screen, "GAME OVER", __FONT_LARGE__, int(700), int(10))

    render_player_list(game_state.players, screen, x_pos, y_pos)

    render_text(
        screen,
        "Bank",
        __FONT_LARGE__,
        x_pos + len(game_state.players) * __PLAYER_RENDER_WIDTH__,
        y_pos + __MARGIN__,
    )

    render_pebble_collection(
        screen,
        game_state.bank,
        x_pos + len(game_state.players) * __PLAYER_RENDER_WIDTH__,
        y_pos + __FONT_SIZE_LARGE__ * 2,
    )

    render_text(
        screen, "Cards", __FONT_LARGE__, x_pos, y_pos + __PLAYER_RENDER_HEIGHT__
    )

    render_cards(
        screen,
        game_state.visibles,
        x_pos,
        y_pos + __PLAYER_RENDER_HEIGHT__ + __FONT_SIZE_LARGE__ + __MARGIN__,
    )

    render_text(
        screen,
        "Equations",
        __FONT_LARGE__,
        x_pos + __CARD_WIDTH__ * 2,
        y_pos + __PLAYER_RENDER_HEIGHT__,
    )

    render_equation_table(
        screen,
        game_state.equations,
        x_pos + __CARD_WIDTH__ * 2,
        y_pos + __PLAYER_RENDER_HEIGHT__ + __FONT_SIZE_LARGE__,
    )

    if index:
        render_text(screen, str(index), __FONT_SMALL__, x_pos, y_pos)


def render_other_players_scores(
    turn_state: TurnState, screen: pygame.display, x_pos: int, y_pos: int
) -> None:
    """
    Renders scores of other active players in the game vertically one below the previous.

    :param screen: screen to render the Players on
    :param x_pos: x-position of the top left corner of the first Player's username
    :param y_pos: y-position of the top left corner of the first Player's username
    """
    render_text(screen, "Player Scores", __FONT_LARGE__, x_pos, y_pos)
    y_offset = y_pos + __FONT_SIZE_LARGE__ + __MARGIN__
    for score_index, score in enumerate(turn_state.player_scores):
        score_text = f"Player {score_index}: {score}"
        render_text(screen, score_text, __FONT_LARGE__, x_pos, y_offset)
        y_offset += __FONT_SIZE_LARGE__ + __MARGIN__


def render_turn_state(
    turn_state: TurnState, screen: pygame.display, x_pos: int, y_pos: int
) -> None:
    """
    Renders the state of the Player's turn with the following elements: bank, equations, and other player's scores.

    :param screen: screen to render the turn state on
    :param x_pos: x-coordinate of the top left corner of the given Player's username
    :param y_pos: y-coordinate of the top left corner of the given Player's username
    """
    if turn_state.player.in_game:
        render_player(turn_state.player, screen, x_pos, y_pos)
    else:
        render_text(
            screen,
            "You are\nout of\nthe game!",
            __FONT_LARGE__,
            x_pos,
            y_pos + __MARGIN__,
        )

    render_text(
        screen,
        "Bank",
        __FONT_LARGE__,
        x_pos + __PLAYER_RENDER_WIDTH__,
        y_pos + __MARGIN__,
    )

    render_pebble_collection(
        screen,
        turn_state.bank,
        x_pos + __PLAYER_RENDER_WIDTH__,
        y_pos + __FONT_SIZE_LARGE__ * 2,
    )

    render_text(
        screen,
        "Equations",
        __FONT_LARGE__,
        x_pos + __PLAYER_RENDER_WIDTH__ + __BANK_RENDER_WIDTH__,
        y_pos,
    )

    render_equation_table(
        screen,
        turn_state.equations,
        x_pos + __PLAYER_RENDER_WIDTH__ + __BANK_RENDER_WIDTH__,
        y_pos + __FONT_SIZE_LARGE__,
    )

    render_other_players_scores(
        turn_state, screen, x_pos, y_pos + __PLAYER_RENDER_HEIGHT__ + __MARGIN__
    )

def filename_popup(screen):
    """
    Creates a window to allow user text input for saving a gamestate to a file.

    :param screen: screen to render the Pop up window.
    """
    font = pygame.font.Font(None, 36)
    popup_width = 400
    popup_height = 200
    px = (SCREEN_WIDTH - popup_width) // 2
    py = (SCREEN_HEIGHT - popup_height) // 2
    input_box = pygame.Rect(px, py, popup_width, 50)  # Input box dimensions
    submit_button = pygame.Rect(px, py + 70, 100, 40)  # Submit button dimensions
    color_active = pygame.Color('white')
    color_inactive = pygame.Color('red')
    button_color = pygame.Color('red')
    button_text_color = pygame.Color('white')
    color = color_inactive
    active = False
    text = ''
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
                if submit_button.collidepoint(event.pos):
                    return text
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((54, 69, 79))
        txt_surface = font.render(text, True, color)
        width = max(300, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.draw.rect(screen, button_color, submit_button)
        button_text = font.render("Save", True, button_text_color)
        screen.blit(button_text, (submit_button.x + 10, submit_button.y + 5))
        pygame.display.flip()
