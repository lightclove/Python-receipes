'''
    Creating a dictionary of two lists
    Создание словаря из двух списков

    Встроенная функция zip() принимает несколько ИТЕРИРУЕМЫХ объектов и
    возвращает     последовательность  кортежей. Каждый кортеж группирует
    элементы объектов по их индексу.

    The built -in zip () function accepts several iteric objects and
    Returns the sequence of motorcies. Each motorcade groups
    Elements of objects according to their index.
'''
keys   = ['first_key','second_key','third_key']
values = ['first_value','second_value','third_value']
zipped = dict(zip(keys, values))
print(zipped)
# {
#    'first_key': 'first_value',
#    'second_key': 'second_value',
#    'third_key':'third_value'
# }

print(type(zipped)) #<class 'dict'>

