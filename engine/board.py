# Acts as the board/game 
from game import Game
from pieces import Pawn, Rook, Bishop, Knight, Queen, King
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
		# Validate the move
		if (self.board[start_row][start_col] != None): # If space to validate isnt None
			if (self.board[start_row][start_col].validate_Move(start_row, start_col, end_row, end_col, self.board, self.moves, self.turn)):
				return True
		return False
	
	def en_passant_check(self, moving_piece, turn, moves, start_row, start_col, end_row, end_col):
		# en passant validation
		print(turn, flush=True)

		if (turn > 0):
			last_move = moves[turn - 1] 
			last_start_pos, last_end_pos = last_move['src'], last_move['dst']
			# Check if the last move was made by a pawn moving two squares'']
			print(abs(last_start_pos[0] - last_end_pos[0]) == 2, flush=True)
			if abs(last_start_pos[0] - last_end_pos[0]) == 2 and abs(last_start_pos[1] - last_end_pos[1]) == 0:
				# Check if the current pawn is adjacent to the position the pawn moved to
				if abs(start_col - last_end_pos[1]) == 1:
					if moving_piece.color == 'light' and start_row == 3 and end_row == 2 and end_col == last_end_pos[1]:
						return True
					elif moving_piece.color == 'dark' and start_row == 4 and end_row == 5 and end_col == last_end_pos[1]:
						return True
		return False

	# Moves a piece and sees if it has captured anything in the process
	def move_piece(self, move):
		start_pos = move['source']
		end_pos = move['destination']

		if(self.can_move_piece(start_pos, end_pos)):
			# Convert chess moves to coordinates
			start_row, start_col = self.convert_to_index(start_pos)
			end_row, end_col = self.convert_to_index(end_pos)
			moving_piece = self.board[start_row][start_col]
			if moving_piece.type == "Pawn":
				is_en_passant = self.en_passant_check(moving_piece, self.turn, self.moves, start_row, start_col, end_row, end_col)

			# Write history of move
			move_info = {
				'src': (start_row, start_col),
				'dst': (end_row, end_col)
			}
			self.record_move(move_info)


			# If en passant
			print(moving_piece.type, flush=True)
			print(is_en_passant, flush=True)
			if moving_piece.type == "Pawn" and is_en_passant:
				captured_row = start_row
				captured_col = end_col 
				captured_piece = self.board[captured_row][captured_col]
				
				if captured_piece.color == 'light':
					self.captured_whites.append(captured_piece)
				else:
					self.captured_blacks.append(captured_piece)
				
				self.board[captured_row][captured_col] = None

			# If move isn't en passant
			# See if there was a piece there
			elif self.board[end_row][end_col] is not None:
				captured_piece = self.board[end_row][end_col]
				captured_piece.capture()

				if captured_piece.color == 'light':
					self.captured_whites.append(captured_piece)
				else:
					self.captured_blacks.append(captured_piece)

			self.board[end_row][end_col] = self.board[start_row][start_col]
			self.board[start_row][start_col] = None
		return self.game_to_json()
	

	# we only use chess notation here bruv
	def convert_to_index(self, position):
		column, row = position
		col_idx = ord(column) - ord('a')
		row_idx = 8 - int(row)
		return row_idx, col_idx