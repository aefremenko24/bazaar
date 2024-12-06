from collections import deque

from Bazaar.Common.cards import Cards
from Bazaar.Common.equations import Equations
from Bazaar.Common.pebble import PebbleColor, Pebble
from Bazaar.Common.render import render_player
import pygame

from Bazaar.Player.mechanism import Mechanism
from Bazaar.Referee.player_state import PlayerState
from render import (
    __MARGIN__,
    render_equation,
    render_card,
    render_equation_table,
    render_game_state,
    render_turn_state,
)
import random
from Bazaar.Referee.game_state import GameState
import unittest

def test_render_card():
    cards = Cards.generate_random(5)
    for card in cards.cards:
        screen = pygame.display.set_mode((220, 320))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((255, 255, 255))
            render_card(card, screen, __MARGIN__, __MARGIN__)
            pygame.display.flip()

    assert True


def test_render_equations():
    equations1 = Equations.generate_random(10)
    equations2 = Equations.generate_random(10)
    for equation_table in (equations1, equations2):
        screen = pygame.display.set_mode((600, 750))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((255, 255, 255))
            render_equation_table(screen, equation_table, __MARGIN__, __MARGIN__)
            pygame.display.flip()

    assert True


def test_render_player():
    player1 = PlayerState()
    player2 = PlayerState()
    player3 = PlayerState()
    players = [player1, player2, player3]
    player_names = ["ultimate", "penguins", "team"]
    actor1 = Mechanism(name=player_names[0], policy="purchase-points")
    actor2 = Mechanism(name=player_names[1], policy="purchase-points")
    actor3 = Mechanism(name=player_names[2], policy="purchase-points")

    player1.actor = actor1
    player2.actor = actor2
    player3.actor = actor3

    for player_index, player in enumerate(players):
        for _ in range(random.randint(1, 5)):
            player.wallet.add_pebble(Pebble(color=PebbleColor.WHITE))
        for _ in range(random.randint(1, 5)):
            player.wallet.add_pebble(Pebble(color=PebbleColor.RED))
        for _ in range(random.randint(1, 5)):
            player.wallet.add_pebble(Pebble(color=PebbleColor.GREEN))
        for _ in range(random.randint(1, 5)):
            player.wallet.add_pebble(Pebble(color=PebbleColor.BLUE))
        for _ in range(random.randint(1, 5)):
            player.wallet.add_pebble(Pebble(color=PebbleColor.YELLOW))

    for player in (player1, player2, player3):
        screen = pygame.display.set_mode((200, 300))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((255, 255, 255))
            render_player(player, screen, __MARGIN__, __MARGIN__)
            pygame.display.flip()

    assert True


def test_render_game_state():
    player1 = PlayerState()
    player2 = PlayerState()
    player3 = PlayerState()
    players = [player1, player2, player3]
    player_names = ["ultimate", "penguins", "team"]
    actor1 = Mechanism(name=player_names[0], policy="purchase-points")
    actor2 = Mechanism(name=player_names[1], policy="purchase-points")
    actor3 = Mechanism(name=player_names[2], policy="purchase-points")

    player1.actor = actor1
    player2.actor = actor2
    player3.actor = actor3

    for player_index, player in enumerate(players):
        for _ in range(random.randint(1, 5)):
            player.wallet.add_pebble(Pebble(color=PebbleColor.WHITE))
        for _ in range(random.randint(1, 5)):
            player.wallet.add_pebble(Pebble(color=PebbleColor.RED))
        for _ in range(random.randint(1, 5)):
            player.wallet.add_pebble(Pebble(color=PebbleColor.GREEN))
        for _ in range(random.randint(1, 5)):
            player.wallet.add_pebble(Pebble(color=PebbleColor.BLUE))
        for _ in range(random.randint(1, 5)):
            player.wallet.add_pebble(Pebble(color=PebbleColor.YELLOW))

    game_state = GameState(invisible_deck=Cards.generate_random(16), visibles=Cards.generate_random(4), players=deque(players))

    screen = pygame.display.set_mode((1500, 900))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        render_game_state(game_state, screen, 50, 20)
        pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    # test_render_equations()
    # test_render_card()
    # test_render_player()
    test_render_game_state()
    pygame.quit()
