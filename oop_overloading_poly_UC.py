'''
https://ru.stackoverflow.com/questions/511606/Перегрузка-метода-внутри-класса-в-python

# НЕ ПРОЯСНЕНО, НО СОХРАНЮ ДЛЯ
'''
'''
class test:
    def testrunner(self):
        pass
    def testrunner(self,a):
        pass
# при попытке сделать такое, не запустится, как это сделать

Перегрузка операторов — один из способов РЕАЛИЗАЦИИ ПОЛИМОРФИЗМА, 
когда мы можем задать свою реализацию какого-либо метода в своём классе.

В Python нет возможности перегрузить метод класса, как например в Java или С.
Но есть костыль. Метод может иметь значения параметров по-умолчанию,
что совместно с проверкой типа аргумента позволит вам сделать то, что вы хотите:
'''

class Test(object):

    def testrunner(self, i=None):
        if isinstance(i, str):
            print ('c: ', i)
        elif isinstance(i, int):
            print ('b: ', i)
        else:
            print ('a')
'''
Cледует упомянуть что не стоит писать Java код, используя Python синтаксис. 
Например, не обязательно всё внутрь классов пихать — в Питоне можно использовать свободные функции. 
К наличию многочисленных isinstance() в коде следует с подозрением относится — это может указывать на проблемы в интерфейсе. 
Следует рассмотреть альтернативные варианты, например, которые опираются на duck typing без isinstance костыле
'''
if __name__ == '__main__':
    print()

class BaseClass:

    def __init__(self):
        #        BaseClass.__init__(self)
        print('Создан экземпляр класса BaseClass')

    def go(self):
        print('Go, BaseClass!')


class DerivedClass1(BaseClass):
    '''
    Метод __init__ базового класса вызывается явно при помощи переменной self,
    чтобы инициализировать ЧАСТЬ ОБЪЕКТА, относящуюся к базовому классу
    Это очень важно запомнить: Python НЕ ВЫЗЫВАЕТ конструктор базового класса АВТОМАТИЧЕСКИ
    – его необходимо вызывать самостоятельно в явном виде.
    '''
    # def __init__(self):
    #     BaseClass.__init__(self)
    #     print('Создан экземпляр класса DerivedClass1')

    def go(self):
        print('Go, DerivedClass1!')
#
#
class DerivedClass2(BaseClass):
    '''
    Метод __init__ базового класса вызывается явно при помощи переменной self,
    чтобы инициализировать ЧАСТЬ ОБЪЕКТА, относящуюся к базовому классу
    Это очень важно запомнить: Python НЕ ВЫЗЫВАЕТ конструктор базового класса АВТОМАТИЧЕСКИ
    – его необходимо вызывать самостоятельно в явном виде.
    '''
    # def __init__(self):
    #     BaseClass.__init__(self)
    #     print('Создан экземпляр класса DerivedClass2')

    def go(self):
        print('Go, DerivedClass2!')

'''
Однако в python имеются методы, которые, как правило, не вызываются напрямую, а вызываются встроенными функциями или операторами.
Например, метод __init__ перегружает конструктор класса. Конструктор - создание экземпляра класса.
'''

if __name__ == '__main__':
    print()
    baseObject = BaseClass()
    baseObject.go()

    derivedObjected1 = DerivedClass1()
    derivedObjected1.go()

    derivedObjected2 = DerivedClass2()
    derivedObjected2.go()

    objects = [baseObject, derivedObjected1, derivedObjected2]
    print()

    for o in objects:
        o.go()

