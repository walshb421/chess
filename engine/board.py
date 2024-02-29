# Acts as the board for the game
from pieces import Pawn
import json

class ChessBoard:
	def __init__(self):
		self.board = self.create_starting_board()

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

	# convert 2d array of board to json string
	def board_to_json(self):
		board_arr = []
		for row in self.board:
			row_arr = ['.' if square is None else str(square) for square in row]
			board_arr.append(row_arr)
		return json.dumps(board_arr)

	# naive approach for moving a piece without validation
	def move_piece(self, start_pos, end_pos):
		start_row, start_col = self.convert_to_index(start_pos)
		end_row, end_col = self.convert_to_index(end_pos)
		#print(f'start row: {start_row}, start col: {start_col}, end row: {end_row}, end col: {end_col}')
		self.board[end_row][end_col] = self.board[start_row][start_col]
		self.board[start_row][start_col] = None

	# we only use chess notation here bruv
	def convert_to_index(self, position):
		column, row = position
		col_idx = ord(column) - ord('a')
		row_idx = 8 - int(row)
		return row_idx, col_idx