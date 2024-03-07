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

class Pawn(Piece):
	def __init__(self, color, position):
		super().__init__(color, 'Pawn', position)

	def validate_Move(self, start_row, start_col, end_row, end_col, board):
		# Check if white pawn just moving up one square 
		if self.color == 'light' and end_row == start_row - 1 and board[end_row][end_col] == None and end_col == start_col:
			return True
		elif self.color == 'dark' and end_row == start_row + 1 and board[end_row][end_col] == None and end_col == start_col:
			return True

		# Check if they doing a double move
		if self.color == 'light' and end_row == start_row - 2 and board[end_row][end_col] == None and end_col == start_col and start_row == 6:
			return True
		elif self.color == 'dark' and end_row == start_row + 2 and board[end_row][end_col] == None and end_col == start_col and start_row == 1:
			return True
		
		# Check for capture
		if self.color == 'light' and end_row == start_row - 1 and board[end_row][end_col] and ((end_col == start_col + 1 and start_col + 1 < 8) or (end_col == start_col - 1 and start_col - 1 > -1)):
			# Set the other object 
			return True
		elif self.color == 'dark' and end_row == start_row + 1 and board[end_row][end_col] and ((end_col == start_col + 1 and start_col + 1 < 8) or (end_col == start_col - 1 and start_col - 1 > -1)):
			return True

		#TODO en passant

		return False
	
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
	
	def validate_Move(self, start_row, start_col, end_row, end_col, board):
		# Check if the move is within bounds of the board
		if not (0 <= end_col and end_col < 8 and 0 <= end_row and end_row < 8):
			return False
		
		# Check if move isn't up down left or right, then it isn't valid
		if (start_col != end_col and start_row != end_row):
			print("isnt horizontal or vetical", flush=True)
			return False

		# If we moving vertically, check that all spots are not blocked leading up to ending square
		if (start_col == end_col):
			# If we moving down
			if (start_row < end_row):
				# Check every spot for a piece blocking the way
				for row in range(start_row + 1, end_row, 1):
					# If blocked
					if board[row][start_col] is not None:
						return False
			# If we moving up
			elif (start_row > end_row):
				# Check spots for blocking pieces
				for row in range(start_row - 1, end_row, -1):
					# If blocked
					if board[row][start_col] is not None:
						return False
					
		# If we moving horizontally, check that spots leading up aren't blocked
		if (start_row == end_row):
			# If we moving right
			if (start_col < end_col):
				# Check if blocked
				for col in range(start_col + 1, end_col, 1):
					if board[start_row][col] is not None:
						return False
			elif (start_col > end_col):
				# Check if blocked
				for col in range(start_col - 1, end_col, -1):
					if board[start_row][col] is not None:
						return False
		
		# Check if that space has one of our own pieces
		if (board[end_row][end_col] is not None and board[end_row][end_col].color == self.color):
			return False

		# If we get here we can move/capture at this space
		return True
		
