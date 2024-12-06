# GameState  Interface and Referee-GameState protocol

**TO**: Matthias Felleisen

**FROM**: Arthur, Ezri

**CC**: CS4500 TAs

**DATE**: October 17, 2024

**SUBJECT**: Player Protocol Planning

The Gamestate Interface should have:<br>
- set_up(List[PlayerState]) -> Equations : this function set up the game and return
- get_turnstate(): extract the state of current turn 
- next_turn () : advanced to the next player in order
- is_game_over() -> bool:return if this game is over
- get_winner() ->List[PlayerState]

Referee-GameState protocol in order:
1. set_up(list[playerstate]) - from referee to game_state, set up the game and get equations
2. get_turnstate() -referee request turn_state from game state. The game state extracts and sends the current turn state to the referee.
3. update_gamestate(bank, wallet) - referee called this when exchange or purchases request has been verified. It update the gameState.
4. if(is_game_over()) - referee called this when a player is done playing the turn to check if game is over after this turn  
  True: get_winner()  - if game is over, get the winner from gamestate
  False:  next_turn() then retrun to step 2 - if game is not over. Advanced to next turn and repeat the step.



