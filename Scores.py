class Scores:
    """Score contributors stored in this class and updated throughout the game"""
    def __init__(self):
        self.material = 0   # Sum of all pieces values on the board
        self.king_safety = 0
        self.control_of_centre = 0
        self.bad_knights = 0    # Sum of all penalties to knights on files 0 and 7
        self.threat_by_pawns = 0 # Bonuses applied when pawns threaten a non pawn piece
        self.isolated_pawns = 0
        self.double_pawns = 0
        self.capturable_unprotected = 0
        self.mobility = 0
        self.white_pawns_count = [1, 1, 1, 1, 1, 1, 1, 1]   # num pawns in files from 0 to 7
        self.black_pawns_count = [1, 1, 1, 1, 1, 1, 1, 1]
        self.num_legal_white_moves = 20
        self.num_legal_black_moves = 20
    
    def get_total(self):
        score = self.material + self.king_safety + self.control_of_centre + self.bad_knights+ self.threat_by_pawns + self.isolated_pawns+ self.double_pawns + self.mobility + self.capturable_unprotected
        return score
    
    def print_totals(self):
        print("material: "+str(self.material))
        print("mobility: "+str(self.mobility))
        print("king safety: "+str(self.king_safety))
        print("control of centre: "+str(self.control_of_centre))
        print("bad knights: "+str(self.bad_knights))
        print("threat by pawns: "+str(self.threat_by_pawns))
        print("Isolated pawn penalty: "+ str(self.isolated_pawns))
        print("Double pawns penalty: "+ str(self.double_pawns))
        print("Unprotected capturable: "+ str(self.capturable_unprotected))

    def update_isolated_pawn_penalty(self):
        # If 0,x,0 with x>=1 appears in pawn count apply x penalties to that colour
        penalty = 0
        penalty_value = 0.6
        # Central cases
        for i in range(1,7):
            if self.white_pawns_count[i]>=1 and self.white_pawns_count[i-1]==0 and self.white_pawns_count[i+1]==0:
                penalty += self.white_pawns_count[i]
            if self.black_pawns_count[i]>=1 and self.black_pawns_count[i-1]==0 and self.black_pawns_count[i+1]==0:
                penalty -= self.black_pawns_count[i]

        # Edge cases
        if self.white_pawns_count[0]>=1 and self.white_pawns_count[1]==0:
            penalty += self.white_pawns_count[0]
        if self.white_pawns_count[7]>=1 and self.white_pawns_count[6]==0:
            penalty += self.white_pawns_count[7]
        if self.black_pawns_count[0]>=1 and self.black_pawns_count[1]==0:
            penalty -= self.black_pawns_count[0]
        if self.black_pawns_count[7]>=1 and self.black_pawns_count[6]==0:
            penalty -= self.black_pawns_count[7]


        self.isolated_pawns = -penalty*penalty_value

    def update_double_pawns_penalty(self):
        penalty = 0
        penalty_value = 0.2
        for i in range(8):
            if self.white_pawns_count[i]>1:
                penalty += (penalty_value+self.white_pawns_count[i]-2)
            if self.black_pawns_count[i]>1:
                penalty -= (penalty_value+self.black_pawns_count[i]-2)
        self.double_pawns = -penalty

    def update_mobility(self):
        self.mobility = 0.01*(self.num_legal_white_moves - self.num_legal_black_moves)

# Things to add
# King safety- penalty for king on pawnless file
# King eyed by pieces etc
# Open semi open rook file (no friendly pawn on file)
