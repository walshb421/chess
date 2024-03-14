from board import ChessBoard
import asyncio
if __name__ == "__main__":
   try:
        game = ChessBoard()
        asyncio.run(game.server())
   except KeyboardInterrupt:
        print("Reloading Server ... ")
        pass

