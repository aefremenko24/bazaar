## TO-DO List

**FROM**: Arthur, Ezri

**DATE**: October 27, 2024

## TODO

#### game_state.py
- [ ] fix unit tests set up due to the change of PebbleCollection implementation

#### exchange.py
- [ ] change name of classes
- [ ] test and debug the recursive search for all possible wallet

#### purchase.py
- [ ] unit test for search and tie-breaking

#### mechanism.py
- [ ] Add unit tests for mechanism.py

#### referee.py
- [ ] write unit test for each protocol call
- [ ] have ai player test to run the whole game


--------------------

## Completed:
#### exchanges.py
- [x] fix issue with Exchange serializer not allowing duplicate equations -- [fix issue with Exchange serializer not allowing duplicate equations](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/e5b2d62f94b695981bc3bee7d3ba4f293da5c8ce)
- [x] make Exchanges deserializer explicit as opposed to using Equations.deserialize -- [make Exchanges deserializer explicit as opposed to using Equations.deserialize](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/793de46c9883e2d707327b73de24730279142249)
#### test_rulebook.py
- [x] [move functionality from card test](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/577b837bbd21a7dcab7f1586c9a9a9c4812cf0f8)
#### player_state.py
- [x] remove name from PlayerState -- [remove name from PlayerState](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/dcfd03c10610951f4d5b2ad51f907a902888f458)
- [x] change id to name to match the mechanism fields -- [add name field in PlayerState to replace id](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/71c12bd95787051290394d287da02f1e18e1680a)
#### game_state.py
- [x] add a method for kicking player provieded their actor in game_state - [add a method for kicking player provieded their actor in game_state](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/cfba6f864f077030deecec5684751311569e005c)
- [x] get is_bank_empty in game_state to work properly -- [fix is_bank_empty in game_state](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/4a545b3616ef811823738944b4384842271f9af7)
- [x] add function for extracting the active actor due to the change in turn_state -- [add get active player](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/8ead397b5a3c6186dcd61099aa323751a8048d2f)
#### equations.py
- [x] fix can_trade_equation failing half the time -- [fix can_trade_equation failing half the time](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/10bba76fbd94ae8c378f58b1463a7ee0589c4ba0)
- [x] add less than method for comparing two Equation instances -- [add less than method for comparing two Equation instances](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/87d6cd2d653a1fe9d0514e6aa9e7cd61ee2edd55)
- [x] fix unit tests set up due to the change of PebbleCollection implementation -- [fix syntax](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/7a538657bd2b2769bd19e42a6ab862f2f8494dc5)
- [x] change tests to adapt tuple instead of list inside PebbleCollection -- [fix syntax](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/b9b76eda38d2cf0486ad9c1b885aa650a4ff89d1)
#### turn_state.py
- [x] add assert messages in turn_state validators for clearer debugging -- [add assert messages in turn_state validators for clearer debugging](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/753ffdd379ee9a385ea438e35d2913abd1123200)
- [x] change active_player in TurnState to active_player_score and active_player_wallet to avoid circular import of Mechanism
  - [resolve circular import](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/94d0df91ee414e3b50058df3c32494473d6efd72)
  - [turn_state changes](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/96c4e9f1d44f7b4e499e0f9b985b5cf573fada22)
