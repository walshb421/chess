import asyncio
from websocket import server
from game import Game
#from board import ChessBoard

# Runs when websocket connection is established
async def main(websocket):
    # Initalize the board
    game = Game()
    #board = ChessBoard()
    #board.create_starting_board()    

    #await websocket.send(board.game_to_json())

    # Runs everytime client sends data
    async for message in websocket:
        game.on_message(message)
        # Parse Move
        #moves = move.split()
        #startMove = moves[0]
        #endMove = moves[2]

        # Do move and update board
        #if(board.can_move_piece(startMove, endMove)):
        #    board.move_piece(startMove, endMove)
            
        # Send resulting board/game state
        #await websocket.send(board.game_to_json())            

asyncio.run(server(main))