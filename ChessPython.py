from menu import *
import threading
import cProfile


# Testing

"""
# C profile engine decision
def abcd():
    x = 0
    while x<50:
        g = Game()
        g.out_of_book = True
        engine_move = g.engine_move_decision(1)
        g.board.make_move(engine_move[0],engine_move[1],engine_move[2],engine_move[3])   # Make move
        g.handle_new_successfully_made_move(engine_move)
        x +=1

cProfile.run("abcd()")

time1 = time.time()
abcd()
time2 = time.time()
print("abcd took", time2 - time1)
"""


"""
# END GAME TESTING
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
    print(g.white_won)
"""

# Create menu
Menu()


"""
BUGS:
in engine decision logic it is printing checkmate to console when checkmates are impossible within the search depth
  
Engine stalemated instead of winning and believed stalemate was victory
"""


"""
CYTHON IMPROVEMENTS:
Most expensive functions are legal_moves() function
Rewrite this in Cython


"""