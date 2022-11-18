"""
    Новая модель программирования RPyC (начиная с RPyC 3.00) основана на сервисах. 
    Как вы могли заметить, в классическом режиме клиент в основном получает полный контроль над сервером, 
    поэтому мы (привык) называем серверы RPyC подчиненными. 
    К счастью, это уже не так. Новая модель ориентирована на сервисы: 
    сервисы позволяют предоставлять четко определенный набор возможностей другой стороне, 
    что делает RPyC универсальной платформой RPC. 
    На самом деле классический RPyC, который вы видели до сих пор, — это просто «еще один» сервис.
    Услуги на самом деле очень простые. Чтобы доказать это, SlaveService 
    (сервис, который реализует классический RPyC) состоит всего из 30 строк, включая комментарии ;). 
    По сути, сервис имеет следующий шаблон:

    Аргумент conn для on_connect и on_disconnect добавлен в rpyc 4.0. 
    Это обратно несовместимо с предыдущими версиями, 
    где вместо этого конструктор службы вызывается с параметром соединения и сохраняет его в self._conn.

    Как видите, кроме специальных методов инициализации/финализации, вы можете определить класс как любой другой класс. 
    Однако, в отличие от обычных классов, вы можете выбрать, какие атрибуты будут доступны другой стороне: 
    если имя начинается с exposed_, атрибут будет доступен удаленно, 
    в противном случае он доступен только локально. 
    В этом примере клиенты смогут вызывать get_answer, но не get_question.
"""
import rpyc

class MyService(rpyc.Service):
    def on_connect(self, conn):
        # code that runs when a connection is created
        # (to init the service, if needed)
        pass

    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        # (to finalize the service, if needed)
        pass

    def exposed_get_answer(self): # this is an exposed method
        return 42

    exposed_the_real_answer_though = 43     # an exposed attribute

    def get_question(self):  # while this method is not exposed
        return "what is the airspeed velocity of an unladen swallow?"
    
if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    # Обратите внимание, что здесь мы передали класс MyService серверу, 
    # в результате чего каждое входящее соединение будет использовать 
    # свой собственный независимый экземпляр MyService в качестве корневого объекта.
    t = ThreadedServer(MyService, port=18861)
    t.start()
# Для теста запустите:
# >>> import rpyc
# >>> c = rpyc.connect("localhost", 18861)
# >>> c.root # <__main__.MyService object at 0x7f28a9946330> , f.ex.
"""
    Этот «корневой объект» является ссылкой (netref) на экземпляр службы, находящийся в серверном процессе. 
    Его можно использовать для доступа и вызова открытых атрибутов и методов:
"""
# >>> c.root.get_answer() # 42
# >>> c.root.the_real_answer_though # 43
# >>> c.root.get_question() # local traceback / remote traceback output

