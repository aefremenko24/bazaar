# Changes

**TO**: Co-Ceo

**FROM**: James Quinlivan, Arthur Efremenko

**CC**: CS4500 TAs

**DATE**: November 21, 2024

**SUBJECT**: Changes to Code

### Change to Code Base Part 1:
#### Changes to adding bonus points if a player, has bought cards with a red pebble, white pebble, and a blue pebble.
The change to the code base that this change would cause would not be super dramatic. This first thing that would be changed, 
is the data representation for the referee's player knowledge.
First we would include another field in the player knowledge, that tracks what card each player has purchased. <br>
Next we would add the functionality for checking what cards a player has bought at the end of the game, if the correct cards
were purchased. We would add the correct amount of points to the player and then decide the winners.<br>
This will affect our code base in only a handful a files:
1. player_state.py
2. rule_book.py
3. referee.py

### Part 2
#### Adding Another type of Pebble
Adding another type of pebble would change our code base across many files. We would have to adjust our definition of a pebble,
to now include the glowing pebble. We would also have to adjust the rules for buying cards, and exchanges. Changing the rules, would affect how strategy is
implemented. This would pertain to the rules around how a player could use a glowing pebble. With Python being untyped, this proposed data
change would cause us to have to change the pebble definition, allong with how the observer handles rendering the glowing pebble.
