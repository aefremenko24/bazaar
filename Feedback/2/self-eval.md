The commit we tagged for your submission is 7e8f22f247fff535786060f5dfc400f3b6cdf29.
**If you use GitHub permalinks, they must refer to this commit or your self-eval will be rejected.**
Navigate to the URL below to create permalinks and check that the commit hash in the final permalink URL is correct:

https://github.khoury.northeastern.edu/CS4500-F24/ultimate-penguins/tree/7e8f22f247fff535786060f5dfc400f3b6cdf29

## Self-Evaluation Form for Milestone 2

Indicate below each bullet which file/unit takes care of each task:

1. does your implementation come with a separate data representationn
   for collections of pebbles (like those on cards, in the bank, or in
   the player's possession)? 
   
   - Since pebbles are not unique and color is their only property, we decided to use a Color enum to represent each pebble, as opposed to creating a struct or a class. Collections of pebbles are then represented simply by a list of Color enums.

   https://github.khoury.northeastern.edu/CS4500-F24/ultimate-penguins/blob/7e8f22f247fff535786060f5dfc400f3b6cdf295/Bazaar/Common/utils.py#L76-L85

2. do your "filtering" and "acquisition" functionalities come with
   signatures/purpose statements? 

   - Yes. See **_filter_equations_by_pebbles_** and **_can_acquire_card_** functions below.

   https://github.khoury.northeastern.edu/CS4500-F24/ultimate-penguins/blob/7e8f22f247fff535786060f5dfc400f3b6cdf295/Bazaar/Common/equations.py#L71-L82

   https://github.khoury.northeastern.edu/CS4500-F24/ultimate-penguins/blob/7e8f22f247fff535786060f5dfc400f3b6cdf295/Bazaar/Common/cards.py#L82-L95

3. do your "filtering" and "acquisition" functionalities come with
   unit tests? 

   - Yes. See **_test_filter_equations_by_pebbles_** and **_test_can_aquire_card_** for each function respectively.

   https://github.khoury.northeastern.edu/CS4500-F24/ultimate-penguins/blob/7e8f22f247fff535786060f5dfc400f3b6cdf295/Bazaar/Common/test_equations.py#L22-L43

   https://github.khoury.northeastern.edu/CS4500-F24/ultimate-penguins/blob/7e8f22f247fff535786060f5dfc400f3b6cdf295/Bazaar/Common/test_cards.py#L21-L41

4. is your "filtering" functionality a composite of other pieces of
   functionality? (Its specification implies at least two tasks.)
   
   - Yes. Equation class method **_can_use_equation_** is used in a list comprehension for filtering. In turn, **_can_use_equation_** is composed of two functions: **_can_use_left_side_** and **_can_use_right_side_**.
   
   https://github.khoury.northeastern.edu/CS4500-F24/ultimate-penguins/blob/7e8f22f247fff535786060f5dfc400f3b6cdf295/Bazaar/Common/equations.py#L71-L82

   https://github.khoury.northeastern.edu/CS4500-F24/ultimate-penguins/blob/7e8f22f247fff535786060f5dfc400f3b6cdf295/Bazaar/Common/equations.py#L144-L152

Thinking question: 

It is necessary to consider the use cases (context) behind
programming tasks, for example, when you work out the focused and
precise purpose statement of the equations component.  Here is the
question you would ponder: 

5. How do you anticipate this component will be used?

- This component will be used in the game when a player wants to exchange pebbles with the bank, using any of the applicable 10 equations as exchange rates. The functions described above will help determine which equations the player can use and which way the exchange will go (left or right).

#### Notes 

Remember that if you think the name of a method/function is _totally
obvious_, there is no need for a purpose statement.

The ideal feedback for each of these points is a GitHub perma-link to
the range of lines in a specific file or a collection of files.

A lesser alternative is to specify paths to files and, if files are
longer than a laptop screen, positions within files are appropriate
responses.

You may wish to add a sentence that explains how you think the
specified code snippets answer the request.

If you failed to do any of the above points, say so.

