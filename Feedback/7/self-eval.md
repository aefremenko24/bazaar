The commit we tagged for your submission is 2733d07ec665f00b45f165e1687e2fbcc14bb86.
**If you use GitHub permalinks, they must refer to this commit or your self-eval will be rejected.**
Navigate to the URL below to create permalinks and check that the commit hash in the final permalink URL is correct:

https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/tree/2733d07ec665f00b45f165e1687e2fbcc14bb86

## Self-Evaluation Form for Milestone 7

Indicate below each bullet which file/unit takes care of each task:

1. turned failing integration tests into language-specific unit tests
https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/2733d07ec665f00b45f165e1687e2fbcc14bb860/Bazaar/Planning/todo.md?plain=1#L34
https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/721f0245d957e448682dde88dfaf4b6f766b2cf5/Bazaar/Common/test_rulebook.py#L99-L116

2. reformulated unit tests for &quot;functions&quot; called from failing &quot;methods&quot;
   This commit involves adding unite tests in test_referee that break down steps from running entire game using execute_game function
https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/2733d07ec665f00b45f165e1687e2fbcc14bb860/Bazaar/Planning/todo.md?plain=1#L58
https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/721f0245d957e448682dde88dfaf4b6f766b2cf5/Bazaar/Common/test_rulebook.py#L422-L549

3. added purpose statements to methods whose names didn't convey the full purpose
https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/2733d07ec665f00b45f165e1687e2fbcc14bb860/Bazaar/Planning/todo.md?plain=1#L88
https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/721f0245d957e448682dde88dfaf4b6f766b2cf5/Bazaar/Player/strategy.py#L305-L319
https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/2733d07ec665f00b45f165e1687e2fbcc14bb860/Bazaar/Planning/todo.md?plain=1#L69
https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/721f0245d957e448682dde88dfaf4b6f766b2cf5/Bazaar/Referee/referee.py#L492-L494

4. factor methods that mixed several tasks into a composite and atomic tasks 
https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/2733d07ec665f00b45f165e1687e2fbcc14bb860/Bazaar/Planning/todo.md?plain=1#L70
https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/721f0245d957e448682dde88dfaf4b6f766b2cf5/Bazaar/Referee/referee.py#L448-L490
also the changes in this commit in the strategy file:
https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/2733d07ec665f00b45f165e1687e2fbcc14bb860/Bazaar/Planning/todo.md?plain=1#L58
https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/blob/721f0245d957e448682dde88dfaf4b6f766b2cf5/Bazaar/Player/strategy.py#L250-L269



The ideal feedback for each of these points is a GitHub perma-link to
the range of lines in a specific file or a collection of files that _illustrates_
how you dealt with each of these points.

A lesser alternative is to specify paths to files and, if files are
longer than a laptop screen, positions within files are appropriate
responses.

You may wish to add a sentence that explains how you think the
specified code snippets answer the request.

If you did *not* address any of these points, say so.

