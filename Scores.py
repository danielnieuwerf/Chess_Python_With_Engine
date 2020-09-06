class Scores:
    """Score contributors stored in this class and updated throughout the game"""
    def __init__(self):
        self.material = 0   # Sum of all pieces values on the board
        self.king_safety = 0
        self.control_of_centre = 0
        self.bad_knights = 0    # Sum of all penalties to knights on files 0 and 7

    def get_total(self):
        score = self.material + self.king_safety + self.control_of_centre + self.bad_knights
        return score



