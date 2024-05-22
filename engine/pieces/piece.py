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

    def generate_moves(self, board, moves, turn, flags):
        return []

    def piece_to_dict(self):
        return {
            "type": self.type,
            "team": self.color
        }