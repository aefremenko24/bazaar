from pydantic import conint

Score = conint(ge=0)
PEBBLE_COUNT = 5
CARD_COUNT = 20
CARD_REWARDS = {
    (0, False): 5,
    (0, True): 8,
    (1, False): 3,
    (1, True): 5,
    (2, False): 2,
    (2, True): 3,
    (3, False): 1,
    (3, True): 2,
}
MIN_EQUATION_SIZE = 1
MAX_EQUATION_SIZE = 4
MIN_CARDS_NUM = 0
MAX_CARDS_NUM = 20
MAX_EQUATION_NUM = 10
WIN_SCORE = 20

MAX_EXCHANGE_DEPTH = 4
