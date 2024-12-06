The commit we tagged for your submission is d0a6a66a0a8d32fdb0eea08620e9100a69182f0.
**If you use GitHub permalinks, they must refer to this commit or your self-eval will be rejected.**
Navigate to the URL below to create permalinks and check that the commit hash in the final permalink URL is correct:

https://github.khoury.northeastern.edu/CS4500-F24/ultimate-beetles/tree/d0a6a66a0a8d32fdb0eea08620e9100a69182f0

## Self-Evaluation Form for Milestone 9

Indicate below each bullet which file/unit takes care of each task.

### Programming Task 

For `Bazaar/Server/player`,

- explain how it implements the exact same interface as `Bazaar/Player/player`
  - Since we are working in Python, with no interface functionality available, we created a ProxyPlayer class that implements all methods from the Mechanism API. This includes name, setup, request_pebble_or_trades, request_cards, and win. Since Python doesn't do any type checking, as far as the Referee object is concerned, all methods it needs to interact with the player mechanism are available in the ProxyPlayer, so we can just pass it to the Referee instead of the actual Mechanism.
- explain how it receives the TCP connection that enables it to communicate with a client
  - When the ProxyPlayer class is initialized by the Server, it gets passed the StreamReader and StreamWriter objects (those are initialized by the Server class and are unique to each client) to be able to read and write to the TCP stream that the Server established previously.
  - https://github.khoury.northeastern.edu/CS4500-F24/ultimate-beetles/blob/d0a6a66a0a8d32fdb0eea08620e9100a69182f03/Bazaar/Server/player.py#L19-L48
- point to unit tests that check whether it writes (proper) JSON to a mock output device
  - No unit tests :(

For `Bazaar/Client/referee`,

- explain how it implements the same interface as `Bazaar/Referee/referee`
  - Similarly to the ProxyPlayer, ProxyReferee is a class that implements all public methods in the Referee API. Again, since Python does not support interfaces and does not do type checking, the client can just initialize ProxyReferee object client side and use it instead of the regular Referee.
- explain how it receives the TCP connection that enables it to communicate with a server
  - The ProxyReferee object stores the StreamReader and StreamWriter objects that are initialized by the Client class based on the port and host provided by the user. The reader and writer objects are used to read data and send data from and to the server respectively. They are unique to this singular client-server TCP connection and correspond to the StreamReader and StreamWriter objects described previously in ProxyReferee.
  - https://github.khoury.northeastern.edu/CS4500-F24/ultimate-beetles/blob/d0a6a66a0a8d32fdb0eea08620e9100a69182f03/Bazaar/Client/referee.py#L29-L43
- point to unit tests that check whether it reads (possibly broken) JSON from a mock input device
  - No unit tests as well :( (but broken JSON messages are thoroughly accounted for)

For `Bazaar/Client/client`, explain what happens when the client is started _before_ the server is up and running:

- does it wait until the server is up (best solution)
- does it shut down gracefully (acceptable now, but switch to the first option for 10)
  - The latter option: it shuts down gracefully and does not wait for the server to be up.
  - https://github.khoury.northeastern.edu/CS4500-F24/ultimate-beetles/blob/d0a6a66a0a8d32fdb0eea08620e9100a69182f03/Bazaar/Client/client.py#L43-L49

For `Bazaar/Server/server`, explain how the code implements the two waiting periods. 
  - The server implements the waiting periods using the `await asyncio.sleep(MAX_SIGNUP_WAITING_TIME)` call (here, 20 seconds). It does until either MAX_WAITING_ROUNDS (here, 2) waiting periods are done, or if there is sufficient number of players (here, 2 to 6) signed up by the end of the first waiting period. See code snipped below for implementation.  
  - https://github.khoury.northeastern.edu/CS4500-F24/ultimate-beetles/blob/d0a6a66a0a8d32fdb0eea08620e9100a69182f03/Bazaar/Server/server.py#L106-L123

### Design Task 

For design task 1,

- did you make sure to separate the changes into one for the knowledge
  about players and one for the rule book? Why is this separation critical?
  - Yes, we specifically stated that the changes would be done separately to the player_state.py and rule_book.py. This separation is important because the referee should know what cards the player have purchased in order to award the bonus points, but the referee should not do the scoring itself: it should be delegated to the rule_book.

For design task 2, 

- did you consider changes to the data representation pebbles?
  - Yes, we considered the way we would change the Pebble class we currently use to represent a single pebble and PebbleCollection class we use to represent multiple pebbles.
  - Because we have a separate classes for Pebble, PebbleColor, and PebbleCollection, as opposed to using built in types, the changes would not be too difficult to implement (for example, is_glowing could be a new field in Pebble):
  - https://github.khoury.northeastern.edu/CS4500-F24/ultimate-beetles/blob/d0a6a66a0a8d32fdb0eea08620e9100a69182f03/Bazaar/Common/pebble.py#L58-L63
- would this change induce changes to wallets and cards?
  - Yes, we stated that this change would affect how cards are generated and purchased, because the cards with glowing pebbles should not be mixed with the existing cards. We also did point out that this will affect wallets, since glowing pebbles should be used in different scenarios, as opposed to regular pebbles.

For the reflection on design tasks, you may wish to point to relevant
pieces of code to justify your responses. There was no need to
implement anything so the _old_ code is all the TAs need. 

### Form of Feedback


The ideal feedback for each of these three points is a GitHub
perma-link to the range of lines in a specific file or a collection of
files.

A lesser alternative is to specify paths to files and, if files are
longer than a laptop screen, positions within files are appropriate
responses.

You may wish to add a sentence that explains how you think the
specified code snippets answer the request.

If you did *not* realize these pieces of functionality, say so.

