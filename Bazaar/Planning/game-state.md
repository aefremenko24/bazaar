# Game State

**TO**: Matthias Felleisen

**FROM**: Arthur Efremenko, Tony Lyu

**CC**: CS4500 TAs

**DATE**: September 25, 2024

**SUBJECT**: Game State Planning

### **Data Representation**:

To manage the state of the game and make sure game rules are followed by players, the referee needs access to some of the game object states. 
Those include the information about each player, in-game resources information (cards, equations, pebble bank), and information about turns. 
The referee should also determine the winner when win conditions are met by one of the players. 
The following are potential fields the Referee object should have access to:

- Players(loPlayer): A list of players participating in the current Bazaar Game.
- Cards(loCard): A list of cards representing cards available in the current Bazaar Game.
- Equations(loEquation): A list of Equations available in the current Bazaar Game.
- Pebbles(loColor): A list of Pebbles (bank) available in the current Bazaar Game.
- Turn information(int): Represents index of current player whose turn it is to move.
- Game Phase(enum): Initial, representing start of game; Round, representing game in process, End, representing a player has win.
- End condition(predicate): To decide if the game can proceed.
- Actions(loAction): A list of valid actions Players can make(skip, draw, exchange, etc.).
- Outcome(return Player): Return the Player who wins the current Bazaar Game. Could be a print statement depending on future implementation.
  
### **Operations for Referee**:

Operations for referee are designed to monitor the flow of the game, check validity of player actions, facilitate game progress, and determining winner of the game. 
The operations include initialization of the game, giving and ending turns for players, process player actions to update the game, and end the game when appropriate. 
The following are potential operations available to the referee:

- start(): Initialize game, resources, and board.
- turn() -> Player: Give current player turn to make actions.
- check_valid_action(String) -> Boolean: Check if the given action is valid(uses helpers from equations and cards).
- receive_action(Player) -> String: Receives the player action, execute the action if its valid.
- execute_action(Player, String): Execute the Player's action and update game states.
- end_turn(): Ends turn for current player, update Turn information(Player index).
- check_game_over() -> Boolean: Checks if the current game is over.
- winner() -> Player: Returns the Player who wins the current game, and end the game loop.

