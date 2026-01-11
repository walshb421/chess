# Acts as the board/game 
from game import Game
from pieces.pawn import Pawn
from pieces.rook import Rook
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.queen import Queen
from pieces.king import King
from move import Move
from fixtures import POSITIONS, CATEGORIES, get_fixture, get_all_fixtures
import json

columns = ["A", "B", "C", "D", "E", "F", "G", "H"]
rows = ["8", "7", "6", "5", "4", "3", "2", "1"]

# FEN piece mapping
FEN_PIECE_MAP = {
    'p': ('dark', Pawn),
    'r': ('dark', Rook),
    'n': ('dark', Knight),
    'b': ('dark', Bishop),
    'q': ('dark', Queen),
    'k': ('dark', King),
    'P': ('light', Pawn),
    'R': ('light', Rook),
    'N': ('light', Knight),
    'B': ('light', Bishop),
    'Q': ('light', Queen),
    'K': ('light', King),
}

PIECE_TO_FEN = {
    ('dark', 'Pawn'): 'p',
    ('dark', 'Rook'): 'r',
    ('dark', 'Knight'): 'n',
    ('dark', 'Bishop'): 'b',
    ('dark', 'Queen'): 'q',
    ('dark', 'King'): 'k',
    ('light', 'Pawn'): 'P',
    ('light', 'Rook'): 'R',
    ('light', 'Knight'): 'N',
    ('light', 'Bishop'): 'B',
    ('light', 'Queen'): 'Q',
    ('light', 'King'): 'K',
}

