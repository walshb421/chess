import asyncio
from websocket import server

async def main(websocket):
    async for message in websocket:
        await websocket.send("message")

asyncio.run(server(main))