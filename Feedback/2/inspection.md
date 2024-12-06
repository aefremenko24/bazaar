Pair: ultimate-penguins \
Commit: 7e8f22f247fff535786060f5dfc400f3b6cdf29 \
Score: 50/95 \
Grader: Sai Tulluri

readme: [20/20]

Well done!

code-inspection: [20/55] (includes bonus)

- [-10] Please include signatures for your functions. Since you're using an untyped language like Python, you can include types in your comments. It is unclear from `filter_equations_by_pebbles(equations, player)` what are the types of `equations` (a list? a list of?) and `player` (instance of a class?).
- [-10] Unit testing for "filtering" doesn't consider cases where the "bank" doesn't have right kind of pebbles and also where the "bank" and player's wallet doesn't have right kind of pebbles.
- [-10] Question 5: While the equations component is useful for the player to determine what pebbles to use like you stated, it is also important to recognise that a referee would also use this component to determine whether a player's action is illegal.
- [0/10] BONUS: A collection of pebbles can be thought as a "bag" or a "muti-set" and can be abstracted into a seperate data representation. Lost bonus points as this wasn't implemented.

design task: [10/20]

- [-5] No functionality to pick a random pebble from the bank.
- [-5] No functionality that lets a player swap pebbles for a card.
