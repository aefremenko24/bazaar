# Game Observer

**TO**: Matthias Felleisen

**FROM**: Arthur, Ezri

**CC**: CS4500 TAs

**DATE**: October 24, 2024

**SUBJECT**: Game-Observer Mechanism Planning

Game observer is the mechanism that should allow dev-ops to observe the game of Bazaar happening from the referee's perspective. To accomplish this goal, the observer interface will have the following methods:
- void **update_state**(GameStateDelta game_state_delta)
- void **game_over**()

The **update_state** method will allow the observer to consume a game state delta and update its representation of the game state based on that. This method will be called by the referee at the end of each turn, before it takes away the turn from the current player and passes it to the next player. It will also be called after the player's intermediate steps, such as trading or purchasing. When the observer receives the delta, it will compute the new game state based on the changes made and reassign its game_state field. It is also important to note that it will not be the job of the observer to check whether the delta of the game_state sent is valid according to the rule book. The observer must simply observe the game, while the referee should be the one checking for any rules broken while computing the delta (for example, sending negative change in score, etc.)

The **game_over** method will let the observer know that the game is over and that no more game states will be sent over. This method will be called by the referee before it destructs itself and ends the game. The referee will also call **update_state** right before calling **game_over** to share the last state that the game was in before it finished.  

The observer mechanism will use the information that the referee has shared with it to construct a visual representation of the game state. To do that, the observer will use pre-existing modules for rendering game state that we saw in milestone 2. 