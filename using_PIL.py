# -*- coding: utf-8 -*-
#Как можно реализовать передачу изображения от клиента к серверу используя PIL ImageGrab.grab()
import PIL 

buf = BytesIO()

img = ImageGrab.grab()
img.save(buf, 'png')

some_socket.sendall(buf.getvalue())

