# Acts as the board/game 
from game import Game
from pieces.pawn import Pawn
from pieces.rook import Rook
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.queen import Queen
from pieces.king import King
from move import Move
import json

columns = ["a", "b", "c", "d", "e", "f", "g", "h"]
rows = ["8", "7", "6", "5", "4", "3", "2", "1"]

class ChessBoard(Game):
	def __init__(self):
		super().__init__()
		self.reset()
		self.add_callback("move", self.move_piece)
		self.add_callback("connect", lambda object : self.game_to_json())
		self.add_callback("reset", lambda object : self.reset())

	def reset(self):
		self.turn = -1
		self.moves = []
		self.board = self.create_starting_board()
		self.turn += 1
		self.captured_whites = []
		self.captured_blacks = []

		self.white_king_moved = False
		self.black_king_moved = False
		self.white_rook_a_moved = False
		self.white_rook_h_moved = False
		self.black_rook_a_moved = False
		self.black_rook_h_moved = False
		return self.game_to_json()

	def create_starting_board(self):
		# Make basic 8x8 board
		board = [[None for i in range(8)] for i in range(8)]

		# Create Pawns
		for column in range(8):
			board[1][column] = Pawn('dark', (1, column))
			board[6][column] = Pawn('light', (6, column))

		# Create Rooks
		board[0][0] = Rook('dark', (0, 0))
		board[0][7] = Rook('dark', (0, 7))

		board[7][0] = Rook('light', (7, 0))
		board[7][7] = Rook('light', (7, 7))

		# Create Knights
		board[0][1] = Knight('dark', (0, 1))
		board[0][6] = Knight('dark', (0, 6))
		board[7][1] = Knight('light', (7, 1))
		board[7][6] = Knight('light', (7, 6))

		# Create Bishops
		board[0][2] = Bishop('dark', (0, 2))
		board[0][5] = Bishop('dark', (0, 5))
		board[7][2] = Bishop('light', (7, 2))
		board[7][5] = Bishop('light', (7, 5))

		# Create Queens
		board[0][3] = Queen('dark', (0, 3))
		board[7][3] = Queen('light', (7, 3))

		# Create Kings
		board[0][4] = King('dark', (0, 4))
		board[7][4] = King('light', (7, 4))

		return board
	
	# Print board to console
	def print_board(self):
		for row in self.board:
			print(' '.join(['.' if square is None else str(square) for square in row]))

	# convert 2d array of board state and info to json
	def game_to_json(self):
		board_obj = {}
		for i in range(8):
			for j in range(8):
				key = columns[j] + rows[i]
				if self.board[i][j]:
					board_obj[key] = self.board[i][j].piece_to_dict()
				else:
					board_obj[key] = "."

		captured_white = [str(piece) for piece in self.captured_whites]
		captured_black = [str(piece) for piece in self.captured_blacks]

		# Create a dictionary to hold all game data
		game_state = {
			'board': board_obj,
			'captured_white': captured_white,
			'captured_black': captured_black
		}

		return json.dumps(game_state)
	
	# Checks if a piece can legally be moved to the square the user has requested
	def can_move_piece(self, start_pos, end_pos):
		# Convert chess moves to coordinates
		start_row, start_col = self.convert_to_index(start_pos)
		end_row, end_col = self.convert_to_index(end_pos)
		piece = self.board[start_row][start_col]
		# if piece exists, find its possible moves and see if that move is 
		if piece:
			possible_moves = piece.generate_moves(self.board, self.moves, self.turn, self.get_castling_flags())
			for move in possible_moves:
				if move.dst == (end_row, end_col):
					return self.validate_move(move);
		return {'valid': False, 'special': None}
	
	def validate_move(self, move):
		start_row, start_col = move.src
		end_row, end_col = move.dst
		if move.special == 'en_passant':
			if self.en_passant_check(move.piece, start_row, start_col, end_row, end_col):
				return {'valid': True, 'special': 'en_passant'}
		if move.special == 'castling':
			if self.castling_check(move.piece, start_row, start_col, end_row, end_col):
				return {'valid': True, 'special': 'castling'}
		return {'valid': True, 'special': None}
	
	def en_passant_check(self, pawn, start_row, start_col, end_row, end_col):
		# Check if the piece is a pawn
		if pawn.type != 'Pawn':
			return False
		# Check if the pawn is captured or at the correct position
		if pawn.is_captured or pawn.position != (start_row, start_col):
			return False
		# Main logic for en passant
		if self.turn > 0:
			last_move = self.moves[self.turn - 1]
			last_start_row, last_start_col = last_move.src
			last_end_row, last_end_col = last_move.dst
			if abs(last_start_row - last_end_row) == 2 and abs(start_col - last_end_col) == 1:
				if pawn.color == 'light' and start_row == 3 and end_row == 2 and end_col == last_end_col:
					return True
				elif pawn.color == 'dark' and start_row == 4 and end_row == 5 and end_col == last_end_col:
					return True
		
		return False
	
	def castling_check(self, king, start_row, start_col, end_row, end_col):
		# Check if the king has moved before
		if king.type != 'King':
			return False
		# Check if the king has moved before or if the rooks have moved before 
		if king.color == 'light':
			if self.white_king_moved:
				return False
			# Check moving left or right and if the rook has moved
			if end_col - start_col == 2 and self.white_rook_h_moved:
				return False
			if end_col - start_col == -2 and self.white_rook_a_moved:
				return False
		else:
			# Check if the black king has moved before
			if self.black_king_moved:
				return False
			# Check if the black rooks have moved before
			# Check moving left or right and if the rook has moved
			if end_col - start_col == 2 and self.black_rook_h_moved:
				return False
			if end_col - start_col == -2 and self.black_rook_a_moved:
				return False

		# Check if the path between the king and the rook is clear
		if end_col - start_col == 2:  # Kingside castling
			for col in range(start_col + 1, end_col):
				if self.board[start_row][col] is not None:
					return False
		elif end_col - start_col == -2:  # Queenside castling
			for col in range(end_col + 1, start_col):
				if self.board[start_row][col] is not None:
					return False

		# TODO: Check if the king is in check, passes through check, or ends up in check

		return True

	def get_castling_flags(self):
		return {
			'white_king_moved': self.white_king_moved,
			'black_king_moved': self.black_king_moved,
			'white_rook_a_moved': self.white_rook_a_moved,
			'white_rook_h_moved': self.white_rook_h_moved,
			'black_rook_a_moved': self.black_rook_a_moved,
			'black_rook_h_moved': self.black_rook_h_moved
	}

	# Moves a piece and sees if it has captured anything in the process
	def move_piece(self, move):
		start_pos = move['source']
		end_pos = move['destination']
		move_info = self.can_move_piece(start_pos, end_pos)

		if(move_info['valid']):
			# Convert chess moves to coordinates
			start_row, start_col = self.convert_to_index(start_pos)
			end_row, end_col = self.convert_to_index(end_pos)
			moving_piece = self.board[start_row][start_col]

			# Create a Move object
			move_obj = Move(moving_piece, (start_row, start_col), (end_row, end_col), move_info['special'])
			self.record_move(move_obj)

			# Set flags if a king or rook is moved
			if moving_piece.type == 'King':
				if moving_piece.color == 'light':
					self.white_king_moved = True
				else:
					self.black_king_moved = True
			elif moving_piece.type == 'Rook':
				if start_col == 0:
					if moving_piece.color == 'light':
						self.white_rook_a_moved = True
					else:
						self.black_rook_a_moved = True
				elif start_col == 7:
					if moving_piece.color == 'light':
						self.white_rook_h_moved = True
					else:
						self.black_rook_h_moved = True

			# Check if the move is en passant
			if move_obj.special == 'en_passant':
				if moving_piece.color == 'light':
					captured_row = end_row + 1
				else:
					captured_row = end_row - 1
				captured_col = end_col
				captured_piece = self.board[captured_row][captured_col]
				self.capture_piece(captured_piece)
				self.board[captured_row][captured_col] = None

			# Check if the move is castling
			elif move_obj.special == 'castling':
				# Check Kingside castling
				if end_col - start_col == 2:
					rook_start_col = 7
					rook_end_col = end_col - 1
				else:  # Queenside castling
					rook_start_col = 0
					rook_end_col = end_col + 1

				rook = self.board[start_row][rook_start_col]
				self.board[start_row][rook_end_col] = rook
				self.board[start_row][rook_start_col] = None

				# Update the rook's position
				rook.position = (start_row, rook_end_col)

			else: # If the move is not special, then we try to capture a piece if not then move
				captured_piece = self.board[end_row][end_col]
				if captured_piece:
					self.capture_piece(captured_piece)

			# Move the piece to the new location
			self.board[end_row][end_col] = moving_piece
			# Remove the piece from the old location
			self.board[start_row][start_col] = None

			# Update the piece's position
			moving_piece.position = (end_row, end_col)	

		return self.game_to_json()

	def capture_piece(self, piece):
		piece.capture()
		if piece.color == 'light':
			self.captured_whites.append(piece)
		else:
			self.captured_blacks.append(piece)


	# we only use chess notation here bruv
	def convert_to_index(self, position):
		column, row = position
		col_idx = ord(column) - ord('a')
		row_idx = 8 - int(row)
		return row_idx, col_idx
