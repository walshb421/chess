import asyncio
from websockets.server import serve
import json

class Game:
    def __init__(self):
        self.websocket = {}
        self.players = {}
        self.config = {}
        self.moves = []
        self.board = {}
        self.turn = -1
        self.chats = []
        self.messages = {}

    async def server(self):
        async with serve(self.websocket_handler, "0.0.0.0", 8765):
            await asyncio.Future()  # run forever

    async def websocket_handler(self, websocket):
        self.websocket = websocket
        async for message in websocket:
            await self.update(websocket, self.on_message(json.loads(message)))

    def on_message(self, message):
        if type(message) is dict:
            for key, value in message.items():
                return self.messages[key](value)
        
    async def update(self, websocket, message):
        await websocket.send(message)

    def add_callback(self, message, callback):
        self.messages[message] = callback
        
	
    

