import random
import itertools
SUITS = 'cdhs'
RANKS = '23456789TJQKA'
DECK  = tuple(''.join(card) for card in itertools.product(RANKS, SUITS))
hand  = random.sample(DECK, 4)
print(hand)
# ['Kh', '2s', '9c', '8c']
