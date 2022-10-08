#!/usr/bin/python
# -*- coding: utf-8 -*-
# Итак, проблемы из предыдущего примера решены.
# Но возможно ли найти более оптимальный способ (без наследования классов)?

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Logger(metaclass=Singleton):
    def write_log(self, path):
        pass


if __name__ == "__main__":
    logger1 = Logger()
    logger2 = Logger()
    assert logger1 is logger2
