# General piece class, specific pieces inherit from the piece class

class Piece:
	def __init__(self, color, type, position):
		self.color = color
		self.type = type
		self.position = position
		self.is_captured = False

	def move(self, new_position):
		self.position = new_position
	
	def capture(self):
		self.is_captured = True

	def validate_Move(end_row, end_col):
		return True
	
	def piece_to_dict(self):
		return {
			"type": self.type,
			"team": self.color
		}


	def __str__(self):
		return self.type[0]

class Pawn(Piece):
	def __init__(self, color, position):
		super().__init__(color, 'Pawn', position)

	def validate_Move(self, start_row, start_col, end_row, end_col, board):
		# Check if white pawn just moving up one square (doesn't check if moves out of range)
		if self.color == 'white' and end_row == start_row - 1 and board[end_row][end_col] == None and end_col == start_col:
			return True
		elif self.color == 'black' and end_row == start_row + 1 and board[end_row][end_col] == None and end_col == start_col:
			return True

		# Check if they doing a double move
		if self.color == 'white' and end_row == start_row - 2 and board[end_row][end_col] == None and end_col == start_col and start_row == 6:
			return True
		elif self.color == 'black' and end_row == start_row + 2 and board[end_row][end_col] == None and end_col == start_col and start_row == 1:
			return True
		
		# Check for capture
		if self.color == 'white' and end_row == start_row - 1 and board[end_row][end_col] and ((end_col == start_col + 1 and start_col + 1 < 8) or (end_col == start_col - 1 and start_col - 1 > -1)):
			# Set the other object 
			return True
		elif self.color == 'black' and end_row == start_row + 1 and board[end_row][end_col] and ((end_col == start_col + 1 and start_col + 1 < 8) or (end_col == start_col - 1 and start_col - 1 > -1)):
			return True
		
		return False
	def __str__(self):
		return 'p'
	
class Bishop(Piece):
	def __init__(self, color, position):
		super().__init__(color, 'Bishop', position)

class King(Piece):
	def __init__(self, color, position):
		super().__init__(color, 'King', position)

class Queen(Piece):
	def __init__(self, color, position):
		super().__init__(color, 'Queen', position)

class Knight(Piece):
	def __init__(self, color, position):
		super().__init__(color, 'Knight', position)

class Rook(Piece):
	def __init__(self, color, position):
		super().__init__(color, 'Rook', position)
		
		
