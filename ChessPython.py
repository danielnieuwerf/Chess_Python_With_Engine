from menu import *
import threading

# Testing
g = Game()
g.move_number = 69
for i in range(8):
    for j in range(8):
        g.board.pieces[i][j] = '.'

g.board.pieces[2][2] = 'k'
g.board.pieces[3][3] = 'p'
g.board.pieces[1][1] = 'K'
g.board.scores.white_pawns_count = [0,0,0,0,0,0,0,0]
g.board.scores.black_pawns_count = [0,0,0,1,0,0,0,0]
g.board.black_king_position = [2,2]
g.board.white_king_position = [1,1]
print(Kkp(g.board, True))
print()
print("pieces string: ", g.board.get_pieces_string())
print("pos eval", g.evaluate_position_score())

# Create menu
Menu()


"""
BUGS:
Final move needs to be handled with the clock
If gameover pause clock and stop updating it's display


in engine decision logic it is printing checkmate to console when checkmates are impossible within the search depth

Engine did not stop mate in one
  
Engine stalemated instead of winning


DO depth 4 before doing depth 3 with alpha beta pruning

current moves and off them branches of possible boards 

Add idea of outposts to score function

IMPROVEMENTS:
Add a game over screen instead of returning out of the new game function

Game over screen:
Option to save the game
Option to replay the game

"""

