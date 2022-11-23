# -*- coding: UTF-8 -*-
# !/usr/bin/env python2
# ----------------------------------------------------------------------------------------------------------------------
# Имя модуля: Transmitter2.py
# Назначение: Прослушивание 2 портов на предмет получения udp-пакетов и переброс полученных udp-пакетов на указанные
#             в конфигурационномфайле "Transmitter2.conf" ip дреса и порты
# Версия интерпретатора: 2.7.15
# Автор: Дмитрий Ильюшкò ilyushko@itain.ru dm.ilyushko@gmail.com
# Создан: 20.03.2019
# Изменен: 22.03.2019
# Правообладатель:(c) ЗАО "Институт телекоммуникаций" www.itain.ru 2019
# Лицензия: MIT www.opensource.org/licenses/mit-license.php
# ----------------------------------------------------------------------------------------------------------------------
import socket
import os
import threading
import time
from ConfigParser import ConfigParser
import sys

# ----------------------------------------------------------------------------------------------------------------------
# This is your Project Root'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
configParser = ConfigParser()
configFilePath = 'Transmitter.conf'
configParser.read(configFilePath)

listenPort_1 = configParser.get('config', 'listenPort_1')  #

listenIP_1 = configParser.get('config', 'listenIP_1')
# Если приходит heartbeat с размером пакета = 1 байт или заявка # с размером пакета = 9 байт
dstIP_1_1 = configParser.get('config', 'dstIP_1_1')
dstPort_1_1 = configParser.get('config', 'dstPort_1_1')  # Если приходит heartbeat с размером пакета = 1 байт или заявка
# с размером пакета = 9 байт
dstIP_1_2 = configParser.get('config', 'dstIP_1_2')  # Если приходит пакет с размером большим 9 байт
listenPort_2 = configParser.get('config', 'listenPort_2')  # Переброс пакета с порта на порт  в пределах узла OB.
listenIP_2 = configParser.get('config', 'listenIP_2')  # Маршрут От OA к OB
dstIP_2_1 = configParser.get('config', 'dstIP_2_1')  # Если приходит heartbeat с размером пакета = 1 байт или заявка
# с размером пакета = 9 байт или маршрут , отсылаем пакет на этот ip-адрес
dstPort_2_1 = configParser.get('config',
                               'dstPort_2_1')  # Если приходит heartbeat с размером пакета = 1 байт или заявка
# с размером пакета = 9 байт
dstIP_2_2 = configParser.get('config', 'dstIP_2_2')  # Если приходит пакет с размером пакета большим 16 байт
dstPort_2_2 = configParser.get('config', 'dstPort_2_2')  # Если приходит пакет с размером пакета = 16 байт
dstPort_2_3 = configParser.get('config', 'dstPort_2_3')  # Если приходит маршрут с размером пакета равным 16 байт
bufferSize = configParser.get('config', 'bufferSize')


# ----------------------------------------------------------------------------------------------------------------------

