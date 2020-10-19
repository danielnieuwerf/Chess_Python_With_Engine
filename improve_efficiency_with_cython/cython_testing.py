import game_c
import timeit
from Game import Game
import endgames_cy

g = Game()

print(g.legal_moves())

my_setup = """

"""

code = """
g = Game();
g.legal_moves()
"""

py = timeit.timeit(code, setup="from Game import Game", number= 1000)
cy = timeit.timeit(code, setup="from game_c import Game", number= 1000)


print("C is {} times faster than Python".format(py/cy))