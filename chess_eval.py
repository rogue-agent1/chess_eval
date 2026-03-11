#!/usr/bin/env python3
"""chess_eval — Chess position evaluator with piece-square tables. Zero deps."""

PIECE_VALUES = {'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 20000}

# Piece-square tables (from white's perspective, a1=index 0)
PAWN_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 10,  5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5, -5,-10,  0,  0,-10, -5,  5,
    5, 10, 10,-20,-20, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0,
]

KNIGHT_TABLE = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50,
]

PST = {'P': PAWN_TABLE, 'N': KNIGHT_TABLE}

def parse_fen(fen):
    board = [None] * 64
    parts = fen.split()
    rows = parts[0].split('/')
    for r, row in enumerate(rows):
        c = 0
        for ch in row:
            if ch.isdigit():
                c += int(ch)
            else:
                color = 'w' if ch.isupper() else 'b'
                board[r * 8 + c] = (color, ch.upper())
                c += 1
    return board, parts[1] if len(parts) > 1 else 'w'

def evaluate(board, side='w'):
    score = 0
    material = {'w': 0, 'b': 0}
    for i, piece in enumerate(board):
        if piece is None: continue
        color, ptype = piece
        val = PIECE_VALUES.get(ptype, 0)
        material[color] += val
        # Piece-square bonus
        pst = PST.get(ptype)
        if pst:
            idx = i if color == 'w' else (7 - i // 8) * 8 + (i % 8)
            val += pst[idx]
        score += val if color == 'w' else -val
    return score if side == 'w' else -score, material

def display(board):
    print("    a  b  c  d  e  f  g  h")
    symbols = {'P':'♟','N':'♞','B':'♝','R':'♜','Q':'♛','K':'♚'}
    for r in range(8):
        row = f"  {8-r} "
        for c in range(8):
            piece = board[r * 8 + c]
            if piece:
                color, ptype = piece
                s = symbols.get(ptype, ptype)
                row += f" {s} " if color == 'w' else f"({s})"
            else:
                row += " · " if (r + c) % 2 == 0 else " . "
        print(row)

def main():
    # Starting position
    start = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w"
    board, side = parse_fen(start)
    score, material = evaluate(board, side)
    print("Chess Position Evaluator:\n")
    display(board)
    print(f"\n  Eval: {score/100:+.2f} (white's view)")
    print(f"  Material: W={material['w']/100:.0f} B={material['b']/100:.0f}")

    # After e4 e5 Nf3
    fen2 = "rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b"
    board2, side2 = parse_fen(fen2)
    score2, mat2 = evaluate(board2, 'w')
    print(f"\n  After 1.e4 e5 2.Nf3: {score2/100:+.2f}")

if __name__ == "__main__":
    main()
