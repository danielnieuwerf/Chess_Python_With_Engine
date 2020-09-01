class Book():
    # Maps list of moves played to a move (book move)
    def __init__(self):
        self.book_moves = {}
        # [1,4,3,4] maps to [6,4,4,4]
        # Sicilian Defense
        {[1,3,3,3]:[6,3,4,3]}
        # French defense
        #e4 e6
        # Ruy Lopez
        # e4 e5 nf3 nc6 bb5
        