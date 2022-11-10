'''
Декораторы — мощный инструмент в Python. 
Вы можете их использовать для ТОНКОЙ НАСТРОЙКИ работы КЛАССА или функции. 
Декораторы можно считать функцией, которая применена к другой функции. 
Чтобы определить функцию-декоратор для декорируемой функции, 
используется знак @ и после него название функции. 
Из этого следует, что декоратор принимает 
в качестве аргумента функцию, которою он декорирует.
Рассмотрим функцию square decorator(), 
которая в качестве аргумента принимает функцию 
и в результате также выдают функцию.

Decorators are a powerful Python tool.
You can use them to finely configure the class or function.
Decorators can be considered a function that is applied to another function.
To determine the function-decorator for the decorated function,
The @ and after it is used the name of the function.
It follows that the decorator accepts
As an argument, the function to which it decorates.
Consider the Square Decorator () function,
which as an argument accepts the function
And as a result, they also give out a function.
'''
from math import sin, pi

def square_decorator(function):
    def square_it(arg):
        x = function(arg)
        return x * x
    return square_it

def main():
    size_sq = square_decorator(len)
    print(size_sq([1, 2, 3]))

    sin_sq = square_decorator(sin)
    print(sin_sq(pi / 4))

    @square_decorator
    def plus_one(a):
        return a + 1

    a = plus_one(3)
    print(a)

if __name__ == '__main__':
    main()
