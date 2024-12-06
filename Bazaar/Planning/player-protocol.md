# Player Interface

**TO**: Matthias Felleisen

**FROM**: Arthur, Ezri

**CC**: CS4500 TAs

**DATE**: October 10, 2024

**SUBJECT**: Player Protocol Planning

For the player components to interact with the referee, there need to be functions and methods invoked in a specific order — that being the protocol by which the game is ran. For the system to be complete, both the referee and the players need a set of functions they can use. We have identifies the following communication functions/methods to be needed for the game to run.

The player components should be able to call:

- send_player_action() - sends a game action to the referee (i.e. trading a card, using an equation, or requesting a pebble)
- quit_game() - can be called by any player at any time, if they would like to quit the game

The referee should be able to call:

- inform_start_game() - informs the players that the game has started, sends the equations generated to the players
- next_turn() - called by when the active player is done with their turn or at the beginning of the game, sends the new turn state to the next active player
- update_player_info() - informs the player that just took the turn about their updated information (wallet, score) after their actions
- feedback() - sends a message to the player (i.e. last action was accepted/not accepted)
- inform_game_over() - informs the players that the game is over and announces the winner
- kick_player() - informs a player that they've been kicked

The order we imagine these will be called throughout the game:
1. inform_start_game() - starting point of the game
2. next_turn() - inform the first player it's their turn
3. send_player_action() - ran as many times as the player needs to complete their turn, then "done" action is sent
4. update_player_info() - referee updates the player's info after the turn, sends it over
5. feedback() - referee sends over any feedback on the action player toook
6. next_turn() - pass the turn to the next player
7. inform_game_over() - when conditions are met, the game is done

Here, steps 2-6 repeat for every player until the game is done. kick_player() and quit_game() can be called at any time during the game.