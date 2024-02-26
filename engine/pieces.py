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

	def __str__(self):
		return self.type[0]

class Pawn(Piece):
	def __init__(self, color, position):
		super().__init__(color, 'Pawn', position)

	def __str__(self):
		return 'p'