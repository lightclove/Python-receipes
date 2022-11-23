'''
    Websockets is a library for building WebSocket servers and clients in Python with a focus on correctness, simplicity, robustness, and performance.
    Built on top of asyncio, Python’s standard asynchronous I/O framework, it provides an elegant coroutine-based API.
    Here’s how a client sends and receives messages:
'''
'''
    websockets — это библиотека для создания серверов и клиентов WebSocket на Python 
    с упором на правильность, простоту, надежность и производительность.
    Построенный на основе asyncio, стандартной платформы асинхронного ввода-вывода Python, он
    предоставляет элегантный API на основе coroutines (сопрограмм).
    Вот как клиент отправляет и получает сообщения:
'''
#!/usr/bin/env python

import asyncio
import websockets

async def hello():
    async with websockets.connect("ws://localhost:8765") as websocket:
        await websocket.send("Hello world!")
        await websocket.recv()

asyncio.run(hello())


