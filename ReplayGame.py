from New_Game import New_Game
from pgn_parser import parser, pgn

class ReplayGame(object):
    """Given a pgn file replay the game"""
    def __init__(self, pgn):
        self.new_game = New_Game()
        self.moves = pgn_to_moves(pgn)

def pgn_to_moves(pgn) -> list:
    # Given a pgn return of list of moves
    pass



