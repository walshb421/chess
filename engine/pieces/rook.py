from .piece import Piece
from move import Move

class Rook(Piece):
	def __init__(self, color, position):
		super().__init__(color, 'Rook', position)

	def generate_moves(self, board, moves, turn, flags):
		possible_moves = []
		start_row, start_col = self.position

		# Check each direction the rook can move
		for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
			for step in range(1, 8):
				end_row = start_row + direction[0] * step
				end_col = start_col + direction[1] * step

				# make sure the move is within the board limits
				if 0 <= end_row < 8 and 0 <= end_col < 8:
					# If the destination is empty add move and continue
					if board[end_row][end_col] is None:
						possible_moves.append(Move(self, (start_row, start_col), (end_row, end_col)))
					# If the destination has a enemy then we can capture it but cant go further so stop
					elif board[end_row][end_col].color != self.color:
						possible_moves.append(Move(self, (start_row, start_col), (end_row, end_col)))
						break
					# If the destination has our own piece, then stop
					else:
						break

		return possible_moves