from .piece import Piece
from move import Move

class King(Piece):
	def __init__(self, color, position):
		super().__init__(color, 'King', position)

	def generate_moves(self, board, moves, turn, flags):
		possible_moves = []
		start_row, start_col = self.position

		# Check each direction the king can move
		for direction in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
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

        # Castling moves
		if not self.is_captured:
			# Check the white king side castling
			if self.color == 'light' and not flags['white_king_moved']:
				king_start_row, king_start_col = 7, 4
				# Check if the king is in the starting position
				if self.position == (king_start_row, king_start_col):
					# Check if we are castling on queen side
					# Check if the rook is in the starting position
					if not flags['white_rook_a_moved'] and board[7][0] is not None and board[7][0].type == 'Rook':
						# Check if the squares between the king and the rook are empty
						if board[7][1] is None and board[7][2] is None and board[7][3] is None:
							# TODO Check if the king is not in check
							possible_moves.append(Move(self, (start_row, start_col), (7, 2), 'castling'))

					# Check if we are castling on king side
	 				# Check if the rook is in the starting position	
					if not flags['white_rook_h_moved'] and board[7][7] is not None and board[7][7].type == 'Rook':
						# Check if the squares between the king and the rook are empty
						if board[7][5] is None and board[7][6] is None:
							# TODO Check if the king is not in check
							possible_moves.append(Move(self, (start_row, start_col), (7, 6), 'castling'))

			# Check the black king side castling
			elif self.color == 'dark' and not flags['black_king_moved']:
				king_start_row, king_start_col = 0, 4
				# Check if the king is in the starting position
				if self.position == (king_start_row, king_start_col):
					# Check if we are castling on queen side
					if not flags['black_rook_a_moved'] and board[0][0] is not None and board[0][0].type == 'Rook':
						# Check if the squares between the king and the rook are empty
						if board[0][1] is None and board[0][2] is None and board[0][3] is None:
							# TODO Check if the king is not in check
							possible_moves.append(Move(self, (start_row, start_col), (0, 2), 'castling'))
					
					# Check if we are castling on king side
					if not flags['black_rook_h_moved'] and board[0][7] is not None and board[0][7].type == 'Rook':
						# Check if the squares between the king and the rook are empty
						if board[0][5] is None and board[0][6] is None:
							# TODO Check if the king is not in check
							possible_moves.append(Move(self, (start_row, start_col), (0, 6), 'castling'))
		
		return possible_moves
