"""
Аннотация типов

Тайп хинтинг был добавлен в python еще в версии 3.5 вместе c библиотекой typing, 
в которой содержались структуры нужные для создания дженериков для аннотирования переменных. 
Тогда синтаксис аннотирования работал при инициализации переменных. 
В последствии в версии 3.6 эта возможность была расширена и 
стало возможно объявлять типы переменных вообще в любом месте кода.

В python 3.9 была добавлена возможность использовать в качестве дженериков 
для аннотирования встроенные коллекции, вместо структур typing'а (List, Dict, Tuple...).

И наконец в 3.10 на замену перечисления возможных принимаемых типов через typing.Union пришел опреатор | (or). 
Также в 3.10 был изменен синтаксис создания тайпалиасов, чтобы разграничить с присваиванием переменной, 
теперь лучше это делать непосредственно через TypeAlias.
"""
# earlier
from typing import List
some_list: List[int] = [1, 2, 3, 4, 5]
# now
some_list: list[int] = [1, 2, 3, 4, 5]

# earlier
name = str
def foo() -> name:
    pass

# now 
from typing import TypeAlias
name: TypeAlias = str
def foo() -> name:
    pass

# earlier
from typing import Union
def foo(val: Union[int, float]) -> Union[int, float]:
    pass

# now 
def foo(val: int | float ) -> int or float:
    pass

"""
Annotation of types

Type Hinting was added to Python back in version 3.5 together with the Typing library,
In which the structures were contained necessary for creating generics for annotating variables.
Then the syntax of annotation worked in the initialization of variables.
Subsequently in version 3.6, this possibility was expanded and
It has become possible to declare types of variables in general anywhere in the code.

Python 3.9 was added the opportunity to use as generics
For annotation, built -in collections, instead of Typing structures (List, Dict, Tuple ...).

And finally, at 3.10, a defiator came to replace the possible types of types through Typing.union | (or).
Also at 3.10, the syntax of the creation of the Typalias was changed to distinguish with the assignment of a variable,
Now it is better to do this directly through Typealias.
"" ""