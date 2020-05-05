#!/usr/bin/env python
# coding:utf-8
# https://zhevak.wordpress.com/2016/03/30/python-последовательный-порт-и-нуль-модемн/
import threading
import serial

# ===============================================================================
class Conn(threading.Thread):
    '''
    Открываем и настраиваем последовательный порт.
    '''
    #def __init__(self, port="/dev/ttyS0", baud=57600):
    #def __init__(self, port="/dev/USB0", baud=57600):
    def __init__(self, port="COM8", baud=115200):
        threading.Thread.__init__(self)
        self.daemon = True

        try:
            self.ser = serial.Serial(port)
        except:  # SerialException:
            print "Проблема: не могу открыть порт", port
            exit(0)

        self.ser.baudrate = baud
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.timeout = None

    '''
    Для приёма сообщений создадим отдельный поток.
    Эта функция потока не должна вызываться напрямую из главного потока.
    Запуск функции осуществляется вызовом метода start
    '''

    def run(self):
        answer = ""  # Заготовка для новой строки
        # Бесконечный цикл
        while True:
            byte = str(self.ser.read())  # Читаем один байт
            if len(byte) == 1:
                answer += byte  # Составляем строку

                # Вывод ответа произведём только тогда, когда строка будет сформирована
                # полностью
                if len(answer) >= 1:
                    if answer[-1:] == "\n":  # Окончание строки
                        print answer[:-1]  # Выводим строку на терминал. Символ '\n'
                        #   будет добавлен оператором print
                        answer = ""  # Заготовка для новой строки

    '''
    Отправка текстового сообщения на другой комп
    '''
    def send(self, msg):
        self.ser.write(msg)


if __name__ == "__main__":

    #PORT = "/dev/ttyUSB0"
    PORT = "COM8"
    BAUDRATE = 57600

    conn = Conn(PORT, BAUDRATE)
    conn.start()

    print "Связь с другим хостом через нуль-модемный кабель."
    print "Для отправки сообщения на второй комп наберите сообщение и нажмите Enter."
    print "Для выхода из программы наберите слово QUIT и нажмите Enter."

    while True:
        message = raw_input(">")

        if message.upper().strip() == "QUIT":
            break
        else:
            conn.send(message + "\n")