Pair: educational-lizards \
Commit: 1d31e67221c55794d37d19956b86932cf95a8c0 \
Score: 123/150 \
Grader: Kamalanethra Arulmozhi

[readme] - 20/20 - good job!

- [10/10] README file in Bazaar/,  mentions about Player directory

- [10/10] README file in Bazaar/Common mentions about rule-book

[code-inspection] - 88/90

- [20/20] - Helpful self eval

- [10/10] - To check the legality of the result of the first call from the referee to the player

- [10/10] - To check the legality of the result of the second call from the referee to the player

- [5/5] -  Functionality that checks if the game is over

- [5/5] - Functionality that checks whether a player may buy a card

- [5/5] - Functionality that determines the number of points a player gets for buying a card

- [10/10] - the tasks are properly divided into atomic methods

Testing: Good job!

- [3/5] For a test case with an empty bank. Honesty points!
- [5/5  for a test case that confirms that requesting from a non-empty bank is okay
- [5/5]   for a test case that covers a trade request that would put the player into “debt”
- [5/5]  for a test case that covers a trade request that would put the bank into “debt”
- [5/5]  for a test case for at least one trade that succeeds.

Design:  15/40

- [0/5] There is no explicit mention of legality checks
- [0/5] There is no clear mention of scoring.
- [5/5] For rotation of players
- [0/5] There is no mention of eliminating a player who makes an illegal request
- [5/5] to check whether the game is over.
- [5/15] - A referee must call in the following order - legality check, complete turn, the game is over check. There should be a clear distinction between the legality check and a complete turn. Also, game-over functionality should be called after each turn/action.
