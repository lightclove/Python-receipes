import itertools
from select import select

Codes = ['C', 'C++', 'Java', 'Python']
selectors = [True, False, True, False, True, True ]

Best_Programming = itertools.compress(Codes, selectors)

for each in Best_Programming:
    print(each)
