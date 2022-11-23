'''
    Websockets is a library for building WebSocket servers and clients in Python 
    with a focus on correctness, simplicity, robustness, and performance.
    Built on top of asyncio, Python’s standard asynchronous I/O framework, 
    it provides an elegant coroutine-based API.
    
    Don’t worry about the opening and closing handshakes, pings and pongs, or any other behavior described in the specification. 
    
    websockets takes care of this under the hood so you can focus on your application!
    Here’s how a client sends and receives messages:

'''
# here’s an echo server:

import asyncio
import websockets

async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)

async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())

#  here’s an echo websocket client:
# import asyncio
# import websockets

# async def hello():
#     async with websockets.connect("ws://localhost:8765") as websocket:
#         await websocket.send("Hello world!")
#         await websocket.recv()

# asyncio.run(hello())


