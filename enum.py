"""
    Перечисления enum
    Python 3 поддерживает простой способ написания перечислений через класс Enum. 
    Этот класс можно назвать удобным способом ИНКАПСУЛЯЦИИ СПИСКА КОНСТАНТ, 
    чтобы они не были разбросаны по всему коду БЕЗ СТРУКТУРЫ.
"""
from enum import Enum, auto


class Monster(Enum):
    HITLER = auto()
    STALIN = auto()
    PUTIN = auto()
    CHIKATILLO = auto()
    BREWIK = auto()
    ZOMBIE = auto()
    VAMPIRE = auto()
    CYRIAK = auto() 

print(Monster.PUTIN)
