The commit we tagged for your submission is 9cf7960400220edf0e8eb23e27cb3de18b4152a.
**If you use GitHub permalinks, they must refer to this commit or your self-eval will be rejected.**
Navigate to the URL below to create permalinks and check that the commit hash in the final permalink URL is correct:

https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/tree/9cf7960400220edf0e8eb23e27cb3de18b4152a

## Self-Evaluation Form for Milestone 6

Indicate below each bullet which piece of your code takes care of each task:

1. the five pieces of player functionality
- name: implemented as an id field in PlayerState class, as opposed to mechanism https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/9cf7960400220edf0e8eb23e27cb3de18b4152a4/Bazaar/Referee/player_state.py#L13
- setup: https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/9cf7960400220edf0e8eb23e27cb3de18b4152a4/Bazaar/Player/mechanism.py#L18-L26
- request pebble or trades: https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/9cf7960400220edf0e8eb23e27cb3de18b4152a4/Bazaar/Player/mechanism.py#L28-L40
- request cards: https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/9cf7960400220edf0e8eb23e27cb3de18b4152a4/Bazaar/Player/mechanism.py#L42-L51
- win: https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/9cf7960400220edf0e8eb23e27cb3de18b4152a4/Bazaar/Player/mechanism.py#L53-L60
2. `setting up players` functionality in the referee component 
<br> The referee sets up players in 
https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/9cf7960400220edf0e8eb23e27cb3de18b4152a4/Bazaar/Referee/referee.py#L106-L118
<br> , which is called when the referee sets up the game using  __create_game_state
https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/9cf7960400220edf0e8eb23e27cb3de18b4152a4/Bazaar/Referee/referee.py#L143-L163

3. `running a game with just players` functionality in the referee component
   <br>There is a bug in the parameters typing, the game_state return type None should be the default value  of game_state, and this function returns a tuple of two lists of players:
   https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/9cf7960400220edf0e8eb23e27cb3de18b4152a4/Bazaar/Referee/referee.py#L424-L447
   
   because the code does anticipate the  game_state to be none when setting up the initial state. When no game state is given, it initializes a game state:
   <br> https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/9cf7960400220edf0e8eb23e27cb3de18b4152a4/Bazaar/Referee/referee.py#L120-L140


4. `running a game with players and a game state` functionality in the referee component
   <br> https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/9cf7960400220edf0e8eb23e27cb3de18b4152a4/Bazaar/Referee/referee.py#L424-L447
   <br> When setting up the initial state is called, if there is a game state passing in, it sets up the game state directly
https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/9cf7960400220edf0e8eb23e27cb3de18b4152a4/Bazaar/Referee/referee.py#L120-L140



5. `managing an individual turn` functionality in the referee component, which involves two calls to the active player
  <br><br> The referee managed an individual turn by handling the transition from exchange state to purchase state by calling handle(), a function handle transition between states.
<br> When the state is an exchange state, it asks the player for an exchange request and transit to the purchase state based on the result of the legality check.
<br> When the state is a purchase state, it asks the player for a purchase request and transits back to the exchange state based on the result of the legality check. When a purchase_state transits back to the exchange state, a turn is finished.   <br> The cycling will stop when a state transit to Overstate.
https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/9cf7960400220edf0e8eb23e27cb3de18b4152a4/Bazaar/Referee/referee.py#L441-L443

  <br> Handle() in ExchangeState:
https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/9cf7960400220edf0e8eb23e27cb3de18b4152a4/Bazaar/Referee/referee.py#L179-L194
   advance to PurchaseState if the game is not over and actions are legal:
https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/9cf7960400220edf0e8eb23e27cb3de18b4152a4/Bazaar/Referee/referee.py#L259-L301
<br> Handle() in PurchaseState:
https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/9cf7960400220edf0e8eb23e27cb3de18b4152a4/Bazaar/Referee/referee.py#L304-L315
advance to ExchangeState when a new active player if the game is not over and actions are legal:
https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/9cf7960400220edf0e8eb23e27cb3de18b4152a4/Bazaar/Referee/referee.py#L368-L411
   

6. `informing survivors of the outcome` functionality in thea referee component
<br> Informing remaining players the update about the game after a player's action during the turn:
https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/9cf7960400220edf0e8eb23e27cb3de18b4152a4/Bazaar/Referee/referee.py#L49-L78
<br> Informing remaining players the result of the game when game is over:
https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/9cf7960400220edf0e8eb23e27cb3de18b4152a4/Bazaar/Referee/referee.py#L445-L447


8. unit tests for the `referee`:

   - five distinct unit tests for the overall `referee` functionality, or
   - unit tests for the abvove pieces of functionality
<br> The code does not have unit test for each functionalities.
<br> It has  unit tests for small cases that runs the entire game, thus testing the above functionalities:
<br> Testing the referee's ability to ask the player for one purchase and ending the game (no exchange just purchase):
   https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/9cf7960400220edf0e8eb23e27cb3de18b4152a4/Bazaar/Referee/test_referee.py#L118-L153
<br> Testing the referee's ability to run the 5 turns and end the game (drawing pebbles five times):
   https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/9cf7960400220edf0e8eb23e27cb3de18b4152a4/Bazaar/Referee/test_referee.py#L155-L177
<br> Testing the referee's ability to kick a player when an unexpected error happens: 
https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/9cf7960400220edf0e8eb23e27cb3de18b4152a4/Bazaar/Referee/test_referee.py#L178-L201
<br> Testing the referee's ability to kick a misbehave player:
https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/9cf7960400220edf0e8eb23e27cb3de18b4152a4/Bazaar/Referee/test_referee.py#L203-L226
<br> Testing the referee's ability to run turns and output correct winner:
https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/9cf7960400220edf0e8eb23e27cb3de18b4152a4/Bazaar/Referee/test_referee.py#L227-L267



   
9. the explanation in the referee component of what is considered ill-behaved player and how the referee deals with it.
https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/9cf7960400220edf0e8eb23e27cb3de18b4152a4/Bazaar/Referee/referee.py#L18-L24


The ideal feedback for each of these points is a GitHub perma-link to
the range of lines in a specific file or a collection of files.

A lesser alternative is to specify paths to files and, if files are
longer than a laptop screen, positions within files are appropriate
responses.

You may wish to add a sentence that explains how you think the
specified code snippets answer the request.

If you failed to do any of the above points, say so.