# dstPort
def receivePackets(serverIP, serverPort):
    while 1:
        UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        UDPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        UDPClientSocket.bind(('0.0.0.0', int(serverPort)))
        # receiving packets
        print(threading.currentThread().getName() + u':Server accepting data on: ' + unicode(
            UDPClientSocket.getsockname()))

        data, addr = UDPClientSocket.recvfrom(1024)
        print(threading.currentThread().getName() + u': From address: ' + str(addr[0]) + u' on port: ' + str(
            serverPort) + u' received udp-datagram data: ' + unicode(str(data))) + unicode(
            str(serverPort) + u' with size of bytes:' + unicode(str(len(data))))  # print(data)'
        # Пересылка пакетов при получении и их анализ с дальнейшим перебросом
        # на указанные в конфигурационном файле Transmitter.conf порты и ip-адреса
        # Если получен heartbeat  размером пакета = 1 байт, переброс на OB c ip

        if (len(data) == 1 and int(serverPort) == int(listenPort_1)):
            print(u"Received HEARTBEAT: " + unicode(data.decode('utf-8')) + "with size of packet = " + len(
                data) + u" from: " + addr)
            sendByteArray(data, dstIP_1_1, int(dstPort_1_1))

        elif (len(data) == 9 and int(serverPort) == int(listenPort_1)):
            print(u"Received REQUEST(Заявка): " + unicode(data.decode('utf-8')) + "with size of packet = " + len(
                data) + u" from: " + addr)
            # также как и выше
            sendByteArray(data, dstIP_1_1, int(dstPort_1_1))


        elif (len(data) > 9 and int(serverPort) == int(listenPort_1)):
            print(u"Received udp-packet: " + unicode(data.decode('utf-8')) + "with size of packet = " + len(
                data) + u" from: " + addr)
            #  такой же порт как и выше
            sendByteArray(data, dstIP_1_2, int(dstPort_1_1))

        # ----------------------------------------------------------------------------------------------------------------------
        if (len(data) == 1 and int(serverPort) == int(listenPort_2)):
            print(u"Received HEARTBEAT: " + unicode(data.decode('utf-8')) + u"with size of packet = " + len(
                data) + u" from: " + addr)
            sendByteArray(data, dstIP_2_1, int(dstPort_2_1))

        elif (len(data) == 9 and int(serverPort) == int(listenPort_2)):
            print(u"Received REQUEST(Заявка): " + unicode(data.decode('utf-8')) + u"with size of packet = " + str(
                len(data)) + u" from: " + str(addr))
            sendByteArray(data, dstIP_2_1, int(dstPort_2_1))

        elif (len(data) == 16 and int(serverPort) == int(listenPort_2)):
            print(u"Received udp-packet: " + unicode(data.decode('utf-8')) + u"with size of packet = " + str(
                len(data)) + u" from: " + str(addr))
            sendByteArray(data, dstIP_2_1, int(dstPort_2_3))

        elif (len(data) > 16 and int(serverPort) == int(listenPort_2)):
            print(u"Received ROUTE: " + unicode(data.decode('utf-8')) + "with size of packet = " + len(
                data) + u" from: " + addr)
            sendByteArray(data, dstIP_2_2, int(dstPort_2_3))
        # ----------------------------------------------------------------------------------------------------------------------


def sendByteArray(bytesToSend, ipdaddr, port):
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    serverAddressPort = (ipdaddr, port)
    # Create a UDP socket at client side
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    print(threading.currentThread().getName() + u':data: ' + bytesToSend + u'were sent to the: ' + str(
        serverAddressPort) + u" with size of bytes: " + str(len(bytesToSend)))
    time.sleep(1)
    UDPClientSocket.close()


# ----------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    try:
        print(u"Program started...")
        # global - для возможности доступа к потокам (доступа из блока перехвата исключения
        # и перевод  их в .setDaemon(True)) и их убийства после того как приложение завершится
        global receivePackets_thread1, receivePackets_thread2  # для доступа
        # (serverIP, serverPort, dstPort):
        receivePackets_thread1 = (threading.Thread(target=receivePackets, args=([listenIP_1, int(listenPort_1)])))
        receivePackets_thread1.setName(u"RECEIVER THREAD 1")
        receivePackets_thread1.start()
        receivePackets_thread2 = (threading.Thread(target=receivePackets, args=([listenIP_2, int(listenPort_2)])))
        receivePackets_thread2.setName(u"RECEIVER THREAD 2")
        receivePackets_thread2.start()

    except socket.error:
        print(str(socket.error) + "\nSocket error handling... Continue listening")
    # для перехвата ошибок и корректного завершения приложения с очисткой ресурсов - потоков
    except (KeyboardInterrupt, SystemExit):
        print('Program was interrupted by user')
        # ToDO Убить все запущенные потоки. Как вариант - запускать процессы
        receivePackets_thread1.setDaemon(True)
        receivePackets_thread2.setDaemon(True)
        sys.exit()
