import asyncio
import re
from websocket import server
from board import ChessBoard

async def main(websocket):
    async for move in websocket:

        # Initalize the board
        board = ChessBoard()
        board.create_starting_board()

        # Assuming the game already is started
        # Parse Move
        moves = move.split()
        startMove = moves[0]
        endMove = moves[2]

        await websocket.send(message)

asyncio.run(server(main))