class ChessBoard(Game):
    def __init__(self):
        super().__init__()
        self.en_passant_target = None  # Track en passant target square
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.reset()
        self.add_callback("move", lambda object : self.move_piece(object))
        self.add_callback("connect", lambda object : self.game_to_json())
        self.add_callback("reset", lambda object : self.reset())
        self.add_callback("load_fen", lambda object : self.load_fen(object['fen']))
        self.add_callback("load_fixture", lambda object : self.load_fen(get_fixture(object['name'])))
        self.add_callback("get_fixtures", lambda object : self.send_fixtures())

    def reset(self):
        self.turn = -1
        self.moves = []
        self.board = self.create_starting_board()
        self.turn += 1
        self.captured_whites = []
        self.captured_blacks = []
        self.en_passant_target = None
        self.halfmove_clock = 0
        self.fullmove_number = 1

        self.white_king_moved = False
        self.black_king_moved = False
        self.white_rook_a_moved = False
        self.white_rook_h_moved = False
        self.black_rook_a_moved = False
        self.black_rook_h_moved = False
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

    def load_fen(self, fen_string):
        """
        Parse FEN string and initialize board state.
        
        Args:
            fen_string: Valid FEN notation string
            
        Returns:
            Game state JSON
            
        Raises:
            ValueError: If FEN string is invalid
        """
        try:
            parts = fen_string.strip().split(' ')
            if len(parts) != 6:
                raise ValueError(f"FEN must have 6 parts, got {len(parts)}")
            
            piece_placement, active_color, castling, en_passant, halfmove, fullmove = parts
            
            # Clear the board
            self.board = [[None for _ in range(8)] for _ in range(8)]
            self.moves = []
            self.captured_whites = []
            self.captured_blacks = []
            
            # Parse piece placement
            rank_strs = piece_placement.split('/')
            if len(rank_strs) != 8:
                raise ValueError(f"FEN piece placement must have 8 ranks, got {len(rank_strs)}")
            
            for row, rank_str in enumerate(rank_strs):
                col = 0
                for char in rank_str:
                    if char.isdigit():
                        col += int(char)
                    elif char in FEN_PIECE_MAP:
                        color, piece_class = FEN_PIECE_MAP[char]
                        self.board[row][col] = piece_class(color, (row, col))
                        col += 1
                    else:
                        raise ValueError(f"Invalid FEN character: {char}")
                if col != 8:
                    raise ValueError(f"FEN rank {row + 1} has wrong number of squares")
            
            # Parse active color
            if active_color == 'w':
                self.turn = 0
            elif active_color == 'b':
                self.turn = 1
            else:
                raise ValueError(f"Invalid active color: {active_color}")
            
            # Parse castling rights
            self.white_king_moved = 'K' not in castling and 'Q' not in castling
            self.black_king_moved = 'k' not in castling and 'q' not in castling
            self.white_rook_h_moved = 'K' not in castling
            self.white_rook_a_moved = 'Q' not in castling
            self.black_rook_h_moved = 'k' not in castling
            self.black_rook_a_moved = 'q' not in castling
            
            # Parse en passant target
            if en_passant == '-':
                self.en_passant_target = None
            else:
                col = ord(en_passant[0].lower()) - ord('a')
                row = 8 - int(en_passant[1])
                self.en_passant_target = (row, col)
            
            # Parse halfmove clock and fullmove number
            self.halfmove_clock = int(halfmove)
            self.fullmove_number = int(fullmove)
            
            return self.game_to_json()
            
        except Exception as e:
            raise ValueError(f"Invalid FEN string: {str(e)}")

    def to_fen(self):
        """
        Export current board state as FEN string.
        
        Returns:
            str: Valid FEN notation of current position
        """
        # Piece placement
        fen_ranks = []
        for row in range(8):
            fen_rank = ""
            empty_count = 0
            for col in range(8):
                piece = self.board[row][col]
                if piece is None:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen_rank += str(empty_count)
                        empty_count = 0
                    fen_rank += PIECE_TO_FEN[(piece.color, piece.type)]
            if empty_count > 0:
                fen_rank += str(empty_count)
            fen_ranks.append(fen_rank)
        piece_placement = '/'.join(fen_ranks)
        
        # Active color
        active_color = 'w' if self.turn % 2 == 0 else 'b'
        
        # Castling rights
        castling = ""
        if not self.white_king_moved and not self.white_rook_h_moved:
            castling += 'K'
        if not self.white_king_moved and not self.white_rook_a_moved:
            castling += 'Q'
        if not self.black_king_moved and not self.black_rook_h_moved:
            castling += 'k'
        if not self.black_king_moved and not self.black_rook_a_moved:
            castling += 'q'
        if not castling:
            castling = '-'
        
        # En passant target
        if self.en_passant_target:
            row, col = self.en_passant_target
            en_passant = chr(ord('a') + col) + str(8 - row)
        else:
            en_passant = '-'
        
        # Halfmove clock and fullmove number
        halfmove = str(self.halfmove_clock)
        fullmove = str(self.fullmove_number)
        
        return f"{piece_placement} {active_color} {castling} {en_passant} {halfmove} {fullmove}"

    def send_fixtures(self):
        """Send available fixtures to the client."""
        fixtures_data = get_all_fixtures()
        self.update({'fixtures': fixtures_data})

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

        captured_white = [piece.piece_to_dict() for piece in self.captured_whites]
        captured_black = [piece.piece_to_dict() for piece in self.captured_blacks]

        # Create a dictionary to hold all game data
        game_state = {
            'board': board_obj,
            'captured_white': captured_white,
            'captured_black': captured_black,
            'turn': self.turn,
            'fen': self.to_fen()
        }

        self.update(game_state)
    
    # Checks if a piece can legally be moved to the square the user has requested
    def can_move_piece(self, start_pos, end_pos):
        # Convert chess moves to coordinates
        start_row, start_col = self.convert_to_index(start_pos)
        end_row, end_col = self.convert_to_index(end_pos)
        piece = self.board[start_row][start_col]
        # if piece exists, find its possible moves and see if that move is 
        if piece:
            possible_moves = piece.generate_moves(self.board, self.moves, self.turn, self.get_castling_flags())
            for move in possible_moves:
                if move.dst == (end_row, end_col):
                    return self.validate_move(move);
        return {'valid': False, 'special': None}
    
    def validate_move(self, move):
        start_row, start_col = move.src
        end_row, end_col = move.dst
        if move.special == 'en_passant':
            if self.en_passant_check(move.piece, start_row, start_col, end_row, end_col):
                return {'valid': True, 'special': 'en_passant'}
        if move.special == 'castling':
            if self.castling_check(move.piece, start_row, start_col, end_row, end_col):
                return {'valid': True, 'special': 'castling'}
        return {'valid': True, 'special': None}
    
    def en_passant_check(self, pawn, start_row, start_col, end_row, end_col):
        # Check if the piece is a pawn
        if pawn.type != 'Pawn':
            return False
        # Check if the pawn is captured or at the correct position
        if pawn.is_captured or pawn.position != (start_row, start_col):
            return False
        
        # Check against en_passant_target if set (from FEN)
        if self.en_passant_target:
            if (end_row, end_col) == self.en_passant_target:
                return True
        
        # Main logic for en passant (from move history)
        if self.turn > 0 and len(self.moves) > 0:
            last_move = self.moves[-1]
            last_start_row, last_start_col = last_move.src
            last_end_row, last_end_col = last_move.dst
            if abs(last_start_row - last_end_row) == 2 and abs(start_col - last_end_col) == 1:
                if pawn.color == 'light' and start_row == 3 and end_row == 2 and end_col == last_end_col:
                    return True
                elif pawn.color == 'dark' and start_row == 4 and end_row == 5 and end_col == last_end_col:
                    return True
        
        return False
    
    def castling_check(self, king, start_row, start_col, end_row, end_col):
        # Check if the king has moved before
        if king.type != 'King':
            return False
        # Check if the king has moved before or if the rooks have moved before 
        if king.color == 'light':
            if self.white_king_moved:
                return False
            # Check moving left or right and if the rook has moved
            if end_col - start_col == 2 and self.white_rook_h_moved:
                return False
            if end_col - start_col == -2 and self.white_rook_a_moved:
                return False
        else:
            # Check if the black king has moved before
            if self.black_king_moved:
                return False
            # Check if the black rooks have moved before
            # Check moving left or right and if the rook has moved
            if end_col - start_col == 2 and self.black_rook_h_moved:
                return False
            if end_col - start_col == -2 and self.black_rook_a_moved:
                return False

        # Check if the path between the king and the rook is clear
        if end_col - start_col == 2:  # Kingside castling
            for col in range(start_col + 1, end_col):
                if self.board[start_row][col] is not None:
                    return False
        elif end_col - start_col == -2:  # Queenside castling
            for col in range(end_col + 1, start_col):
                if self.board[start_row][col] is not None:
                    return False

        # TODO: Check if the king is in check, passes through check, or ends up in check

        return True

    def get_castling_flags(self):
        return {
            'white_king_moved': self.white_king_moved,
            'black_king_moved': self.black_king_moved,
            'white_rook_a_moved': self.white_rook_a_moved,
            'white_rook_h_moved': self.white_rook_h_moved,
            'black_rook_a_moved': self.black_rook_a_moved,
            'black_rook_h_moved': self.black_rook_h_moved
        }

    # Moves a piece and sees if it has captured anything in the process
    def move_piece(self, move):
        start_pos = move['source']
        end_pos = move['destination']
        move_info = self.can_move_piece(start_pos, end_pos)

        if(move_info['valid']):
            # Convert chess moves to coordinates
            start_row, start_col = self.convert_to_index(start_pos)
            end_row, end_col = self.convert_to_index(end_pos)
            moving_piece = self.board[start_row][start_col]

            # Create a Move object
            move_obj = Move(moving_piece, (start_row, start_col), (end_row, end_col), move_info['special'])
            self.record_move(move_obj)

            # Update en passant target
            if moving_piece.type == 'Pawn' and abs(start_row - end_row) == 2:
                # Pawn moved two squares, set en passant target
                self.en_passant_target = ((start_row + end_row) // 2, start_col)
            else:
                self.en_passant_target = None

            # Set flags if a king or rook is moved
            if moving_piece.type == 'King':
                if moving_piece.color == 'light':
                    self.white_king_moved = True
                else:
                    self.black_king_moved = True
            elif moving_piece.type == 'Rook':
                if start_col == 0:
                    if moving_piece.color == 'light':
                        self.white_rook_a_moved = True
                    else:
                        self.black_rook_a_moved = True
                elif start_col == 7:
                    if moving_piece.color == 'light':
                        self.white_rook_h_moved = True
                    else:
                        self.black_rook_h_moved = True

            # Check if the move is en passant
            if move_obj.special == 'en_passant':
                if moving_piece.color == 'light':
                    captured_row = end_row + 1
                else:
                    captured_row = end_row - 1
                captured_col = end_col
                captured_piece = self.board[captured_row][captured_col]
                self.capture_piece(captured_piece)
                self.board[captured_row][captured_col] = None

            # Check if the move is castling
            elif move_obj.special == 'castling':
                # Check Kingside castling
                if end_col - start_col == 2:
                    rook_start_col = 7
                    rook_end_col = end_col - 1
                else:  # Queenside castling
                    rook_start_col = 0
                    rook_end_col = end_col + 1

                rook = self.board[start_row][rook_start_col]
                self.board[start_row][rook_end_col] = rook
                self.board[start_row][rook_start_col] = None

                # Update the rook's position
                rook.position = (start_row, rook_end_col)

            else: # If the move is not special, then we try to capture a piece if not then move
                captured_piece = self.board[end_row][end_col]
                if captured_piece:
                    self.capture_piece(captured_piece)

            # Move the piece to the new location
            self.board[end_row][end_col] = moving_piece
            # Remove the piece from the old location
            self.board[start_row][start_col] = None

            # Update the piece's position
            moving_piece.position = (end_row, end_col)

            # Update fullmove number (increments after black's move)
            if self.turn % 2 == 1:
                self.fullmove_number += 1

        return self.game_to_json()

    def capture_piece(self, piece):
        piece.capture()
        if piece.color == 'light':
            self.captured_whites.append(piece)
        else:
            self.captured_blacks.append(piece)


    # we only use chess notation here bruv
    def convert_to_index(self, position):
        column, row = position
        col_idx = ord(column) - ord('A')
        row_idx = 8 - int(row)
        return row_idx, col_idx
