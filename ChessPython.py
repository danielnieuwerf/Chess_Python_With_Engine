from New_Game import *        


# Play games with engines or players
New_Game(white_is_engine = False, black_is_engine = True, white_engine_depth = 1, black_engine_depth = 1)
New_Game(white_is_engine = False, black_is_engine = False, white_engine_depth = 1, black_engine_depth = 1)
New_Game(white_is_engine = True, black_is_engine = True, white_engine_depth = 1, black_engine_depth = 1)
New_Game(white_is_engine = True, black_is_engine = False, white_engine_depth = 1, black_engine_depth = 1)
New_Game(white_is_engine = False, black_is_engine = True, white_engine_depth = 1, black_engine_depth = 1)
New_Game(white_is_engine = False, black_is_engine = False, white_engine_depth = 1, black_engine_depth = 1)


"""
BUGS:
Threat by pawns slightly dodgy when pieces captured
when pawn captures pawn
"""
