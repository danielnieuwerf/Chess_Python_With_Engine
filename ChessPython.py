from menu import *
import threading
import cProfile

# Testing

"""
def abcd():
    g = Game()
    x = 0
    while x<1000:
        g.legal_moves()
        x +=1

cProfile.run("abcd()")

time1 = time.time()
abcd()
time2 = time.time()
print("abcd took", time2 - time1)


while True:
    g = Game()
    g.move_number = 69
    for i in range(8):
        for j in range(8):
            g.board.pieces[i][j] = '.'

    g.board.pieces[3][0] = 'k'
    g.board.pieces[6][1] = 'R'
    g.board.pieces[2][2] = 'K'
    g.white_turn = True
    g.board.scores.white_pawns_count = [0,0,0,0,0,0,0,0]
    g.board.scores.black_pawns_count = [0,0,0,0,0,0,0,0]
    g.board.black_king_position = [3,0]
    g.board.white_king_position = [2,2]
    print("pieces string: ", g.board.get_pieces_string())
    print("pos eval", g.evaluate_position_score())
    g.out_of_book = True


    New_Game_Test(g, True,True)

"""

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
Add idea of pass pawns to score function

IMPROVEMENTS:
Add a game over screen instead of returning out of the new game function

Game over screen:
Option to save the game
Option to replay the game

"""

