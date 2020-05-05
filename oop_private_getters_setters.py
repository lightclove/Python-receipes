''''''
'''
ПРИМЕЧАНИЕ:  

Все идентификаторы внутри класса в языке Python являются открытыми. т. е. доступны для непосредственного изменения. 
Для имитации частных идентификаторов можно воспользоваться методами __getattr__(), __getattribute__() и __setattr__(),
которые ПЕРЕХВАТЫВАЮТ ОБРАЩЕНИЯ к АТРИБУТАМ КЛАССА.
Кроме того, можно воспользоваться идентификаторами, названия которых начинаются с двух символов подчеркивания. 
Такие идентификаторы называются 'псевдочастными. Псевдочастные идентификаторы доступны лишь внутри класса, НО НИКАК НЕ ВНЕ ЕГО. 
Тем не менее, изменить идентификатор через экземпляр класса ВСЕ РАВНО МОЖНО, зная, КАКИМ ОБРАЗОМ ИСКАЖАЕТСЯ НАЗВАНИЕ ИДЕНТИФИКАТОРА. 
Например, идентификатор __privateVar внутри класса Classl будет доступен по имени _Classl.__privatevar
Как можно видеть, здесь перед идентификатором добавляется название класса с предваряющим символом подчеркивания. 
Приведем пример использования псевдочастных идентификаторов.
'''
class MyClass:

    def __init__(self, value):
        self.__privateVar = value

    def set_var(self, value):
        self.__privateVar = value

    def get_var(self):
        return self.__privateVar

    def del_var(self):
       del self.__privateVar


objectOfMyClass = MyClass(100)
print(objectOfMyClass.get_var())

try:
    print(objectOfMyClass.__privateVar) # Ошибка!!
except AttributeError as msg:
    print(msg)

objectOfMyClass.__class__._privateVar = 50 #
print(objectOfMyClass.__class__._privateVar)
objectOfMyClass.del_var()

# Выведет: 10 # Изменяем значение # Выведет: 20 # Перехватываем ошибки
# Выведет: 'MyClass' object has # no attribute ' _privateVar' # Значение псевдочастных атрибутов # все равно можно изменить # Выведет: 50

