
import socket
localIP = "127.0.0.1"
localPort = 20001
bufferSize = 2048
msgFromServer = "RESPONSE FROM SERVER: Client's message was: "

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening on ip: " + str(localIP) + " and port: " + str(localPort))
#Listen for incoming datagrams
def init():
    while (True):
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        if not bytesAddressPair:
            break
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        clientMsg = "Message from Client:{}".format(message)
        clientIP = "Client IP Address:{}".format(address)
        print(clientMsg)
        print(clientIP)
        bytesToSend = str.encode(msgFromServer + clientMsg )
        # Sending a reply to client
        UDPServerSocket.sendto(bytesToSend, address)

    UDPServerSocket.close()

init()

# import socket
#
# sock = socket.socket()
# sock.bind(('', 20001))
# sock.listen(1)
# client, addr = sock.accept()
#
# print('connected:', addr)
#
# while True:
#     data = client.recv(2048).decode()
#
#     if not data:
#         break
#     print(data)
#     client.send(data.upper().encode())
#
# client.close()
