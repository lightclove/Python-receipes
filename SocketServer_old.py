# -*- coding: utf-8 -*-
#!/usr/bin/env python2

###############################################################################

"""
Программа обработки клиентских запросов
На стороне сервера: открывает сокет на указанном порту, ожидает поступления
сообщения от клиента и отправляет его обратно; эта версия использует
стандартный модуль socketserver; модуль socketserver предоставляет классы
TCPServer, ThreadingTCPServer, ForkingTCPServer, их варианты для протокола
UDP и многое другое, передает каждый запрос клиента на соединение методу
handle нового экземпляра указанного объекта обработчика; кроме того,
модуль socketserver поддерживает доменные сокеты Unix, но только
в Unix­подобных системах; смотрите руководство по стандартной
библиотеке Python.
"""
import SocketServer, time  # получить серверы сокетов, объекты­обработчики

myHost = ''                # компьютер­сервер, '' означает локальный хост
myPort = 50007             # использовать незарезервированный номер порта

def now():
    return time.ctime(time.time())

class MyClientHandler(SocketServer.BaseRequestHandler):
    def handle(self):                      # для каждого клиента
        print(self.client_address, now())  # показать адрес этого клиента
        time.sleep(5)                      # имитировать блокирующие действия
        while True:                        # self.request – сокет клиента
            data = self.request.recv(1024) # чтение, запись в сокет клиента
            if not data: break
            reply = 'Echo=>%s at %s' % (data, now())
            self.request.send(reply.encode())
        self.request.close()
# создать сервер с поддержкой многопоточной модели выполнения,
# слушать/обслуживать клиентов непрерывно
myaddr = (myHost, myPort)
server = SocketServer.ThreadingTCPServer(myaddr, MyClientHandler)
server.serve_forever()
'''
Здесь усилия сосредоточены на реализации услуги (индивидуальной реализации метода handle), а не на деталях поддержки 
многопоточной модели выполнения. Результат обработки клиентских запросов
'''
