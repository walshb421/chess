import asyncio
from websockets.server import serve
import json
import queue

class Game:
    def __init__(self):
        self.connections = set()
        self.players = set()
        self.state = dict()
        self.callbacks = dict()
        self.mq = queue.Queue()

    def record_move(self, move):
        self.moves.append(move)
        self.turn += 1

    async def server(self):
        async with serve(self.handler, "0.0.0.0", 8765):
            await self.producer()

    async def handler(self, websocket):
        self.connections.add(websocket)
        try:
            async for message in websocket:
                await self.middleware(message)
        finally:
            self.connections.remove(websocket)

    async def producer(self):
        while True:
            try:
                msg = self.mq.get(block=False)
                self.state.update(msg)
                for websocket in self.connections:
                    await websocket.send(json.dumps(msg))
                self.mq.task_done()
            except queue.Empty:
                await asyncio.sleep(0.2)

    async def middleware(self, message):
        msg = json.loads(message)
        for path in msg:
            if self.callbacks[path]:
                self.callbacks[path](msg[path])

    def add_callback(self, path, callback):
        self.callbacks[path] = callback
    
        
    def update(self, mutation):
        self.mq.put(mutation)
	
    

