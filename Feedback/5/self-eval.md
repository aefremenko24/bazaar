The commit we tagged for your submission is 826d5d0d5e70b1814a265c3ca85fd5825b938d7.
**If you use GitHub permalinks, they must refer to this commit or your self-eval will be rejected.**
Navigate to the URL below to create permalinks and check that the commit hash in the final permalink URL is correct:

https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/tree/826d5d0d5e70b1814a265c3ca85fd5825b938d7

## Self-Evaluation Form for Milestone 5

Indicate below each bullet which piece of your code takes care of each task:

1. where is the functionality (signature, purpose statement) that
   checks the legality of the result of the first call from the referee
   to the player

https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/826d5d0d5e70b1814a265c3ca85fd5825b938d79/Bazaar/Common/rule_book.py#L103-L122

2. where is the functionality (signature, purpose statement) that
   checks the legality of the result of the second call from the referee
   to the player

https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/826d5d0d5e70b1814a265c3ca85fd5825b938d79/Bazaar/Common/rule_book.py#L170-L190

3. the rules of the game also specify whether a player may buy a card, 
   how to score the purchase of a card, and how to determine whether
   the game is over.

   - Does your rule-book code include these pieces of functionality?
   
   Yes, game_over is still in game_state though.

  - where?
    - Can player buy a card: https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/826d5d0d5e70b1814a265c3ca85fd5825b938d79/Bazaar/Common/rule_book.py#L124-L137
    - Card purchase scoring: https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/826d5d0d5e70b1814a265c3ca85fd5825b938d79/Bazaar/Common/rule_book.py#L191-L212
    - Is the game over: https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/826d5d0d5e70b1814a265c3ca85fd5825b938d79/Bazaar/Referee/game_state.py#L33-L51

  - Did you revise `game-state` to rely on rule-book instead of
    implementing the check directly?
    - game-state did not rely on the rule-book directly because it imports Equations and Cards, which themselves rely on the rule-book directly.
    - https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/826d5d0d5e70b1814a265c3ca85fd5825b938d79/Bazaar/Common/equations.py#L249
    - https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/826d5d0d5e70b1814a265c3ca85fd5825b938d79/Bazaar/Common/cards.py#L212

4. Where are the unit tests for the two explicitly required pieces of
   functionality? Specifically, point to unit tests that

    - with an empty bank and a request for a pebble
      - Missing this unit test :(

    - confirms that requesting from a non-empty bank is okay
      - https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/826d5d0d5e70b1814a265c3ca85fd5825b938d79/Bazaar/Common/test_rulebook.py#L263-L269
      - From docstring in rulebook: https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/826d5d0d5e70b1814a265c3ca85fd5825b938d79/Bazaar/Common/rule_book.py#L111
   
    - covers a trade request that would put the player into ``debt''
      - https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/826d5d0d5e70b1814a265c3ca85fd5825b938d79/Bazaar/Common/test_rulebook.py#L155-L169      

    - covers a trade request that would put the bank into ``debt''
      - https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/826d5d0d5e70b1814a265c3ca85fd5825b938d79/Bazaar/Common/test_rulebook.py#L171-L183
   
    - for at least one trade that succeeds.
      - https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/826d5d0d5e70b1814a265c3ca85fd5825b938d79/Bazaar/Common/test_rulebook.py#L201-L207

The ideal feedback for each of these points is a GitHub perma-link to
the range of lines in a specific file or a collection of files.

A lesser alternative is to specify paths to files and, if files are
longer than a laptop screen, positions within files are appropriate
responses.

You may wish to add a sentence that explains how you think the
specified code snippets answer the request.

If you failed to do any of the above points, say so.

