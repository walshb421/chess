from piece import Piece
from move import Move

class Knight(Piece):
	def __init__(self, color, position):
		super().__init__(color, 'Knight', position)

	def generate_moves(self, board, moves, turn):
		possible_moves = []
		start_row, start_col = self.position

		# Check each direction the knight can move
		for direction in [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]:
			end_row = start_row + direction[0]
			end_col = start_col + direction[1]

			# make sure the move is within the board limits
			if 0 <= end_row < 8 and 0 <= end_col < 8:
				# If the destination is empty add move
				if board[end_row][end_col] is None:
					possible_moves.append(Move(self, (start_row, start_col), (end_row, end_col)))
				# If the destination has a enemy then we can capture it
				elif board[end_row][end_col].color != self.color:
					possible_moves.append(Move(self, (start_row, start_col), (end_row, end_col)))

		return possible_moves