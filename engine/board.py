# Acts as the board/game 
from pieces import Pawn
import json

columns = ["A", "B", "C", "D", "E", "F", "G", "H"]
rows = ["8", "7", "6", "5", "4", "3", "2", "1"]

class ChessBoard:
	def __init__(self):
		self.board = self.create_starting_board()
		self.captured_whites = []
		self.captured_blacks = []

	def create_starting_board(self):
		# Make basic 8x8 board
		board = [[None for i in range(8)] for i in range(8)]

		# Create Pawns
		for column in range(8):
			board[1][column] = Pawn('black', (1, column))
			board[6][column] = Pawn('white', (6, column))
		return board
	
	# Print board to console
	def print_board(self):
		for row in self.board:
			print(' '.join(['.' if square is None else str(square) for square in row]))

	# convert 2d array of board state and info to json
	def game_to_json(self):
		board_obj = {}
		#for row in self.board:
			##row_arr = ['.' if square is None else str(square) for square in row]
			#board_arr.append(row_arr)

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
			if (self.board[start_row][start_col].validate_Move(start_row, start_col, end_row, end_col, self.board)):
				return True
		return False

	# Moves a piece and sees if it has captured anything in the process
	def move_piece(self, start_pos, end_pos):
		# Convert chess moves to coordinates
		start_row, start_col = self.convert_to_index(start_pos)
		end_row, end_col = self.convert_to_index(end_pos)

		# See if there was a piece there
		if self.board[end_row][end_col] is not None:
			captured_piece = self.board[end_row][end_col]
			captured_piece.capture()

			if captured_piece.color == 'white':
				self.captured_whites.append(captured_piece)
			else:
				self.captured_blacks.append(captured_piece)

		self.board[end_row][end_col] = self.board[start_row][start_col]
		self.board[start_row][start_col] = None

	# we only use chess notation here bruv
	def convert_to_index(self, position):
		column, row = position
		col_idx = ord(column) - ord('a')
		row_idx = 8 - int(row)
		return row_idx, col_idx