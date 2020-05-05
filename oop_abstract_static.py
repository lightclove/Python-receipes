''''''
'''
см. также oop_abstract_class.py

    В состав стандартной библиотеки входит модуль abc. В этом модуле определен ДЕКОРАТОР @abstractmethod,
    который позволяет указать, что метод, перед которым расположен декоратор abstractmethod, является абстрактным.
    При попытке создать экземпляр класса-потомка, в котором не переопределен абстрактный метод, ВОЗБУЖДАЕТСЯ ИСКЛЮЧЕНИЕ TypeError. 
    Рассмотрим использование декоратора @abstractmethod на примере
    Имеется возможность создания абстрактных статических методов и абстрактных методов класса, 
    для чего необходимые декораторы указываются одновременно, друг за другом. 
    Для примера объявим класс с абстрактными статическим методом и методом класса
'''
'''
ПРИМЕЧАНИЕ
    В версиях Python. предшествующих 3.3, для определения абстрактного статического метода 
    предлагалось использовать декоратор @abstractstaticmethod, а для определения
    абстрактного метода класса - декоратор @abstractclassmethod 
    Оба этих декоратора определены в том же модуле аЬс. 
    Однако. начиная с Python 3.3, эти декораторы объявлены нерекомендованными к использованию.
'''

from abc import ABCMeta, abstractmethod

class AbstractBaseClass(metaclass=ABCMeta): # metaclass=ABCMeta - без этого абстрактность не организовать

    @staticmethod
    @abstractmethod
    def abstractMethod(self, x): # Абстрактный статический метод
        pass

    @classmethod
    @abstractmethod
    def abstractMethod(self, x): # Абстрактный метод класса
        pass
########################################################################################################################
class DerivedClass1(AbstractBaseClass): # Наследуем абстрактный метод

    def abstractMethod(self, x): # Переопределяем абстрактный метод
        print('Функционал переопределенного метода класса {0} со значением x ='.format(self.__class__.__name__), x)
########################################################################################################################

class DerivedClass2(AbstractBaseClass):  #Класс НЕ ПЕРЕОПРЕДЕЛЯЕТ метод
    pass
########################################################################################################################

if __name__ == '__main__':
    print()

    do1 = DerivedClass1()
    do1.abstractMethod(11) # Работает!

    #abc = AbstractBaseClass() # ВОЗБУЖДАЕТСЯ ИСКЛЮЧЕНИЕ TypeError: Can't instantiate abstract class DerivedClass2 with abstract methods abstractMethod
    #do2 = DerivedClass2() # ВОЗБУЖДАЕТСЯ ИСКЛЮЧЕНИЕ TypeError: Can't instantiate abstract class DerivedClass2 with abstract methods abstractMethod
