# Player Interface

**TO**: Matthias Felleisen

**FROM**: Arthur Efremenko, Tony Lyu

**CC**: CS4500 TAs

**DATE**: September 30, 2024

**SUBJECT**: Player Interface Planning


The Player Interface will be used by both human and AI players, where the referee controls the game flow and validates player actions. The interface defines the basic functions a player must use to progress in the game and interact with the Referee.

### **Mutual Class Fields**:
- username(String): A unique player username string within the specific game where the player is initialized. 
- score(int): An Integer that represents the player's score. Restricted to natural numbers (0 or larger).
- pebbles(Dict(Pebble: int)): A dictionary representing the player's wallet, where keys are Pebble enums (color) and values are the quantity owned for each color.
- in_game(Bool): True if the player is still in game (not kicked), false otherwise.
- active(Bool): True if this player has the next turn. 
- turn_state(TurnState): TurnState class instance that provides player-specific game information from the Referee
  
### **Functions**:

- start_turn(): Called by the referee when this player should take the turn. Starts in-turn logic, and choose actions to perform.
- send_action(Dict(String: Dict)) -> Bool: Called by the player when they have decided on the action they want to take. The function sends the dictionary where the key is the action (i.e. "buy_card"") and the value is a dictionary with action arguments (i.e. which card to buy)
  - List of possible actions to be sent:
  - "draw_pebble": ask referee to draw a pebble from the bank, no action arguments needed.
  - "apply_equation": try to exchange pebbles using a given equation. argument "equation_number" for the equation index that will be used for the exchange.
  - "draw_card": attempt to draw a card from the game using pebbles in the wallet.
- get_turn_state() -> TurnState: Updates the Player class information regarding the player's score, bank state, and other players' scores using the turn state sent by the referee.
- end_turn(): Called by the player, sends the signal to end the turn to the referee.
- add_to_score(int): Called by Referee, adds an integer number of points to the player's current score. Restricted to only adding positive values.
- add_pebble(Pebble, int) -> Adds a specified number of pebbles to user's wallet. Input is a Pebble enum and a positive integer as a quantity.
- remove_pebble(Pebble, int) -> Remove a specified number of pebbles from the user's wallet. Input is a Pebble enum and a positive integer as a quantity. Number of pebbles removed must not exceed the number of pebbles of that color owned by the player.