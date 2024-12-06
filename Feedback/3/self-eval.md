 The commit we tagged for your submission is 77c0a80685db81d632af023a6a534c7d85da4271.
**If you use GitHub permalinks, they must refer to this commit or your self-eval will be rejected.**
Navigate to the URL below to create permalinks and check that the commit hash in the final permalink URL is correct:

https://github.khoury.northeastern.edu/CS4500-F24/ultimate-penguins/tree/77c0a80685db81d632af023a6a534c7d85da4271

## Self-Evaluation Form for Milestone 3

Indicate below each bullet which method takes care of each task:

0. the data representation for the referee's knowledge about the player,
   including its interpretation
   https://github.khoury.northeastern.edu/CS4500-F24/ultimate-penguins/blob/77c0a80685db81d632af023a6a534c7d85da4271/Bazaar/Referee/game_state.py#L23-L37
   - The Referee has a knowledge of the list of Players in the current game. Each Player has fields accessible by the Referee including username(str), score(int), pebbles(Dict[str, int], representing the Player's Wallet), active(Bool, representing player turn), in_game(Bool, representing if Player still in the game), and turn_state(TurnState). 

1. determining whether a game is over,
   its signature and purpose statement
   https://github.khoury.northeastern.edu/CS4500-F24/ultimate-penguins/blob/77c0a80685db81d632af023a6a534c7d85da4271/Bazaar/Referee/game_state.py#L79-L100
   - This function uses helper functions in the Game_State file, from line 39 to line 77, to check game end logic. 

2. extracting the turn state from the referee’s game state representation,
   its signature and purpose statement 
   https://github.khoury.northeastern.edu/CS4500-F24/ultimate-penguins/blob/77c0a80685db81d632af023a6a534c7d85da4271/Bazaar/Referee/game_state.py#L102-L122
   - This function extract appropriate information the Referee will send to the Player.
3. graphical rendering the referee’s game state
   its signature and purpose statement; and
   https://github.khoury.northeastern.edu/CS4500-F24/ultimate-penguins/blob/77c0a80685db81d632af023a6a534c7d85da4271/Bazaar/Common/render.py#L306-L358
   - This function renders each component in Game_State and combine them for display. 
4. graphical rendering the turn state data transmitted from the referee to the player,
   its signature and purpose statement. 
   https://github.khoury.northeastern.edu/CS4500-F24/ultimate-penguins/blob/77c0a80685db81d632af023a6a534c7d85da4271/Bazaar/Common/render.py#L379-L432
   - This function renders each component in Turn_State and combine them for display.
5. the unit tests for the "end of game" functionality. 
   https://github.khoury.northeastern.edu/CS4500-F24/ultimate-penguins/blob/77c0a80685db81d632af023a6a534c7d85da4271/Bazaar/Referee/test_game_state.py#L95-L122
   - This snippet tests the end of game functionality for our data model. Tests for helper methods are in the same file from line 55 to line 92.
     
The ideal feedback for each of these points is a GitHub perma-link to
the range of lines in a specific file or a collection of files.

A lesser alternative is to specify paths to files and, if files are
longer than a laptop screen, positions within files are appropriate
responses.

You may wish to add a sentence that explains how you think the
specified code snippets answer the request.

If you failed to do any of the above points, say so.