#### cards.py
- [x] fix \_\_lt\_\_() function unit tests -- [fix \_\_lt\_\_](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/c0584ed541eb77b876105dd03549524f026c99ea)
- [x] write unit test for compare sequence of cards -- [fix cards test](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/44119d223b54d5680b9054096461d3b255d05885)
#### purchase.py
- [x] get tie-breaking in purchases.py to work based on strategy -- [get tie-breaking in purchases.py to work based on strategy](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/a292a5e61d1d562cef4b580f640fa8b5d1412f92)
- [x] add default fields to PurchaseSequence to be able to initialize an empty purchase sequence -- [add default fields to PurchaseSequence to be able to initialize an empty purchase sequence](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/f93a15f49df9b1a7d11cd99e6f639a3565d9bf52)
- [x] finish the implementation of new search -- [refactor strategy and add ref unit tests](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/17b401221b518af74237fd4d9697bd589ddc9fc1)
#### strategy.py
- [x] store both number of cards purchased and both points received from purchasing the sequence in Strategy - [store both number of cards purchased and both points received from purchasing the sequence in Strategy](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/97273e27e1061e88fe5401827a7e9c7aa4142b12)
- [x] make purchase empty sequence store the original wallet and bank -- [make purchase empty sequence store the original wallet and bank](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/dfbbbe29322439276085827faebcbe81ae584fa6)
- [x] account for the player wishing to not buy any cards, returning an empty PurchaseSequence -- [account for the player wishing to buy 0 cards](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/4a2b3fb43c06fed1a4c4253851e3f0f966d8f3da)
- [x] change using flag to indicate strategy -- [refactor strategy and add ref unit tests](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/17b401221b518af74237fd4d9697bd589ddc9fc1)
- [x] refactor get_trade_purchase -- [refactor strategy and add ref unit tests](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/17b401221b518af74237fd4d9697bd589ddc9fc1)
#### referee.py
- [x] move the kick_player to before creating the game state in Referee InitState -- [move kick player in setup](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/f51a501a0ceb727f6bc407393155c90bd3fffbff)
- [x] move notify players about equations to a separate function in Referee -- [move notify players about equations to a separate function in Referee](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/8263ae05280ba7a3324e18c272bc1fb1fbab0adf)
- [x] Handle setup exceptions in InitState -- [handle setup exceptions in InitState](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/7bbc95a900a9fecb070a7fc18f2983ac33fc56f6)
- [x] Fix unmatch signature for execute_game() -- [fix signature](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/15d04220e815fc96e37981bbc86849fdb65f0257)
- [x] Separate execute_game into notify_result and init_game_state in Referee class -- [add condition](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/4de2b267e446f8a0e114d0d769bac5055c3f5aed)
#### mechanism.py
- [x] pass policy into strategy calls in Mechanism - [pass policy into strategy calls in Mechanism](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/b1b5485cc64ca32c2b7d462877b8180a06d9b71f)
- [x] Add name() function back in mechanism.py -- [extract refreee n fix meechanism](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/a1eff9555b23fb92ed494fa78c15b07777258ea3)
- [x] Fix circular import -- [resolve circular import](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/94d0df91ee414e3b50058df3c32494473d6efd72)
- [x] Add serializer and deserializer in mechanism.py -- [add serializer and deserializer for Mechanism](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/52d8cf6cce684930afe479a106cc00c0228ae37e)
#### other
- [x] Add missing README.md files for milestone 6 -- [md files](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/9cf7960400220edf0e8eb23e27cb3de18b4152a4)
- [x] Editing this document:
  - [add more items](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/de6c927c589b82dda841235d1c0efd0577164b04)
  - [add more items](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/72a7e3d56a7cb0055d04eea0b695778a69a479e2)
  - [add to do list](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/d3d600455f9247f4a9f0f15f1bbfc8b18e8408f8)
  - [finished two items](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/2474dbc116ddea0d061226fdfc9c6d7d51442930)
  - [add more todos](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/962abb97e87c1f5d0dc359a3b5c0b0f85bfeab69)
  - [add commits and commit messages to todo.md](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/4bc647ac20494d7133591f915afc5da8f841292b)
  - [add cards tests to completed](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/b5bf54d193c6f24e9e77785b0dada36db5800890)
  - [add game_state to completed](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/c696fb61d1d16d4a5df8f2251ee2ea3dd3feeb17)
  - [add completed field](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/2e4ac460367dce70cf1427edc5fc02aa448cc311)
- [x] Clean up docstrings -- [code walk changes](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/a3e843617108410e3ab8e054ed403a434eefd7d2)
- [x] Add UML diagrams to README for milestone 6 -- [add diagrams for 7](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/c49f1f3c4e2c493f160caf7ce702cf33dc8b1aa4)
#### code formatting
- [x] [run black formatter](https://github.khoury.northeastern.edu/CS4500-F24/educational-lizards/commit/bad7a0554af2c85b950e3450168b49ac96ed456f)