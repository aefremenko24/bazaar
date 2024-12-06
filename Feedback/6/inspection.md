Pair: educational-lizards \
Commit: c3e9ca66f2d4e3f998a237958c19760df4a8ae5 \
Score: 185/215 \
Grader: Sai Tulluri

## README [25/25]

- Well done!

## Code-inspection [130/160]

[-10] Setting up players with inital information can be factored out into its own function. For example, these [lines of code](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/9cf7960400220edf0e8eb23e27cb3de18b4152a4/Bazaar/Referee/referee.py#L433-L439) can be factored into a `setup_players` private function within `Referee`.
[-10] Similar to above point, [managing an individual turn](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/9cf7960400220edf0e8eb23e27cb3de18b4152a4/Bazaar/Referee/referee.py#L441-L443) can be factored into its own function.
[-10] Handling of [informing win / loss](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/9cf7960400220edf0e8eb23e27cb3de18b4152a4/Bazaar/Referee/referee.py#L445-L447) can be factored out into its function. On a side note, adding some explanation on why the player at 0th index always becomes a winner and all others would be losers as a comment / part of purpose statement in a factored out function would be helpful.

## Design inspection (game-observer.md) [30/30]

- Well done!
