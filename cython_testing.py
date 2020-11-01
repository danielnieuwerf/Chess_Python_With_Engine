import pyximport; pyximport.install()
import timeit
from Game import Game
from CythonGame import Game

my_setup = """

"""

code = """
g = Game();
engine_move = g.engine_move_decision(1)
g.board.make_move(engine_move[0],engine_move[1],engine_move[2],engine_move[3])   # Make move
g.handle_new_successfully_made_move(engine_move)
"""

while True:
    py = timeit.timeit(code, setup="from Game import Game", number= 1000)
    cy = timeit.timeit(code, setup="from CythonGame import Game", number= 1000)


    print("C is {} times faster than Python".format(py/cy))