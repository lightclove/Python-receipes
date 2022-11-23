def f(x, l=[]):
    l.append(x)
    return l


print (f(1), f(1), f(1))


def append(x, a=[]):
    if a:
        a.append(x)
    else:
        a = [x]
    return a


print (append(1), append(1), append(1))


class C:
    a = []

    def __init__(self, x):
        self.a.append(x)

    def r(self):
        return self.a


print (C(1).r(), C(1).r(), C(1).r())

from timeThis import timeThis
import random

letters = 'abcdefgxyz'


@timeThis
def func1(dict1):
    return [dict1.keys()[dict1.values().index(x)] for x in reversed(sorted(dict1.values()))]


@timeThis
def func2(d):
    return sorted(d.keys(), key=lambda x: d[x], reverse=True)


D = {}
for i in xrange(10000):
    key = lambda: ''.join(random.choice(letters) for i in xrange(3))

    if key not in D.keys():
        D[key] = random.choice(xrange(1000000))
# D = {'foo': 3, 'bar': 1, 'baz': 2}

func1(D)

func2(D)
