"""
    Как удалить ключ из словаря при помощи генератора

    Генераторы словаря в Python — это быстрые однострочники,
    которые позволяют легко создавать словари.

    Здесь важно понимать, что мы создаем новый словарь.
    Поэтому это не самый экономичный метод удаления ключа.
    Но если вы уверены, что ключ существует,
    а словарь не слишком велик, можно воспользоваться и генератором.
    ---------------------------------------------------------------------------
    How to remove the key from a dictionary using a generator

    Python dictionary generators are fast single line,
    which allow you to easily create dictionaries.

    It is important to understand here that we are creating a new dictionary.
    Therefore, this is not the most economical method of removing the key.
    But if you are sure that the key exists,
    And the dictionary is not too large, you can use the generator.
"""
# Удаление КЛЮЧА из словаря ПРИ ПОМОЩИ ГЕНЕРАТОРА:
a_dict = {'Ivan':21, 'Piotr:31', 'Sidor':41, 'John':22, 'Jack':32, 'Harry':42}
a_dict = {key:a_dict[key] for key in a_dict if key !='John' }
print(a_dict)
