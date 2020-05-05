#-*-coding:utf-8*-
#!/usr/bin/env python
''''''
# Это мой список покупок
shoplist = ['яблоки', 'манго', 'морковь', 'бананы']
print('Я должен сделать ', len(shoplist), 'покупок.')
print('Покупки:', end=' ')
for item in shoplist:
    print(item, end=' ')
print('\nТакже нужно купить риса.')
shoplist.append('рис')
print('Теперь мой список покупок таков:', shoplist)
print('Отсортирую-ка я свой список')
shoplist.sort() # что этот метод действует на сам список, а не возвращает изменённую его версию, в отличии от СТРОК
print('Отсортированный список покупок выглядит так:', shoplist)
print('Первое, что мне нужно купить, это', shoplist[0])
olditem = shoplist[0]
#del shoplist[0] ######################## !!! ###################
#shoplist.remove(shoplist[0])
print('Я купил', olditem)
print('Теперь мой список покупок:', shoplist)
# добавит элементы списка в конец
shoplist.extend(['test1','test2'])
# добавит сам список в конец в качестве элемента
shoplist.append(['test3','test4'])
print(shoplist)
