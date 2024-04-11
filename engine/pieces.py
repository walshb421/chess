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

	def validate_Move(self, start_row, start_col, end_row, end_col, board, moves, turn):
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

		# en passant validation
		if (turn > 0):
			last_move = moves[turn - 1] 
			last_start_pos, last_end_pos = last_move['src'], last_move['dst']
			# Check if the last move was made by a pawn moving two squares
			if abs(last_start_pos[0] - last_end_pos[0]) == 2 and abs(last_start_pos[1] - last_end_pos[1]) == 0:
				# Check if the current pawn is adjacent to the position the pawn moved to
				if abs(start_col - last_end_pos[1]) == 1:
					if self.color == 'light' and start_row == 3 and end_row == 2 and end_col == last_end_pos[1]:
						return True
					elif self.color == 'dark' and start_row == 4 and end_row == 5 and end_col == last_end_pos[1]:
						return True
		return False
	
class Bishop(Piece):
	def __init__(self, color, position):
		super().__init__(color, 'Bishop', position)

	def validate_Move(self, start_row, start_col, end_row, end_col, board, moves, turn):
		# Ensure the move is within the board limits
		if not (0 <= end_col and end_col < 8 and 0 <= end_row and end_row < 8):
			return False
		
		# Ensure the move is diagonal, abs difference will be equal if diagonal movement
		if (abs(end_row - start_row) != abs(end_col - start_col)):
			return False
		
		# Figure out where bishop is moving directionally for row and col
		if (end_row > start_row):
			row_step = 1
		else: row_step = -1

		if (end_col > start_col):
			col_step = 1
		else: col_step = -1

		# Look for pieces blocking path
		steps = abs(end_row - start_row) # same in any direction
		for i in range(1, steps):
			row = start_row + i * row_step # multiply for direction
			col = start_col + i * col_step
			if board[row][col] is not None: # Path is blocked
				return False
			
		# Ensure the destination is not occupied by our own piece
		if (board[end_row][end_col] is not None and board[end_row][end_col].color == self.color):
			return False
		
		# If we get here, move is valid
		return True

class King(Piece):
	def __init__(self, color, position):
		super().__init__(color, 'King', position)
	
	def validate_Move(self, start_row, start_col, end_row, end_col, board, moves, turn):
		# Ensure the move is within the board limits
		if not (0 <= end_col and end_col < 8 and 0 <= end_row and end_row < 8):
			return False
		
		# Check if move is more than 1 away from any direction
		if abs(end_row - start_row) > 1 or abs(end_col - start_col) > 1:
			return False
		
		# Ensure the destination is not occupied by our own piece
		if (board[end_row][end_col] is not None and board[end_row][end_col].color == self.color):
			return False
		
		# If we get here, move is valid
		return True

class Queen(Piece):
	def __init__(self, color, position):
		super().__init__(color, 'Queen', position)

	def validate_Move(self, start_row, start_col, end_row, end_col, board, moves, turn):
		# Ensure the move is within the board limits
		if not (0 <= end_col and end_col < 8 and 0 <= end_row and end_row < 8):
			return False
		
		# Check if the move is vertical or horizontal
		if (start_col == end_col or start_row == end_row):
			# Validate vertical moves
			if (start_col == end_col):
				# If we moving down
				if (start_row < end_row):
					for row in range(start_row + 1, end_row, 1):
						if board[row][start_col] is not None: # Path is blocked
							return False
				# If we moving up
				elif (start_row > end_row):
					for row in range(start_row - 1, end_row, -1):
						if board[row][start_col] is not None: # path is blocked
							return False
						
			# Validate horizontal moves
			if (start_row == end_row):
				# If we moving right
				if (start_col < end_col):
					for col in range(start_col + 1, end_col, 1):
						if board[start_row][col] is not None: # Path is blocked
							return False
				# Moving left
				elif (start_col > end_col):
					for col in range(start_col - 1, end_col, -1):
						if board[start_row][col] is not None: # Path is blocked
							return False			
		# Check if move is diagonal
		elif (abs(end_row - start_row) == abs(end_col - start_col)):
			# Figure out where queen is moving directionally for row and col
			if (end_row > start_row):
				row_step = 1
			else: row_step = -1

			if (end_col > start_col):
				col_step = 1
			else: col_step = -1

			# Look for pieces blocking path
			steps = abs(end_row - start_row) # same in any direction
			for i in range(1, steps):
				row = start_row + i * row_step # multiply for direction
				col = start_col + i * col_step
				if board[row][col] is not None: # Path is blocked
					return False
		# If move isnt vertical or diagonal cant do
		else:
			return False
		
		# Ensure the destination is not occupied by our own piece
		if (board[end_row][end_col] is not None and board[end_row][end_col].color == self.color):
			return False
		
		# If we get here, move is valid
		return True


class Knight(Piece):
	def __init__(self, color, position):
		super().__init__(color, 'Knight', position)

	def validate_Move(self, start_row, start_col, end_row, end_col, board, moves, turn):
 		# Ensure the move is within the board limits
		if not (0 <= end_col and end_col < 8 and 0 <= end_row and end_row < 8):
			return False
		
		# Find how far the ending spots are for row and col
		row_distance = abs(end_row - start_row)
		col_distance = abs(end_col - start_col)

		# Check if the move is 2 row 1 column move or 2 column row move, which effectively checks all 8 L shape directions
		if not ((row_distance == 2 and col_distance == 1) or (row_distance == 1 and col_distance == 2)):
			return False
		
		# Ensure the destination is not occupied by our own piece
		if (board[end_row][end_col] is not None and board[end_row][end_col].color == self.color):
			return False

		# Move is valid if none of the conditions above are met
		return True
		


class Rook(Piece):
	def __init__(self, color, position):
		super().__init__(color, 'Rook', position)
	
	def validate_Move(self, start_row, start_col, end_row, end_col, board, moves, turn):
 		# Ensure the move is within the board limits
		if not (0 <= end_col and end_col < 8 and 0 <= end_row and end_row < 8):
			return False
		
		# Ensure the move is either horizontal or vertical
		if (start_col != end_col and start_row != end_row):
			return False

		# Validate vertical moves
		if (start_col == end_col):
			# If we moving down
			if (start_row < end_row):
				for row in range(start_row + 1, end_row, 1):
					if board[row][start_col] is not None: # Path is blocked
						return False
			# If we moving up
			elif (start_row > end_row):
				for row in range(start_row - 1, end_row, -1):
					if board[row][start_col] is not None: # path is blocked
						return False
					
		# Validate horizontal moves
		if (start_row == end_row):
			# If we moving right
			if (start_col < end_col):
				for col in range(start_col + 1, end_col, 1):
					if board[start_row][col] is not None: # Path is blocked
						return False
			# Moving left
			elif (start_col > end_col):
				for col in range(start_col - 1, end_col, -1):
					if board[start_row][col] is not None: # Path is blocked
						return False
		
		# Ensure the destination is not occupied by our own piece
		if (board[end_row][end_col] is not None and board[end_row][end_col].color == self.color):
			return False

		# Move is valid if none of the conditions above are met
		return True
		
