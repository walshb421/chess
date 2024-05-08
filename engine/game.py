import asyncio
from websockets.server import serve
import json

class Game:
    def __init__(self):
        self.connections = set()
        self.moves = []
        self.board = {}
        self.turn = -1
        self.chats = []
        self.messages = {}

    def record_move(self, move):
        self.moves.append(move)
        self.turn += 1

    async def server(self):
        async with serve(self.handler, "0.0.0.0", 8765):
            await asyncio.Future()  # run forever

    async def handler(self, websocket):
        self.connections.add(websocket)
        try:
            async for message in websocket:
                response = await self.run_callback(json.loads(message))
                await self.update(response)
        finally:
            self.connections.remove(websocket)

    async def run_callback(self, message):
        if type(message) is dict:
            for key, value in message.items():
                return self.messages[key](value)
        
    async def update(self, message):
        for websocket in self.connections:
            await websocket.send(message)

    def add_callback(self, message, callback):
        self.messages[message] = callback
        
	
    

