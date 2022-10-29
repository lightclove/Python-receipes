'''
Параметры функции *args, **kwargs

Думаю, многие хоть раз видели такую запись,
сейчас мы узнаем, что это за магические символы.
Сообщу сразу, что args и kwargs – общепринятые имена переменных,
а разбирать мы будем звездочки перед ними.

В примере функция принимает обязательный аргумент value,
а остальных аргументов она как бы не ожидает.
В таком случае *args упаковывает все не именованные аргументы в кортеж,
а **kwargs – все именованные в словарь.

В целом, конструкция с *args, **kwargs получается достаточно полезной,
если мы не знаем, кто и в каких целях будет использовать нашу функцию.
То есть, мы можем запихнуть в аргументы после такого практически всё.

*args, ** kwargs Parameters of the function

I think many have seen such a record at least once
Now we will find out what these magic symbols are.
I will tell you right away that Args and Kwargs are generally accepted names of
variables,
And we will disassemble the stars in front of them.

In the example, the function accepts the mandatory argument Value,
And she, as it were, does not expect the rest of the arguments.
In this case, *Args packs all the incided arguments in the motorcade,
A ** KWARGS - all called in the dictionary.

In general, the design with *args, ** kwargs is quite useful,
If we do not know who and for what purpose will use our function.
That is, we can push into the arguments after this almost everything.
'''
def function(value, *args, **kvargs):
    print(value)  # 123
    print(args)   # ('some text', 456, [7, 8, 9])
    print(kvargs) # {'pi': 3.14, 'name': 'Ivan'}

# Usage
function(123 , 'some text', 456 , [7,8,9], pi=3.14, name='Ivan')

