''''''
'''
Внутри класса можно СОЗДАТЬ ИДЕНТИФИКАТОР, через который в дальнейшем будут производиться операции ПОЛУЧЕНИЯ и ИЗМЕНЕНИЯ 
ЗНАЧЕНИЯ какого-либо АТРИБУТА, а также его УДАЛЕНИЯ. Создается такой идентификатор с помощью функции property (). 
'''

class PropertyExampleOne:

    def __init__(self, value):
        self.__privateVar = value

    def set_var(self, value):
        self.__privateVar = value

    def get_var(self):
        return self.__privateVar

    def del_var(self):
        del self.__privateVar

    p = property(get_var, set_var, del_var)

# objectOfMyClass = PropertyExampleOne(100)
# objectOfMyClass.p = 35
# print(objectOfMyClass.p)
'''
Python поддерживает альтернативный метод определения свойств - 
с помощью методов property (), setter () и deleter {), которые используются в декораторах
'''

class PropertyExampleTwo:

    def __init__(self, value):
        self.__privateVar = value
        self.__privateVarForDeleterTest = 444

    # gsd - getter, setter, deleter
    @property
    # Getter
    def gsd(self):
        return self.__privateVar

    # Setter
    @gsd.setter
    def gsd(self, value):
        self.__privateVar = value

    # Deletter
    @gsd.deleter
    def gsd(self):
        del self.__privateVar
        del self.__privateVarForDeleterTest

objectOfMyClass = PropertyExampleTwo(555)
objectOfMyClass.gsd = 111
print(objectOfMyClass.gsd)


'''
Имеется возможность определить абстрактное свойство - в этом случае все реализующие его методы должны быть переопределены в подклассе. 
Выполняется это с помощью знакомого нам декоратора @abstractmethoct из модуля аЬс. Пример определения абстрактного свойства:
'''
from abc import ABCMeta, abstractmethod
class PropertyExampleThree:

    def __init__(self, value):
        self.__privateVar = value
        #self.__privateVarForDeleterTest = 0

    # gsd - getter, setter, deleter
    @property
    @abstractmethod
    # Getter
    def gsd(self):
        return self.__privateVar

    # Setter
    @gsd.setter
    @abstractmethod
    def gsd(self, value):
        self.__privateVar = value

    # Deletter
    @gsd.deleter
    @abstractmethod
    def gsd(self):
        del self.__privateVar

# objectOfMyClass = PropertyExampleThree(777)
# objectOfMyClass.gsd = 7
# print(objectOfMyClass.gsd)
# objectOfMyClass = PropertyExampleThree(100)

'''
ПРИМЕЧАНИЕ
В версиях Python, предшествующих 3.3, для определения абстрактного свойства применялся декоратор @abstractproperty, 
определенный в модуле аЬс. Однако, начиная с Python 3.3, этот декоратор объявлен нерекомендованным к использованию.
'''
