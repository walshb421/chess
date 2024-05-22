class Move:
    def __init__(self, piece, src, dst, special = None):
        self.piece = piece
        self.src = src
        self.dst = dst
        self.special = special  # Can be 'en_passant' or 'castling'