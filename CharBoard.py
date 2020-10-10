from Scores import *
import copy
from bitboard import BitBoard

class CharBoard:
    """Char representation of the board"""
    def __init__(self):
        self.pieces = [['R', 'N', 'B', 'K', 'Q', 'B', 'N', 'R'],
                       ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                       ['.', '.', '.', '.', '.', '.', '.', '.'],
                       ['.', '.', '.', '.', '.', '.', '.', '.'],
                       ['.', '.', '.', '.', '.', '.', '.', '.'],
                       ['.', '.', '.', '.', '.', '.', '.', '.'],
                       ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                       ['r', 'n', 'b', 'k', 'q', 'b', 'n', 'r']
                      ]
        self.scores = Scores()
        self.white_king_position = [0,3]
        self.black_king_position = [7,3]
        self.reset_board_strings = False    # When a pawn move is made we can empty board strings dictionary on this move

    def get_diagonals(self, r, c):
        # Returns [diag1,diag2] that go through r,c
        diag1, diag2 = "", ""
        # Get diag1 and diag2
        old_r, old_c = r, c
        min1 = min(r,c)
        min2 = min(r, 7-c)
        r = r - min1
        c = c - min1
        while r<8 and c<8:
            if self.pieces[r][c]!= '.':
                diag1 += self.pieces[r][c]
            else:
                diag1 += '.'
            r+=1    # Move in direction 1,1
            c+=1

        r = old_r - min2
        c = old_c + min2
        while r<8 and c>-1:
            if self.pieces[r][c]!= '.':
                diag2 += self.pieces[r][c]
            else:
                diag2 += '.'
            r+=1    # Move in direction 1, -1
            c-=1

        # Return diags
        return [diag1, diag2]

    def get_diagonals_without_empty_squares(self,r,c):
        # Returns [diag1,diag2] that go through r,c excluding empty squares
        diag1, diag2 = "", ""
        # Get diag1 and diag2
        old_r, old_c = r, c
        min1 = min(r,c)
        min2 = min(r, 7-c)
        r = r - min1
        c = c - min1
        while r<8 and c<8:
            if self.pieces[r][c]!= '.':
                diag1 += self.pieces[r][c]
            r+=1    # Move in direction 1,1
            c+=1

        r = old_r - min2
        c = old_c + min2
        while r<8 and c>-1:
            if self.pieces[r][c]!= '.':
                diag2 += self.pieces[r][c]
            r+=1    # Move in direction 1, -1
            c-=1

        # Return diags
        return [diag1, diag2]

    def get_file(self, c):
        # Returns string of symbols for file c
        file = ""
        for i in range(8):
            if self.pieces[i][c]!='.':
                file += self.pieces[i][c]
            else:
                file += "." # Empty SQUARE

        return file

    def get_file_without_empty_squares(self,c):
        file = ""
        for i in range(8):
            if self.pieces[i][c]!='.':
                file += self.pieces[i][c]
        return file

    def get_rank(self, r):
        # Returns string of piece symbols for rank r
        rank = ""
        for i in range(8):
            if self.pieces[r][i]!='.':
                rank += self.pieces[r][i]
            else:
                rank += "." # Empty SQUARE

        return rank

    def get_rank_without_empty_squares(self,r):
        rank = ''
        for i in range(8):
            if self.pieces[r][i]!='.':
                rank += self.pieces[r][i]
        return rank
            
    def is_draw_by_lack_of_material(self):
        # loop through whole board and store pieces in pieces = []
        pieces =[]
        for row in self.pieces:
            for piece in row:
                if piece!= '.':
                    # If board contains a pawn queen or rook return false
                    if piece in ['p', 'P', 'q', 'Q', 'r', 'R']:
                        return False
                    # Else append the piece into pieces
                    pieces.append(piece)
        # If we reach here pieces contains only kings, knights and bishops
        return len(pieces)<4    # Return true if length less than 4 else false

    def king_side_castle_blocked(self, white_turn = True):
        # Return whether or not white/black king is threatened on it's king side castling path
        if white_turn:
            threats_to_white_king_bb = self.create_bitboard_direct_threats_to_king(True)
            if threats_to_white_king_bb.bits[0][2] == 1:
                return True
            return False
        else:
            threats_to_black_king_bb = self.create_bitboard_direct_threats_to_king(False)
            if threats_to_black_king_bb.bits[7][2] == 1:
                return True
            return False

    def queen_side_castle_blocked(self, white_turn = True):
        # Return whether or not white/black king is threatened on it's queen side castling path
        if white_turn:
            threats_to_white_king_bb = self.create_bitboard_direct_threats_to_king(True)
            if threats_to_white_king_bb.bits[0][4] == 1:
                return True
            return False
        else:
            threats_to_black_king_bb = self.create_bitboard_direct_threats_to_king(False)
            if threats_to_black_king_bb.bits[7][4] == 1:
                return True
            return False

    def make_move(self,i,j,x,y):
        # Try to make a move from board[i][j] to board[x][y]
        # Update scores when appropriate within this function
        # Update king positions where appropriate
        sym = self.pieces[i][j]
        if sym == '.':  # If try to move an empty square
            return
        
        captured_symbol = self.pieces[x][y] # '.' if not capturing move

        # Update king positions
        if sym == 'k':
            self.black_king_position = [x,y]
        elif sym == 'K':
            self.white_king_position = [x,y]

        # Update pawn counts
        if captured_symbol == 'P':
            self.scores.white_pawns_count[y]-=1
        elif captured_symbol == 'p':
            self.scores.black_pawns_count[y]-=1
        if sym == 'p' and abs(j-y)==1:
            self.scores.black_pawns_count[y]+=1
            self.scores.black_pawns_count[j]-=1
        elif sym == 'P' and abs(j-y)==1:
            self.scores.white_pawns_count[y]+=1
            self.scores.white_pawns_count[j]-=1

        # Update threat by pawns score (threat to opponents pieces)
        # If a threatening pawn was captured update threat score 
        if captured_symbol == 'p':  # Captured black pawn
            if x!=0 and y!=0 and self.pieces[x-1][y-1] in ['N','B','R','Q']:   # If black pawn was threatening
                self.scores.threat_by_pawns += 0.05
            if x!=0 and y!=7 and self.pieces[x-1][y+1] in ['N','B','R','Q']:
                self.scores.threat_by_pawns += 0.05
        elif captured_symbol == 'P':
            if x!=7 and y!=0 and self.pieces[x+1][y-1] in ['n','b','r','q']:   # If white pawn was threatening
                self.scores.threat_by_pawns -= 0.05
            if x!=7 and y!=7 and self.pieces[x+1][y+1] in ['n','b','r','q']:
                self.scores.threat_by_pawns -= 0.05
        # If a threatening pawn was captured by en passant update threat by pawns score during en passant logic later on in this function

        # If a pawn was moved calculate the change in threat for this pawn
        if sym == 'p':  # Move a black pawn
            initial_threat = 0  # number of pieces the pawn threatens initially
            if j!=0 and i!=0 and self.pieces[i-1][j-1] in ['N','B','R','Q']:
                initial_threat += 1
            if i!=0 and j!=7 and self.pieces[i-1][j+1] in ['N','B','R','Q']:
                initial_threat += 1
            final_threat = 0
            if x!=0:    # If not pawn promotion
                if y!=0 and self.pieces[x-1][y-1] in ['N','B','R','Q']:
                    final_threat +=1
                if y!=7 and self.pieces[x-1][y+1] in ['N','B','R','Q']:
                    final_threat +=1
            threat_change = (final_threat - initial_threat)
            self.scores.threat_by_pawns -= (threat_change*0.05)  # Update threat by pawn
        elif sym == 'P':    # Move a white pawn
            initial_threat = 0
            if i!=7 and j!=0 and self.pieces[i+1][j-1] in ['n','b','r','q']:
                initial_threat +=1
            if i!=7 and j!=7 and self.pieces[i+1][j+1] in ['n','b','r','q']:
                initial_threat +=1
            final_threat = 0
            if x!=7:    # If not pawn promotion
                if y!=0 and self.pieces[x+1][y-1] in ['n','b','r','q']:
                    final_threat +=1
                if y!=7 and self.pieces[x+1][y+1] in ['n','b','r','q']:
                    final_threat +=1
            threat_change = (final_threat - initial_threat)
            self.scores.threat_by_pawns += (threat_change*0.05)  # Update threat by pawn

        # Move a piece away from/ to threatening pawn
        if sym in ['n','b','r','q']:    # Move black piece
            initial_threat = 0  # Initial threat to moving black piece
            if i>1 and j!=0 and self.pieces[i-1][j-1] == 'P':
                initial_threat +=1
            if i>1 and j!=7 and self.pieces[i-1][j+1] == 'P':
                initial_threat +=1
            final_threat = 0
            if x>1 and y!=0 and self.pieces[x-1][y-1]== 'P':
                final_threat +=1
            if x>1 and y!=7 and self.pieces[x-1][y+1]== 'P':
                final_threat +=1
            threat_change = final_threat - initial_threat
            self.scores.threat_by_pawns += (threat_change*0.05)
        elif sym in ['N','B','R','Q']:  # Move white piece
            initial_threat = 0  # Initial threat to moving white piece
            if i<6 and j!=0 and self.pieces[i+1][j-1]== 'p':
                initial_threat +=1
            if i<6 and j!=7 and self.pieces[i+1][j+1] == 'p':
                initial_threat +=1
            final_threat = 0
            if x<6 and y!=0 and self.pieces[x+1][y-1] == 'p':
                final_threat +=1
            if x<6 and y!=7 and self.pieces[x+1][y+1] == 'p':
                final_threat +=1
            threat_change = final_threat - initial_threat
            self.scores.threat_by_pawns -= (threat_change*0.05)

        # Update bad knights score
        if sym == 'n':   
            if j in [0,7]: # If black knight is moved from file 0 or 7
                self.scores.bad_knights -= 0.1
            elif y in [0,7]: # Else if black knight is moved onto file 0 or 7
                self.scores.bad_knights += 0.1
        elif sym == 'N':
            if j in [0,7]: # If white knight is moved from file 0 or 7
                self.scores.bad_knights += 0.1
            elif y in [0,7]: # Else if white knight is moved onto file 0 or 7
                self.scores.bad_knights -= 0.1
        if y in [0,7]:  # A bad knight is captured
            if captured_symbol == 'N':  # If bad white knight captured
                self.scores.bad_knights += 0.1
            elif captured_symbol == 'n':  # If bad black knight captured
                self.scores.bad_knights -= 0.1

        # Check if enpassant move was made
        if sym in ['p','P'] and abs(j-y)==1 and self.pieces[x][y]=='.':   # If this we have en passant move
            self.pieces[i][y] = '.'    # Delete captured pawn by enpassant and move the capturing pawn later in the function
            # Also update threatened by pawns score contributed by this captured pawn
            if x == 2: # Captured white pawn
                self.scores.material -=1    # Pawn value 1 captured
                if y!=0 and self.pieces[4][y-1] in ['n','b','r','q']:
                    self.scores.threat_by_pawns -=0.05
                if y!=7 and self.pieces[4][y+1] in ['n','b','r','q']:
                    self.scores.threat_by_pawns -=0.05
            elif x == 5:  # Captured black pawn by en passant
                self.scores.material +=1    # Pawn value -1 captured
                if y!=0 and self.pieces[3][y-1] in ['N','B','R','Q']:
                    self.scores.threat_by_pawns +=0.05
                if y!=7 and self.pieces[3][y+1] in ['N','B','R','Q']:
                    self.scores.threat_by_pawns +=0.05
            # Update pawn counts
            if sym == 'p':
                self.scores.white_pawns_count[y]-=1
            elif sym == 'P':
                self.scores.black_pawns_count[y]-=1

        # Check if castling move was made
        if sym in ['k', 'K'] and abs(j-y)==2:  # Sufficient castling condition
            # Handle the rook move here and updating king safety value (we move the king later on)
            if sym == 'k':  # Black king castling
                if y==1:    # King side castling
                    self.pieces[7][0]= '.' # Move rook
                    self.pieces[7][2]= 'r'
                    self.scores.castling_bonus -= 0.24 # Update king safety score  
                elif y==5:  # Queen side castling
                    self.pieces[7][7]= '.' # Move rook
                    self.pieces[7][4]= 'r'
                    self.scores.castling_bonus -= 0.17 # Update king safety score       
            elif sym == 'K': # White king castling
                if y==1:    # King side castling
                    self.pieces[0][0]= '.' # Move rook
                    self.pieces[0][2]= 'R'
                    self.scores.castling_bonus += 0.24 # Update king safety score             
                elif y==5:  # Queen side castling
                    self.pieces[0][7]= '.' # Move rook
                    self.pieces[0][4]= 'R'
                    self.scores.castling_bonus += 0.17 # Update king safety score  

        # If move is capturing move update material score
        if captured_symbol!='.':
            self.scores.material -=self.char_to_value(captured_symbol)

        # move piece at i,j to x,y
        temp_piece = copy.copy(self.pieces[i][j])
        self.pieces[i][j] = '.'
        self.pieces[x][y] = temp_piece

        # Check for pawn promotion
        if sym in ['p','P'] and x in [0,7]:
            self.pawn_promotion(x,y)

        # If pawn moved diagonally, is captured or promoted .... update pawn penalties and king safety
        if (sym in ['p','P'] and (abs(j-y)==1 or x in [0, 7])) or captured_symbol in ['p','P']:
            self.scores.update_isolated_pawn_penalty()
            self.scores.update_double_pawns_penalty()
            self.scores.update_king_safety(self.white_king_position, self.black_king_position)

        # If a pawn moves or is captured we can reset board strings dictionary
        if sym in ['p', 'P'] or captured_symbol in ['p', 'P']:   
            self.reset_board_strings = True

        # If a king was moved update king safety
        if sym in ['k', 'K']:
            self.scores.update_king_safety(self.white_king_position, self.black_king_position)

    def pawn_promotion(self,x,y):
        # Promote the pawn on self.pieces[x][y] to a queen
        if x==0 and self.pieces[0][y]=='p':
            self.pieces[0][y]= 'q'
            self.scores.material -=8
            self.scores.black_pawns_count[y]-=1
        if x==7 and self.pieces[7][y] =='P':
            self.pieces[7][y]= 'Q'
            self.scores.material +=8
            self.scores.white_pawns_count[y]-=1

    def board_to_string(self):
        board_string = ''
        for i in range(8):
            for j in range(8):
                board_string += self.pieces[i][j]
        return board_string

    def white_king_is_in_check(self):
        # Returns whether or not white king is in check
        white_king_pos = self.white_king_position
        row, col = white_king_pos[0], white_king_pos[1] # row and column of white king

        threats = self.create_bitboard_direct_threats_to_king(True)
        return threats.bits[row][col]==1  

    def black_king_is_in_check(self):
        # Returns whether or not black king is in check
        black_king_pos = self.black_king_position
        row, col = black_king_pos[0], black_king_pos[1] # row and column of black king

        threats = self.create_bitboard_direct_threats_to_king(False)
        return threats.bits[row][col]==1
        
    def char_to_value(self, char):
        # Given a char returns its value
        if char!='.':
            if char == 'p':
                return -1
            elif char == 'P':
                return 1
            elif char == 'n':
                return -3
            elif char == 'N':
                return 3
            elif char == 'b':
                return -3.15
            elif char == 'B':
                return 3.15
            elif char == 'r':
                return -5
            elif char == 'R':
                return 5
            elif char == 'Q':
                return 9
            elif char == 'q':
                return -9

        return 0

    def create_bitboard_direct_threats_to_king(self, king_colour_is_white):
        # Return bitboard where 1 represents this square is seen by (opponent of king_colour)
        threats = BitBoard()
        if king_colour_is_white:    # Threats to white king
            # Loop through board finding black pieces
            for i in range(8):
                for j in range(8):
                    if self.pieces[i][j]!='.' and self.pieces[i][j].islower():
                        if self.pieces[i][j]== 'p': # Black pawn
                            if i!=0 and j!=0:
                                threats.set_true(i-1,j-1)
                            if i!=0 and j!=7:
                                threats.set_true(i-1,j+1)
                        elif self.pieces[i][j] == 'k':  # Black king
                            if i!=0:
                                if j!=0:
                                    threats.set_true(i-1,j-1)
                                threats.set_true(i-1,j)
                                if j!=7:
                                    threats.set_true(i-1,j+1)
                            if i!=7:
                                if j!=0:
                                    threats.set_true(i+1,j-1)
                                threats.set_true(i+1,j)
                                if j!=7:
                                    threats.set_true(i+1,j+1)
                            if j!=0:
                                threats.set_true(i,j-1)
                            if j!=7:
                                threats.set_true(i,j+1)
                        elif self.pieces[i][j] == 'n':  # Black knight
                            if i>1:
                                if j>0:
                                    threats.set_true(i-2,j-1)
                                if j<7:
                                    threats.set_true(i-2,j+1)
                            if i>0:
                                if j>1:
                                    threats.set_true(i-1,j-2)
                                if j<6:
                                    threats.set_true(i-1,j+2)
                            if i<7:
                                if j>1:
                                    threats.set_true(i+1,j-2)
                                if j<6:
                                    threats.set_true(i+1,j+2)
                            if i<6:
                                if j>0:
                                    threats.set_true(i+2,j-1)
                                if j<7:
                                    threats.set_true(i+2,j+1)
                        elif self.pieces[i][j] in ['b','q']:    # Diagonal attacks
                            diagonals = self.get_diagonals(i,j)
                            diag1, diag2 = diagonals[0], diagonals[1] # These are strings of length 8 like 'q.r..B..'
                            up_right, up_left , down_right, down_left = 0,0,0,0 # Indicates how many squares the piece can move in each direction

                            # South east diagonal (diag1)
                            if not (i==7 or j==7):  # Down + right
                                x = min(i,j)+1    # min(i,j) is index of our piece in the diag1 string
                                while x<len(diag1) and diag1[x]=='.':
                                    down_right += 1
                                    x += 1
                                # If not past the end of the diagonal, it sees one more square
                                if x!=len(diag1):
                                    down_right += 1

                            if not (i==0 or j==0):  # Up + left
                                x = min(i,j) - 1    # min(i,j) is index of our piece in the diag1 string
                                while x>-1 and diag1[x]=='.':
                                    up_left += 1
                                    x -=1
                                # If not past the end of the diagonal, it sees one more square
                                if x!=-1:
                                    up_left += 1                            

                            # South west diagonal (diag2)
                            if not (i==7 or j==0):  # Down + left
                                x = min(i,7-j)+1  # min(i,7-j) is index of our piece in the diag2 string
                                while x<len(diag2) and diag2[x]=='.':
                                    down_left += 1
                                    x += 1
                                # If not past the end of the diagonal, it sees one more square
                                if x!=len(diag2):
                                    down_left += 1 

                            if not (i==0 or j==7):  # Up + right
                                x = min(i,7-j)-1  # min(i,7-j) is index of our piece in the diag2 string
                                while x>-1 and diag2[x]=='.':
                                    up_right += 1
                                    x -= 1
                                # If not past the end of the diagonal, it sees one more square
                                if x!=-1:
                                    up_right += 1

                            # Add all the up and down (left and right) moves to moves 
                            if up_right>0:
                                for x in range(1,up_right+1):    
                                    threats.set_true(i-x,j+x)
                            if up_left>0:
                                for x in range(1,up_left+1):
                                    threats.set_true(i-x,j-x)
                            if down_right>0:
                                for x in range(1,down_right+1):
                                    threats.set_true(i+x,j+x)
                            if down_left>0:
                                for x in range(1,down_left+1):
                                    threats.set_true(i+x,j-x)     
                        if self.pieces[i][j] in ['r', 'q']:   # Horizontal and vertical attacks
                            up, down, right, left = 0,0,0,0 # Indicates how many squares the piece can move in each direction
                            file_string = self.get_file(j)    
                            rank_string = self.get_rank(i)

                            if j<7: # Right
                                x = j+1
                                while x<8 and rank_string[x]=='.':
                                    x+=1
                                    right+=1

                                # If not at end of row/file can go one more
                                if x<8:
                                    right += 1

                            if j>0: # Left
                                x = j - 1
                                while x>-1 and rank_string[x]=='.':
                                    x-=1
                                    left+=1

                                # If not at end of row/file can go one more
                                if x>-1:
                                    left += 1

                            if i>0: # Down (in column index)
                                x = i - 1
                                while x>-1 and file_string[x]=='.':
                                    x-=1
                                    down+=1

                                # If not at end of row/file can go one more
                                if x>-1:
                                    down+=1

                            if i<7: # Up
                                x = i+1
                                while x<8 and file_string[x]=='.':
                                    x += 1
                                    up += 1
                                # If not at end of row/file can go one more
                                if x<8:
                                    up += 1

                            # Add all up down left right moves to moves 
                            if right>0:
                                for x in range(1,right+1):    
                                    threats.set_true(i,j+x)
                            if left>0:
                                for x in range(1,left+1):
                                    threats.set_true(i,j-x)
                            if up>0:
                                for x in range(1,up+1):
                                    threats.set_true(i+x,j)
                            if down>0:
                                for x in range(1,down+1):
                                    threats.set_true(i-x,j)                      
        else:   # Threats to black king
            # Loop through board finding blackwhite pieces
            for i in range(8):
                for j in range(8):
                    if self.pieces[i][j]!='.' and self.pieces[i][j].isupper():
                        if self.pieces[i][j]== 'P': # White pawn
                            if i!=7 and j!=0:
                                threats.set_true(i+1,j-1)
                            if i!=7 and j!=7:
                                threats.set_true(i+1,j+1)
                        elif self.pieces[i][j] == 'K':  # White king
                            if i!=0:
                                if j!=0:
                                    threats.set_true(i-1,j-1)
                                threats.set_true(i-1,j)
                                if j!=7:
                                    threats.set_true(i-1,j+1)
                            if i!=7:
                                if j!=0:
                                    threats.set_true(i+1,j-1)
                                threats.set_true(i+1,j)
                                if j!=7:
                                    threats.set_true(i+1,j+1)
                            if j!=0:
                                threats.set_true(i,j-1)
                            if j!=7:
                                threats.set_true(i,j+1)
                        elif self.pieces[i][j] == 'N':  # White knight
                            if i>1:
                                if j>0:
                                    threats.set_true(i-2,j-1)
                                if j<7:
                                    threats.set_true(i-2,j+1)
                            if i>0:
                                if j>1:
                                    threats.set_true(i-1,j-2)
                                if j<6:
                                    threats.set_true(i-1,j+2)
                            if i<7:
                                if j>1:
                                    threats.set_true(i+1,j-2)
                                if j<6:
                                    threats.set_true(i+1,j+2)
                            if i<6:
                                if j>0:
                                    threats.set_true(i+2,j-1)
                                if j<7:
                                    threats.set_true(i+2,j+1)
                        elif self.pieces[i][j] in ['B','Q']:    # Diagonal attacks
                            diagonals = self.get_diagonals(i,j)
                            diag1, diag2 = diagonals[0], diagonals[1] # These are strings of length 8 like 'q.r..B..'
                            up_right, up_left , down_right, down_left = 0,0,0,0 # Indicates how many squares the piece can move in each direction

                            # South east diagonal (diag1)
                            if not (i==7 or j==7):  # Down + right
                                x = min(i,j)+1    # min(i,j) is index of our piece in the diag1 string
                                while x<len(diag1) and diag1[x]=='.':
                                    down_right += 1
                                    x += 1
                                # If not past the end of the diagonal, it sees one more square
                                if x!=len(diag1):
                                    down_right += 1

                            if not (i==0 or j==0):  # Up + left
                                x = min(i,j) - 1    # min(i,j) is index of our piece in the diag1 string
                                while x>-1 and diag1[x]=='.':
                                    up_left += 1
                                    x -=1
                                # If not past the end of the diagonal, it sees one more square
                                if x!=-1:
                                    up_left += 1                            

                            # South west diagonal (diag2)
                            if not (i==7 or j==0):  # Down + left
                                x = min(i,7-j)+1  # min(i,7-j) is index of our piece in the diag2 string
                                while x<len(diag2) and diag2[x]=='.':
                                    down_left += 1
                                    x += 1
                                # If not past the end of the diagonal, it sees one more square
                                if x!=len(diag2):
                                    down_left += 1 

                            if not (i==0 or j==7):  # Up + right
                                x = min(i,7-j)-1  # min(i,7-j) is index of our piece in the diag2 string
                                while x>-1 and diag2[x]=='.':
                                    up_right += 1
                                    x -= 1
                                # If not past the end of the diagonal, it sees one more square
                                if x!=-1:
                                    up_right += 1

                            # Add all the up and down (left and right) moves to moves 
                            if up_right>0:
                                for x in range(1,up_right+1):    
                                    threats.set_true(i-x,j+x)
                            if up_left>0:
                                for x in range(1,up_left+1):
                                    threats.set_true(i-x,j-x)
                            if down_right>0:
                                for x in range(1,down_right+1):
                                    threats.set_true(i+x,j+x)
                            if down_left>0:
                                for x in range(1,down_left+1):
                                    threats.set_true(i+x,j-x)     
                        if self.pieces[i][j] in ['R', 'Q']:   # Horizontal and vertical attacks
                            up, down, right, left = 0,0,0,0 # Indicates how many squares the piece can move in each direction
                            file_string = self.get_file(j)    
                            rank_string = self.get_rank(i)

                            if j<7: # Right
                                x = j+1
                                while x<8 and rank_string[x]=='.':
                                    x+=1
                                    right+=1

                                # If not at end of row/file can go one more
                                if x<8:
                                    right += 1

                            if j>0: # Left
                                x = j - 1
                                while x>-1 and rank_string[x]=='.':
                                    x-=1
                                    left+=1

                                # If not at end of row/file can go one more
                                if x>-1:
                                    left += 1

                            if i>0: # Down (in column index)
                                x = i - 1
                                while x>-1 and file_string[x]=='.':
                                    x-=1
                                    down+=1

                                # If not at end of row/file can go one more
                                if x>-1:
                                    down+=1

                            if i<7: # Up
                                x = i+1
                                while x<8 and file_string[x]=='.':
                                    x += 1
                                    up += 1
                                # If not at end of row/file can go one more
                                if x<8:
                                    up += 1

                            # Add all up down left right moves to moves 
                            if right>0:
                                for x in range(1,right+1):    
                                    threats.set_true(i,j+x)
                            if left>0:
                                for x in range(1,left+1):
                                    threats.set_true(i,j-x)
                            if up>0:
                                for x in range(1,up+1):
                                    threats.set_true(i+x,j)
                            if down>0:
                                for x in range(1,down+1):
                                    threats.set_true(i-x,j)

        return threats

    def create_bitboard_shields_to_king(self, king_colour_is_white):
        # Return bitboard where 1 indicates the piece on that square is shielding the king of king_colour from attack
        # And 0 if moving the piece does not reveal an attack on the king
        king_pos = None   # The position of our king
        if king_colour_is_white:
            king_pos = self.white_king_position
        else:
            king_pos = self.black_king_position

        shields = BitBoard()    # Create bit board
        
        # Find the file, rank and diagonals on which our king lies
        file = self.get_file(king_pos[1])
        rank = self.get_rank(king_pos[0])
        diagonals = self.get_diagonals(king_pos[0],king_pos[1])
        diag1, diag2 = diagonals[0], diagonals[1]
        if king_colour_is_white:    # White king
            # For a shield to exist on a row or file it must contain a black rook or queen (similarly for diags with bishops and queens)
            if file.find("q")!=-1 or file.find('r')!=-1:    # File must contain an opposing rook or queen
                clean_file = self.clean_string_looking_for_shields(file, 'K', ['r','q'])
                if clean_file.find("KSX")!=-1:  # If contains shield to the right
                    shield_pos = None
                    for x in range(king_pos[0]+1,8):
                        if file[x]!='.':    # First non empty square is the shield
                            shield_pos = copy.copy(x)
                            break
                    shields.bits[shield_pos][king_pos[1]] = 1   # Update shields bitboard
                if clean_file.find("XSK")!=-1:  # Contains shield to the left
                    shield_pos = None
                    for x in range(king_pos[0]-1,-1,-1):
                        if file[x]!='.':    # First non empty square is the shield
                            shield_pos = copy.copy(x)
                            break
                    shields.bits[shield_pos][king_pos[1]] = 1   # Update shields bitboard

            if rank.find("q")!=-1 or rank.find('r')!=-1:    # File contains an opposing rook or queen
                clean_rank = self.clean_string_looking_for_shields(rank, 'K', ['r','q'])
                if clean_rank.find("KSX")!=-1:  # If contains shield to the right
                    shield_pos = None
                    for x in range(king_pos[1]+1,8):
                        if rank[x]!='.':    # First non empty square is the shield
                            shield_pos = copy.copy(x)
                            break
                    shields.bits[king_pos[0]][shield_pos] = 1   # Update shields bitboard
                if clean_rank.find("XSK")!=-1:  # Contains shield to the left
                    shield_pos = None
                    for x in range(king_pos[1]-1,-1,-1):
                        if rank[x]!='.':    # First non empty square is the shield
                            shield_pos = copy.copy(x)
                            break
                    shields.bits[king_pos[0]][shield_pos] = 1   # Update shields bitboard

            if diag1.find('b')!=-1 or diag1.find('q')!=-1:
                clean_diag1 = self.clean_string_looking_for_shields(diag1, 'K', ['b','q'])
                if clean_diag1.find("KSX")!=-1:  # If contains shield to the right
                    shield_pos = None
                    king_index_in_diag1 = min(king_pos[0], king_pos[1])
                    for x in range(king_index_in_diag1+1,8): 
                        if diag1[x]!='.':    # First non empty square is the shield
                            shield_pos = copy.copy(x)
                            break
                    shield_distance = shield_pos - king_index_in_diag1  # Shield distance from king

                    shields.bits[king_pos[0]+shield_distance][king_pos[1]+shield_distance] = 1   # Update shields bitboard
                if clean_diag1.find("XSK")!=-1:  # Contains shield to the left
                    shield_pos = None
                    king_index_in_diag1 = min(king_pos[0], king_pos[1])
                    for x in range(king_index_in_diag1-1,-1,-1):
                        if diag1[x]!='.':    # First non empty square is the shield
                            shield_pos = copy.copy(x)
                            break
                    shield_distance = king_index_in_diag1 - shield_pos  # Shield distance from king

                    shields.bits[king_pos[0]-shield_distance][king_pos[1]-shield_distance] = 1   # Update shields bitboard
            if diag2.find('b')!=-1 or diag2.find('q')!=-1:
                clean_diag2 = self.clean_string_looking_for_shields(diag2, 'K', ['b','q'])
                king_index_in_diag2 = min(king_pos[0], 7-king_pos[1])
                if clean_diag2.find("KSX")!=-1:  # If contains shield to the right
                    shield_pos = None
                    for x in range(king_index_in_diag2+1,8):
                        if diag2[x]!='.':    # First non empty square is the shield
                            shield_pos = copy.copy(x)
                            break
                    shield_distance = shield_pos - king_index_in_diag2  # Shield distance from king

                    shields.bits[king_pos[0]+shield_distance][king_pos[1]-shield_distance] = 1   # Update shields bitboard
                if clean_diag2.find("XSK")!=-1:  # Contains shield to the left
                    shield_pos = None
                    for x in range(king_index_in_diag2-1,-1,-1):
                        if diag2[x]!='.':    # First non empty square is the shield
                            shield_pos = copy.copy(x)
                            break
                    shield_distance = king_index_in_diag2 - shield_pos  # Shield distance from king

                    shields.bits[king_pos[0]-shield_distance][king_pos[1]+shield_distance] = 1   # Update shields bitboard
        else:   # Black king
            # For a shield to exist on a row or file it must contain a black rook or queen (similarly for diags with bishops and queens)
            if file.find("Q")!=-1 or file.find('R')!=-1:    # File must contain an opposing rook or queen
                clean_file = self.clean_string_looking_for_shields(file, 'k', ['R','Q'])
                if clean_file.find("kSX")!=-1:  # If contains shield to the right
                    shield_pos = None
                    for x in range(king_pos[0]+1,8):
                        if file[x]!='.':    # First non empty square is the shield
                            shield_pos = copy.copy(x)
                            break
                    shields.bits[shield_pos][king_pos[1]] = 1   # Update shields bitboard
                if clean_file.find("XSk")!=-1:  # Contains shield to the left
                    shield_pos = None
                    for x in range(king_pos[0]-1,-1,-1):
                        if file[x]!='.':    # First non empty square is the shield
                            shield_pos = copy.copy(x)
                            break
                    shields.bits[shield_pos][king_pos[1]] = 1   # Update shields bitboard

            if rank.find("Q")!=-1 or rank.find('R')!=-1:    # File contains an opposing rook or queen
                clean_rank = self.clean_string_looking_for_shields(rank, 'k', ['R','Q'])
                if clean_rank.find("kSX")!=-1:  # If contains shield to the right
                    shield_pos = None
                    for x in range(king_pos[1]+1,8):
                        if rank[x]!='.':    # First non empty square is the shield
                            shield_pos = copy.copy(x)
                            break
                    shields.bits[king_pos[0]][shield_pos] = 1   # Update shields bitboard
                if clean_rank.find("XSk")!=-1:  # Contains shield to the left
                    shield_pos = None
                    for x in range(king_pos[1]-1,-1,-1):
                        if rank[x]!='.':    # First non empty square is the shield
                            shield_pos = copy.copy(x)
                            break
                    shields.bits[king_pos[0]][shield_pos] = 1   # Update shields bitboard

            if diag1.find('B')!=-1 or diag1.find('Q')!=-1:
                clean_diag1 = self.clean_string_looking_for_shields(diag1, 'k', ['B','Q'])
                if clean_diag1.find("kSX")!=-1:  # If contains shield to the right
                    shield_pos = None
                    king_index_in_diag1 = min(king_pos[0], king_pos[1])
                    for x in range(king_index_in_diag1+1,8):
                        if diag1[x]!='.':    # First non empty square is the shield
                            shield_pos = copy.copy(x)
                            break
                    shield_distance = shield_pos - king_index_in_diag1  # Shield distance from king

                    shields.bits[king_pos[0]+shield_distance][king_pos[1]+shield_distance] = 1   # Update shields bitboard
                if clean_diag1.find("XSk")!=-1:  # Contains shield to the left
                    shield_pos = None
                    king_index_in_diag1 = min(king_pos[0], king_pos[1])
                    for x in range(king_index_in_diag1-1,-1,-1):
                        if diag1[x]!='.':    # First non empty square is the shield
                            shield_pos = copy.copy(x)
                            break
                    shield_distance = king_index_in_diag1 - shield_pos  # Shield distance from king

                    shields.bits[king_pos[0]-shield_distance][king_pos[1]-shield_distance] = 1   # Update shields bitboard
            if diag2.find('B')!=-1 or diag2.find('Q')!=-1:
                clean_diag2 = self.clean_string_looking_for_shields(diag2, 'k', ['B','Q'])
                king_index_in_diag2 = min(king_pos[0], 7-king_pos[1])
                if clean_diag2.find("kSX")!=-1:  # If contains shield to the right
                    shield_pos = None
                    for x in range(king_index_in_diag2+1,8): 
                        if diag2[x]!='.':    # First non empty square is the shield
                            shield_pos = copy.copy(x)
                            break
                    shield_distance = shield_pos - king_index_in_diag2  # Shield distance from king

                    shields.bits[king_pos[0]+shield_distance][king_pos[1]-shield_distance] = 1   # Update shields bitboard
                if clean_diag2.find("XSk")!=-1:  # Contains shield to the left
                    shield_pos = None
                    for x in range(king_index_in_diag2-1,-1,-1):
                        if diag2[x]!='.':    # First non empty square is the shield
                            shield_pos = copy.copy(x)
                            break
                    shield_distance = king_index_in_diag2 - shield_pos  # Shield distance from king

                    shields.bits[king_pos[0]-shield_distance][king_pos[1]+shield_distance] = 1   # Update shields bitboard

        return shields

    def clean_string_looking_for_shields(self, string, shielded, shielding_from):
        # Given a string which might represent a file or rank or diagonal return a new string in a useful form to determine if there is a shielding piece in the string
        useful_string = ''  # Useful string we shall return
        for x in string:
            if x=='.':
                continue
            elif x==shielded:
                useful_string += x
            elif x in shielding_from:
                useful_string += 'X'    # Attacker
            elif x.isupper()==shielded.isupper():
                useful_string += 'S'    # Shield

        return useful_string

    def get_pieces_string(self):
        pieces_string = ""
        for i in range(8):
            for j in range(8):
                if self.pieces[i][j]!='.':
                    pieces_string += self.pieces[i][j]
        
        return ''.join(sorted(pieces_string))