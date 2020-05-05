#-*-coding:utf-8*-
#!/usr/bin/env python
''''''
'''
Когда мы объявляем параметр со звёздочкой (например, *param), все позиционные аргументы начиная с этой позиции
и до конца будут собраны в кортеж под именем param. Аналогично, когда мы объявляем параметры с двумя
звёздочками (**param), все ключевые аргументы начиная с этой позиции и до конца будут собраны в СЛОВАРЬ
под именем param. 
'''

def total(initial=5, *numbers, **keywords):
    count = initial
    for number in numbers:
        count += number
    for key in keywords:
        count += keywords[key]
    return count

print(total(10,
            1, 2, 3,
            vegetables=50, fruits=100))
