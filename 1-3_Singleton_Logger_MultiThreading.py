#!/usr/bin/python
# -*- coding: utf-8 -*-

from threading import Lock, Thread


class Singleton(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Logger(metaclass=Singleton):
    def __init__(self, name):
        self.name = name

    def write_log(self, path):
        pass


def test_logger(name):
    logger = Logger(name)
    print(logger.name)


if __name__ == "__main__":
    process1 = Thread(target=test_logger, args=("FOO",))
    process2 = Thread(target=test_logger, args=("BAR",))
    process1.start()
    process2.start()
