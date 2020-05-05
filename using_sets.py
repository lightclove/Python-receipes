#-*-coding:utf8;-*-
# множества позволяют бытро найти элемент в списке при помощи in
s0 = set() #создание пустого множества
print(s0)
s1 = {1, 2, 3} # в фигурных скобках задается множество
# print(s1)
print('s1 не изменится при добавлении существующего элемента', s1.add(1))
s1.remove(3)
#s1.remove(4) # не работает! If the element is not a member, raise a KeyError. - use discard() instead
s1.discard(4) # Remove an element from a set if it is a member. If the element is not a member, do nothing.
print(s1)
# во множетсве элементы уникальны
s2 = {"one","one",} # элемент не будет повторяться {"one"}
print(s2) # {'one'}
s3 = {"one", "two", "three"}
print('in the s3-set is always different order of an elements: ', s3) # каждый раз при перезапуске порядок меняется
# множества позволяют бытро найти элемент в списке при помощи in
print('Three in s3:', 'Three' in s3)
print('three in s3:', 'three' in s3)
s4 = {"three", "four", "five", "six"}
print('difference', s3.difference(s4))  #Return the difference of two or more sets as a new set.
print('difference', s4.difference(s3))  # "three" - общий - не выводится!
print('intersection', s3.intersection(s4))  # "three" - общий - не выводится!
print('intersection', s4.intersection(s3))  # "three" - общий - не выводится!
s1.clear()
print('s1 is now over:' , s1)
print('Why None? and not set() ? :', s1.clear()) # Мы не можем вывести сам оператор и результат его работы ?
# Перебор элементов множества
print()
s5 = {"one", "two", "three","one"} # последний элемент не выведется
for s in s5:
    print (s)
