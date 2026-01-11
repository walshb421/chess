"""
Test fixtures for chess board positions using FEN notation.

FEN Format: [piece placement] [active color] [castling rights] [en passant] [halfmove] [fullmove]
- Piece placement: 8 ranks separated by /, lowercase = black, uppercase = white
- Active color: w or b
- Castling rights: KQkq or - if none
- En passant: target square or - if none
- Halfmove clock: moves since pawn move/capture
- Fullmove number: increments after black's move
"""

POSITIONS = {
    # Basic positions
    "starting": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    "empty": "8/8/8/8/8/8/8/8 w - - 0 1",
    
    # Checkmate positions
    "fools_mate": "rnb1kbnr/pppp1ppp/4p3/8/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3",
    "scholars_mate": "r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4",
    "back_rank_mate": "6k1/5ppp/8/8/8/8/8/R3K3 b Q - 0 1",
    "smothered_mate": "r5rk/6pp/7N/8/8/8/8/4K3 b - - 0 1",
    
    # Special moves - En Passant
    "en_passant_white": "rnbqkbnr/ppp1p1pp/8/3pPp2/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 3",
    "en_passant_black": "rnbqkbnr/pppp1ppp/8/8/3Pp3/8/PPP1PPPP/RNBQKBNR b KQkq d3 0 3",
    
    # Special moves - Castling
    "castling_available": "r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1",
    "castling_kingside_only": "r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w Kk - 0 1",
    "castling_queenside_only": "r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w Qq - 0 1",
    "castling_white_only": "r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQ - 0 1",
    "castling_none": "r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w - - 0 1",
    
    # Check scenarios
    "white_in_check": "rnbqkbnr/ppppp1pp/8/5p1Q/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 1 2",
    "black_in_check": "rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2",
    "double_check": "4k3/8/8/8/1b6/8/2N5/4K2R w K - 0 1",
    "pinned_piece": "rnb1kbnr/pppp1ppp/8/4p3/7q/5NP1/PPPPP2P/RNBQKB1R w KQkq - 0 1",
    
    # Pawn promotion
    "promotion_ready_white": "8/P7/8/8/8/8/8/4K2k w - - 0 1",
    "promotion_ready_black": "4K2k/8/8/8/8/8/p7/8 b - - 0 1",
    "promotion_with_capture": "1n6/P7/8/8/8/8/8/4K2k w - - 0 1",
    
    # Stalemate positions
    "stalemate": "k7/8/1K6/8/8/8/8/8 b - - 0 1",
    "stalemate_complex": "7k/8/6Q1/8/8/8/8/K7 b - - 0 1",
    
    # Endgame positions
    "king_rook_vs_king": "8/8/8/8/8/8/8/R3K2k w - - 0 1",
    "king_queen_vs_king": "8/8/8/8/8/8/8/Q3K2k w - - 0 1",
    "king_pawn_endgame": "8/8/8/8/8/4k3/4P3/4K3 w - - 0 1",
}

# Fixture categories for UI organization
CATEGORIES = {
    "Basic": ["starting", "empty"],
    "Checkmates": ["fools_mate", "scholars_mate", "back_rank_mate", "smothered_mate"],
    "En Passant": ["en_passant_white", "en_passant_black"],
    "Castling": ["castling_available", "castling_kingside_only", "castling_queenside_only", "castling_white_only", "castling_none"],
    "Check": ["white_in_check", "black_in_check", "double_check", "pinned_piece"],
    "Promotion": ["promotion_ready_white", "promotion_ready_black", "promotion_with_capture"],
    "Stalemate": ["stalemate", "stalemate_complex"],
    "Endgames": ["king_rook_vs_king", "king_queen_vs_king", "king_pawn_endgame"],
}

def get_fixture(name):
    """Get a FEN string by fixture name."""
    if name not in POSITIONS:
        raise ValueError(f"Unknown fixture: {name}")
    return POSITIONS[name]

def get_all_fixtures():
    """Get all fixtures organized by category."""
    return {
        "positions": POSITIONS,
        "categories": CATEGORIES
    }
