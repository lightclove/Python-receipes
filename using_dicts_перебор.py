''''''
# Перебор словаря
Dict = {
    'One' :  1,
    'Two' :  2,
    'Three': 3,
    'Five': {1,2,3,4,5}
}
# Первый способ перебора - Получаем ВСЕ КЛЮЧИ словаря
for key in Dict:
    print(key, end='\n')
print('________________')
# Второй способ перебора - Получаем ВСЕ КЛЮЧИ словаря keys() = a set-like object providing a view on D's keys """
for key in Dict.keys():
    print(key, end='\n')
print('________________')
#   Получаем ВСЕ ЗНАЧЕНИЯ словаря keys() = a set-like object providing a view on D's keys """
for key in Dict.values():
    print(key, end='\n')
print(type(Dict.values()))
print('________________')
#   Получаем ВСЕ ПАРЫ КЛЮЧ-ЗНАЧЕНИЕ словаря
for key, value in Dict.items():
    print('%s -> %s' % (key, value))
print(type(Dict.items())) # a set-like object providing a view on D's items
