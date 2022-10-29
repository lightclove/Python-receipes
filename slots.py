"""
    _slots_ в Python 
    Позволяет снизить объём памяти, потребляемой экземплярами класса, 
    ограничивая количество атрибутов ими поддерживаемых.
    По умолчанию классы используют СЛОВАРЬ для хранения АТРИБУТОВ — 
    это позволяет модифицировать набор атрибутов объекта прямо в ходе исполнения программы. 
    Однако такой подход оказывается ЗАТРАТНЫМ для объектов, 
    набор атрибутов которых невелик или ограничен. 
    Это становится особенно заметно, когда создаётся БОЛЬШОЕ КОЛИЧЕСТВО ЭКЗЕМПЛЯРОВ.

    Поведение по умолчанию можно изменить, задав slots при определении класса. 
    В slots могут быть перечислены атрибуты для значений которых требуется зарезервировать место 
    (с точки зрения CPython в объекте класса резервируется место для МАССИВА УКАЗАТЕЛЕЙ на Python-объекты). 
    При этом ни dict, ни weakref  для экземпляров автоматически созданы не будут 
    (даже если в качестве значения строки указать пустую строку).

    В качестве значения slots может быть указана строка, объект поддерживающий итерирование, или последовательность строк 
    с именами атрибутов, использующихся экземплярами.

    Слоты реализуются при помощи создания дескриптора для каждого из перечисленных атрибутов.
    Попытки присвоить экземпляру атрибут, который не был перечислен в slots будет поднято исключение AttributeError.
    Если требуется динамическое назначение атрибутов, следует указать в 
    перечислении слотов '__dict__'.

    Не имея атрибута weakref, экземпляры классов со slots не поддерживают слабые 
    ссылки на себя.
    
    Если требуется поддержка слабых ссылок, следует указать в перечислении слотов '__weakref__'.

    Область действия слотов ограничено классом, в котором они определены, 
    поэтому наследники (если конечно они не определили собственные слоты) будут иметь dict.

    Если наследники тоже определяют слоты, то в перечислении должны содержаться лишь 
    дополнительные. 
    В последующих версиях возможно будет реализована проверка на совпадение имён.

    Непустой slots не может быть использован для классов, наследующихся от встроенных типов переменной длины, 
    например long, str и кортеж. 
    При попытке сделать это будет поднято исключение TypeError.

    Слот может принимать перечисления с «нестроками». 
    Например, могут использоваться отображения, 
    однако в будущих версиях значения по ключам могут быть наделены неким определённым смыслом.

    Если назначается class, следует проследить, что для обоих классов определены одинаковые слоты.

"""

class Ordinary(object):
    """
        Экземпляры этого класса могут дополняться атрибутами 
        во время исполнения.

    """


class WithSlots(object):

    __slots__ = 'static_attr'


a = Ordinary()
b = WithSlots()

a.__dict__ # {}
b.__dict__  # AttributeError: 'WithSlots' object has no attribute '__dict__'. Did you mean: '__dir__'?

a.__weakref__  # None
b.__weakref__  # AttributeError: 'WithSlots' object has no attribute '__weakref__'

a.static_attr = 1
b.static_attr = 1

a.dynamic_attr = 2
b.dynamic_attr = 2  # AttributeError

"""
    _Slots_ in python
    Allows you to reduce the amount of memory consumed by copies of the class, limiting
    The number of attributes supported by them.
    By default, classes use a dictionary for storing attributes - this allows
    Modify the set of attributes of the object directly during the execution of the program. However
    This approach is costly for objects, the set of attributes of which is small
    And/or limited. This becomes especially noticeable when a large
    The number of copies.

    The default behavior can be changed by setting Slots when determining the class. AT
    Slots can be listed attributes for which are required
    to reserve a place (from the point of view of Cpython in the class object is reserved
    place for an array of indicators on Python objects). At the same time, neither DICT nor Weakref
    They will not be automatically created for specimens (even if as a value
    Lines indicate the empty line).

    The value of Slots can be indicated a line that supports the object
    Iterization, or a sequence of lines with the names of attributes used
    copies.

    Slots are implemented by creating a descriptor for each of the listed
    attributes.
        Attempts to assign an attribute instance, which was not listed in Slots will be
    The exception of Attributeerror is raised.
    If the dynamic purpose of attributes is required, you should specify in
    listing the slots '__dict__'.

    Without the Weakref attribute, copies of classes with Slots do not support weak
    Links to yourself.
    2.3 If you need support for weak links, you should indicate in the transfer
    Slots '__weakref__'.

    The scope of the slots is limited by the class in which they are determined, therefore
    Heirs (unless of course they determined their own slots) will have DICT.

    If the heirs also determine the slots, then the transfer should only contain
    Additional. In subsequent versions, a check for
    coincidence of names.

    Non -why Slots cannot be used for classes inherited from
    built -in types of variable length, such as LONG, STR and motorcade. Upon attempt
    This will be raised by Typeerror's exception.

    The slot can accept transfers with "non -rhinas." For example, they can be used
    display, however, in future versions the values ​​of the keys can be endowed
    Some certain meaning.

    If Class is prescribed, it should be traced that for both classes are defined
    The same slots.

"""