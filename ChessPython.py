from menu import *

# Testing
from bitboard import *
"""
test_board = CharBoard()        
test_board.pieces = [['R', 'N', 'B', 'K', 'Q', 'B', 'N', 'R'],
                       ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                       ['.', '.', '.', '.', '.', '.', '.', '.'],
                       ['b', '.', '.', 'r', '.', '.', '.', '.'],
                       ['.', '.', '.', 'Q', 'p', 'q', 'k', '.'],
                       ['.', '.', '.', '.', '.', '.', '.', '.'],
                       ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                       ['r', 'n', 'b', '.', 'q', 'b', 'n', 'r']
                      ]
test_board.white_king_position = [0,3]
test_board.black_king_position = [4,6]

white_threats = test_board.create_bitboard_direct_threats_to_king(True)
black_threats =  test_board.create_bitboard_direct_threats_to_king(False)
white_shields = test_board.create_bitboard_shields_to_king(True)
black_shields = test_board.create_bitboard_shields_to_king(False)
print("white threats")
white_threats.print()
print("Black threats")
black_threats.print()
print("white shields")
white_shields.print()
print("Black shields")
black_shields.print()
"""


# Menu
Menu()



"""
BUGS:
Threat by pawns slightly dodgy when pieces captured
when pawn captures pawn

in engine decision logic it is printing checkmate to console when checkmates are impossible within the search depth

Engine did not stop mate in one

Engine stalemated instead of winning


DO depth 4 before doing depth 3 with alpha beta pruning


current moves and off them branches of possible boards 


Add idea of outposts to score function


"""
