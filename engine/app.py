from board import ChessBoard
import asyncio

game = ChessBoard()
asyncio.run(game.server())

