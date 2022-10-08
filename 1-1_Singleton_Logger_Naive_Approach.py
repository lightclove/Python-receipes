# -*- coding: utf-8 -*-
"""
Что не так с этим кодом?

Он нарушает причины изменения, которые приняты в концепции SRP (single responsibility principle).
Необходимо помнить, что доступ к экземплярам класса осуществляется только методом get_instance().
Проблема в дескрипторе, куда пишутся логи со стороны класса Logger.
"""


class Logger:
    @staticmethod
    def get_instance():
        if '_instance' not in Logger.__dict__:
            Logger._instance = Logger()
        return Logger._instance

    def write_log(self, path):
        pass


if __name__ == "__main__":
    s1 = Logger.get_instance()
    s2 = Logger.get_instance()
    assert s1 is s2
