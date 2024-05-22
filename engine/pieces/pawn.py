from .piece import Piece
from move import Move

class Pawn(Piece):
	def __init__(self, color, position):
		super().__init__(color, 'Pawn', position)

	def generate_moves(self, board, moves, turn, flags):
		possible_moves = []
		start_row, start_col = self.position

		# Determine the direction based on the pawn color
		if self.color == 'light':
			direction = -1
		else:
			direction = 1

		# Add the one step forward move
		if board[start_row + direction][start_col] is None:
			possible_moves.append(Move(self, (start_row, start_col), (start_row + direction, start_col)))

		# Check if the pawn can move two steps forward and add the move
		if (start_row == 6 and self.color == 'light') or (start_row == 1 and self.color == 'dark'):
			# Check if the square in front of the pawn is empty
			if board[start_row + direction][start_col] is None:
				if board[start_row + 2 * direction][start_col] is None:
					possible_moves.append(Move(self, (start_row, start_col), (start_row + 2 * direction, start_col)))

		# Check if the pawn can capture diagonally
		# Check each column to the left and right of the pawn
		for col in [start_col - 1, start_col + 1]:
			if 0 <= col < 8:
				if board[start_row + direction][col] is not None and board[start_row + direction][col].color != self.color:
					possible_moves.append(Move(self, (start_row, start_col), (start_row + direction, col)))

        # Check if en passant is possible
		if turn > 0:
			last_move = moves[turn - 1]
			last_start_row, last_start_col = last_move.src
			last_end_row, last_end_col = last_move.dst

			if last_move.piece.type == 'Pawn' and abs(last_start_row - last_end_row) == 2:
				if self.color == 'light' and start_row == 3 and last_end_row == 3 and abs(start_col - last_end_col) == 1:
					possible_moves.append(Move(self, (start_row, start_col), (last_end_row - 1, last_end_col), 'en_passant'))
				elif self.color == 'dark' and start_row == 4 and last_end_row == 4 and abs(start_col - last_end_col) == 1:
					possible_moves.append(Move(self, (start_row, start_col), (last_end_row + 1, last_end_col), 'en_passant'))

		return possible_moves
