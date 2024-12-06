The commit we tagged for your submission is 0693868b1ffb70ed016af7d29a3f9eb170789aa.
**If you use GitHub permalinks, they must refer to this commit or your self-eval will be rejected.**
Navigate to the URL below to create permalinks and check that the commit hash in the final permalink URL is correct:

https://github.khoury.northeastern.edu/CS4500-F24/ultimate-beetles/tree/0693868b1ffb70ed016af7d29a3f9eb170789aa

## Self-Evaluation Form for Milestone 8

Indicate below each bullet which file/unit takes care of each task:

- did you consider what role an observer plays in the overall system?

Yes, specified in the Observer purpose statement:
https://github.khoury.northeastern.edu/CS4500-F24/ultimate-beetles/blob/0693868b1ffb70ed016af7d29a3f9eb170789aaa/Bazaar/Referee/observer.py#L16-L22

- concerning the modifications to the referee: 

  - is the referee programmed to the observer's interface or is it hardwired?
    - The referee is programmed to the observer's class, so that the referee is attached on demand, the observer is not required in the referee at any point.
    - Method below shows how the observer is added to the referee:
    https://github.khoury.northeastern.edu/CS4500-F24/ultimate-beetles/blob/0693868b1ffb70ed016af7d29a3f9eb170789aaa/Bazaar/Referee/referee.py#L588-L595

  - if an observer is desired, is every state per player action sent to the observer? Where? 
    - Yes, every state per player action is sent to the observers that are attached to the referee.
    - This is done in handle_turns, where the observers are updates after .handle in every state is called:
    https://github.khoury.northeastern.edu/CS4500-F24/ultimate-beetles/blob/0693868b1ffb70ed016af7d29a3f9eb170789aaa/Bazaar/Referee/referee.py#L546-L563

  - if an observer is not desired, how does the referee avoid calls to the observer?
    - Observers attached to the referee are stored in the Referee class in a list
    - If the list is empty, update_observers will iterate through an empty list and basically not do anything:
    https://github.khoury.northeastern.edu/CS4500-F24/ultimate-beetles/blob/0693868b1ffb70ed016af7d29a3f9eb170789aaa/Bazaar/Referee/referee.py#L565-L576

- concerning the implementation of the observer:

  - does the purpose statement explain how to program to the
    observer's interface? 
    - Yes, the directions on what is required to construct and connect an observer to the Referee are described in the \_\_init\_\_ docstring:
    https://github.khoury.northeastern.edu/CS4500-F24/ultimate-beetles/blob/0693868b1ffb70ed016af7d29a3f9eb170789aaa/Bazaar/Referee/observer.py#L34-L53

  - does the purpose statement explain how a user would use the
    observer's view? Or is it explained elsewhere? 
    - Yes, the purpose statement for the observer explains it in detail:
    https://github.khoury.northeastern.edu/CS4500-F24/ultimate-beetles/blob/0693868b1ffb70ed016af7d29a3f9eb170789aaa/Bazaar/Referee/observer.py#L17-L23

The ideal feedback for each of these three points is a GitHub
perma-link to the range of lines in a specific file or a collection of
files.

A lesser alternative is to specify paths to files and, if files are
longer than a laptop screen, positions within files are appropriate
responses.

You may wish to add a sentence that explains how you think the
specified code snippets answer the request.

If you did *not* realize these pieces of functionality, say so.

