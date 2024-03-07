import asyncio
from websocket import server
from board import ChessBoard

# Runs when websocket connection is established
async def main(websocket):
    # Initalize the board
    board = ChessBoard()
    board.create_starting_board()    

    await websocket.send(board.game_to_json())

    # Runs everytime client sends data
    async for move in websocket:
        # Parse Move
        moves = move.split()
        startMove = moves[0]
        endMove = moves[2]

        # Do move and update board
        if(board.can_move_piece(startMove, endMove)):
            board.move_piece(startMove, endMove)
            
        # Send resulting board/game state
        await websocket.send(board.game_to_json())            

asyncio.run(server(main))