'''
ИТЕРАЦИЯ ПО СПИСКУ В PYTHON С ПОМОЩЬЮ МЕТОДА ENUMERATE

Если вы не знаете, что именно enumerate делает в python,
то позвольте мне объяснить вам.
Метод enumerate() добавляет счетчик к итерируемому объекту и возвращает его.
И что бы ни возвращал метод enumerate, это будет ОБЪЕКТ enumerate.

Основное преимущество использования метода enumerate заключается в том,
что вы можете преобразовать объекты enumerate в list и tuple с помощью методов
list() и tuple() соответственно:

If you do not know what exactly Enumerate does in Python,
then let me explain to you.
The Enumerate () method adds the counter to the ititeous object and returns it.
And no matter what the Enumerate method return, it will be the Enumerate object.

The main advantage of using the Enumerate method is
that you can convert Enumerate objects to LIST and TUPLE using methods
List () and tuple (), respectively:
'''
list = [1,2,3,4,5,6,7,8,9]
print(enumerate(list)) # <enumerate object at 0x...>
for i, res in enumerate(list):
    print(i, ':', res)
