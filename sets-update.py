# set=Набор — это неупорядоченная, неизменяемая* и неиндексированная коллекция. Нет повторяющихся членов.
# Кортеж — это упорядоченная и неизменяемая коллекция. Позволяет дублировать участников.
# Словарь представляет собой сборник упорядоченный** и изменяемый. Нет повторяющихся членов
#Note: Both union() and update() will exclude any duplicate items.
sets = {3,4,5}
sets.update([1,2,3]) 
print(sets) #{1, 2, 3, 4, 5}
# add method
thisset = {"apple", "banana", "cherry"}
thisset.add("orange")
print(thisset)

