#-*-coding:utf-8*-
#!/usr/bin/env python
'''
https://pythonz.net/references/named/while-else/
'''
for el in [1, 2, 3]:
    print(el)
else:
    print('всё')

'''
Когда элементы ИСЧЕРПАНЫ (например, исчерпана последовательность, либо итератор возбудил исключение StopIteration) 
выполняется часть инструкции, идущая после else (если эта часть присутствует) и цикл завершается.
'''

for el in [1, 2, 3]:
    print(el)
    if el == 2:
        break
else:
    print('этот текст не будет выведен')