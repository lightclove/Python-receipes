#-*-coding:utf-8*-
#!/usr/bin/env python
''''''
from math import *
n = input("Введите диапазон:- ")
p = [2, 3]
count = 2
a = 5
while (count < int(n)):
    b = 0
    for i in range(2, a):
        if (i <= sqrt(a)):
            if (a % i == 0):
                print("a - neprostoe", a)
                b = 1
            else:
                pass
    if (b != 1):
        print("a - prostoe", a)
        p = p + [a]
    count = count + 1
    a = a + 2
    #print p
