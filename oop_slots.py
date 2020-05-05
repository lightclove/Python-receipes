''''''
'''
Можно также ОГРАНИЧИТЬ перечень атрибутов, РАЗРЕШЕННЫХ для ЭКЗЕМПЛЯРОВ класса. 
Для этого РАЗРЕШЕННЫЕ атрибуты перечисляются внутри класса в АТРИБУТЕ __slots__. 
В качестве значения атрибуту можно присвоить строку или список строк с названиями идентификаторов. 

Если производится попытка обращения к атрибуту, не перечисленному в __slots__, 
то возбуждается исключение AttributeError (листинг 13.22).
AttributeError: 'MyClass' object has no attribute 'Var3'

AttributeError: 'MyClass' object attribute 'Var3' is read-only
AttributeError: 'MyClass' object has no attribute 'Var3'
'''

class MyClass:
    __slots__ = ["Var1", "Var2"]

    def __init__(self, value1, value2, value3 ):
        self.Var1, self.Var2  = value1, value2
        self.Var3 = None # Read-only



objectOfMyClass = MyClass(100, 200, 300)
print(objectOfMyClass.Var1, objectOfMyClass.Var2)
objectOfMyClass.Var1, objectOfMyClass.Var2 = 400 , 500
print(objectOfMyClass.Var1, objectOfMyClass.Var2)

# try:
#     objectOfMyClass.Var3 = 555
#     print(objectOfMyClass.Var3)
# except AttributeError as msg:
#     print(msg)

