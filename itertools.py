import time

from itertools import cycle, combinations
list = ['1','2','3','4','5']
clist = cycle(list)

for c in clist:
    time.sleep(1)
    print c

count = 0
for item in clist:
    if count >= 7:
        break
    print(item)
    count += 1


data = combinations('WXYZ', 2)
for item in data:
    print item # возвращает кортежи
   print(''.join(item)) # возвращает строки