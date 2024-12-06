Pair: educational-lizards \
Commit: ae780d9c0da8fea92c3cbb08ff1f828d7ae6130 \
Score: 70/185 \
Grader: Aishwarya Suyamindra

### [5/25] Read me
  - [-20] No read me file in `Bazaar/Player`

### [20/20] Test-script inspection

### [35/130] Code Inspection  
- [-10] The interpretation of what represents pebble exchanges is not clear - you have mentioned it on the self-eval, but it looks like interpretation of `__possible_next_wallet_and_exchange` is incomplete
  
- [0/15] Signature and purpose statements that answer question 1 and 2 on the spec
  - [-15] `max_score_turn` does not specify the complete signature - the return type is missing
  
- [-5] `filter_smallest_pebble_exchange` is missing a purpose statement

- [0/10] Signature and purpose statements for tie-breaking pebble trading and card purchases
  - [-10] The methods `tie_break_card_purchase`, `tie_break_exchange_and_purchase` do not specify the complete signature

- [5/20] Organizing the strategy component
  - [-15] There is a lot of duplicated code between `max_score_turn` and `max_number_turn` which can be abstracted (as you have mentioned on the self-eval)
  - Note: Both  `max_score_turn` and `max_number_turn` have the same purpose statement, and call the the same method `get_best_socre_card_sequences`
  
- [0/40] Unit tests
  - [-40] The unit test cases linked on the self eval don't test the specified conditions - it does not test the strategy 

### [10/10] Design
