The commit we tagged for your submission is 8b6d4211580cd3779db2d00346d6cbeb8e7a5e6.
**If you use GitHub permalinks, they must refer to this commit or your self-eval will be rejected.**
Navigate to the URL below to create permalinks and check that the commit hash in the final permalink URL is correct:

https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/tree/8b6d4211580cd3779db2d00346d6cbeb8e7a5e6

## Self-Evaluation Form for Milestone 4

Indicate below each bullet which method takes care of each task:

0. the data representation for representing pebble exchanges,
   including its interpretation

   we used a List[Equation] for pebble exchange, in order.
   This function finds all pebble exchanges and create an exchange and next_wallet set:
   the filtered equation in line 305 is List[Equation]
https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/8b6d4211580cd3779db2d00346d6cbeb8e7a5e6f/Bazaar/Player/strategy.py#L299-L308 

1. the data representation for representing the purchases of cards,
   including its interpretation
   we used a list[Card] as for purchases of cards:
   this function return all posiible cards purchase, which is list[list[Cards]]
   https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/8b6d4211580cd3779db2d00346d6cbeb8e7a5e6f/Bazaar/Player/strategy.py#L59-L76
   Another example for just one card purchase, this function return the score obtained using this give  card purchase with give wallet:
   https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/8b6d4211580cd3779db2d00346d6cbeb8e7a5e6f/Bazaar/Player/strategy.py#L78-L92

3. the strategy functionality for answering question 1 from the milestone
   its signature and purpose statement 

https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/8b6d4211580cd3779db2d00346d6cbeb8e7a5e6f/Bazaar/Player/strategy.py#L317-L339

Composite function answering questions 1 and 2 from the milestone. Uses many private functions to find the best sequences and tie-break.

3. the strategy functionality for answering question 2 from the milestone
   its signature and purpose statement 

https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/8b6d4211580cd3779db2d00346d6cbeb8e7a5e6f/Bazaar/Player/strategy.py#L317-L339

Composite function answering questions 1 and 2 from the milestone. Uses many private functions to find the best sequences and tie-break.

4. the strategy functionality for determining which pebble exchanges a
   player wishes to conduct; its signature and purpose statement 

https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/8b6d4211580cd3779db2d00346d6cbeb8e7a5e6f/Bazaar/Player/strategy.py#L147-L154

5. the strategy functionality for tie-breaking card purchases

https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/8b6d4211580cd3779db2d00346d6cbeb8e7a5e6f/Bazaar/Player/strategy.py#L111-L128

6. the strategy functionality for tie-breaking the exchanges of pebbles
   
https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/8b6d4211580cd3779db2d00346d6cbeb8e7a5e6f/Bazaar/Player/strategy.py#L130-L145

7. unit tests that show

  - no cards can be bought with the available pebbles

    https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/8b6d4211580cd3779db2d00346d6cbeb8e7a5e6f/Bazaar/Common/testPebble.py#L55-L67

    Here, subtracted pebble collection represents the card wallet 

  - a card can be bought without exchanges of pebbles
    
    https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/8b6d4211580cd3779db2d00346d6cbeb8e7a5e6f/Bazaar/Common/testCards.py#L20-L63

  - a card can be bought after an exchange of pebbles
    
    https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/8b6d4211580cd3779db2d00346d6cbeb8e7a5e6f/Bazaar/Common/testCards.py#L20-L63

  - two cards can be bought after an exchange of pebbles

    https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/8b6d4211580cd3779db2d00346d6cbeb8e7a5e6f/Bazaar/Common/testCards.py#L20-L63

8. Explain how your code abstracts over the two rather similar
   strategies.
   The strategies codes

   - If it uses the template-and-hook pattern from Fundamentals II,
     you may say so and explain where the abstract class and concrete
     classes are to be found.

  - If it uses the command pattern from Fundamentals III, you may say
    so and point to the the parameter is passed in, where it is used,
    and where the argument for the parameter is supplied.

  - If your code employs some other design pattern, explain.
The difference between the strategy is the two filtering functions for card purchase that we have refactored:
The filtering for max-score card purchase:
https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/8b6d4211580cd3779db2d00346d6cbeb8e7a5e6f/Bazaar/Player/strategy.py#L158-L174
the filtering for max-number card purchase:
https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/8b6d4211580cd3779db2d00346d6cbeb8e7a5e6f/Bazaar/Player/strategy.py#L176-L210
We used separately for two strategies:
for max-score strategy (*max_score_turn*):
https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/8b6d4211580cd3779db2d00346d6cbeb8e7a5e6f/Bazaar/Player/strategy.py#L330
for max-number strategy (*max_number_turn*):
https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/8b6d4211580cd3779db2d00346d6cbeb8e7a5e6f/Bazaar/Player/strategy.py#L354
A better abstraction in the future will be having for strategy and have the filtring method pass in as parameters. <br>


   
The ideal feedback for each of these points is a GitHub perma-link to
the range of lines in a specific file or a collection of files.

A lesser alternative is to specify paths to files and, if files are
longer than a laptop screen, positions within files are appropriate
responses.

You may wish to add a sentence that explains how you think the
specified code snippets answer the request.

If you failed to do any of the above points, say so.

