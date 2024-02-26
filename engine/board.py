class ChessBoard:
	def __init__(self):
		self.board = self.create_starting_board()

	def create_starting_board(self):
		return [[None for i in range(8)] for i in range(8)]

	def print_board(self):
		for row in self.board:
			print(' '.join(['-' if square is None else square for square in row]))