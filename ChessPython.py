from New_Game import *        


# Play games with engines or players
New_Game(white_is_engine = False, black_is_engine = True, white_engine_depth = 1, black_engine_depth = 1)
New_Game(white_is_engine = True, black_is_engine = True, white_engine_depth = 1, black_engine_depth = 1)
New_Game(white_is_engine = True, black_is_engine = False, white_engine_depth = 1, black_engine_depth = 1)
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
# Do not compute white king black king is in check every move ( do not compute when king moves... or when knight moves only check if the new knight is checking the king 
# Add this as var in game
# Make get legal moves function more efficient for white and black (shave some time off in en passant logic)
# Bugs it castles while in check