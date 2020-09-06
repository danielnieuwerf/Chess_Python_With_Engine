from Pieces import *
from Scores import *
# Board class initialised to game start
class Board():
    def __init__(self):
        self.pieces = [[White_Rook(), White_Knight(), White_Bishop(), White_King(), White_Queen(), White_Bishop(), White_Knight(), White_Rook()],
                       [White_Pawn(), White_Pawn(), White_Pawn(), White_Pawn(), White_Pawn(), White_Pawn(), White_Pawn(), White_Pawn()],
                       [None, None, None, None, None, None, None, None],
                       [None, None, None, None, None, None, None, None],
                       [None, None, None, None, None, None, None, None],
                       [None, None, None, None, None, None, None, None],
                       [Black_Pawn(), Black_Pawn(), Black_Pawn(), Black_Pawn(), Black_Pawn(), Black_Pawn(), Black_Pawn(), Black_Pawn()],
                       [Black_Rook(), Black_Knight(), Black_Bishop(), Black_King(), Black_Queen(), Black_Bishop(), Black_Knight(), Black_Rook()]
                      ]
        self.scores = Scores()
        self.white_king_position = [0,3]
        self.black_king_position = [7,3]

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
            if self.pieces[r][c]!= None:
                diag1 += self.pieces[r][c].symbol
            else:
                diag1 += '.'
            r+=1    # Move in direction 1,1
            c+=1

        r = old_r - min2
        c = old_c + min2
        while r<8 and c>-1:
            if self.pieces[r][c]!= None:
                diag2 += self.pieces[r][c].symbol
            else:
                diag2 += '.'
            r+=1    # Move in direction 1, -1
            c-=1

        # Return diags
        return [diag1, diag2]

    def get_file(self, c):
        # Returns string of symbols for file c
        file = ""
        for i in range(8):
            if self.pieces[i][c]!=None:
                file += self.pieces[i][c].symbol
            else:
                file += "." # Empty SQUARE

        return file

    def get_file_without_empty_squares(self,c):
        file = ""
        for i in range(8):
            if self.pieces[i][c]!=None:
                file += self.pieces[i][c].symbol
        return file

    def get_rank(self, r):
        # Returns string of piece symbols for rank r
        rank = ""
        for i in range(8):
            if self.pieces[r][i]!=None:
                rank += self.pieces[r][i].symbol
            else:
                rank += "." # Empty SQUARE

        return rank

    def get_rank_without_empty_squares(self,r):
        rank = ''
        for i in range(8):
            if self.pieces[r][i]!=None:
                rank += self.pieces[r][i].symbol
        return rank
            
    def is_draw_by_lack_of_material(self):
        # loop through whole board and store pieces in pieces = []
        pieces =[]
        for row in self.pieces:
            for piece in row:
                if piece!= None:
                    # If board contains a pawn queen or rook return false
                    if type(piece)==White_Pawn or type(piece)==Black_Pawn:
                        return False
                    if piece.symbol =='q' or piece.symbol =='Q' or piece.symbol =='r' or piece.symbol =='R':
                        return False
                    # Else append the piece into pieces
                    pieces.append(piece.symbol)
        # If we reach here pieces contains only kings, knights and bishops
        return len(pieces)<4    # Return true if length less than 4 else false

    def king_side_castle_blocked(self, white_turn = True):
        # If white turn check castling for white else check for black
        # Return true if the move is blocked else return false
        copy_board = copy.deepcopy(self)
        if white_turn:
            copy_board.make_move(0,3,0,2)
            if copy_board.white_king_is_in_check():
                return True
            return False    # If not in check path is not blocked
        else:
            copy_board.make_move(7,3,7,2)
            if copy_board.black_king_is_in_check():
                return True
            return False    # If not in check path is not blocked

    def queen_side_castle_blocked(self, white_turn = True):
        # If white turn check castling for white else check for black
        # Return true if the move is blocked else return false
        copy_board = copy.deepcopy(self)
        if white_turn:
            copy_board.make_move(0,3,0,4)
            if copy_board.white_king_is_in_check():
                return True
            return False    # If not in check path is not blocked
        else:
            copy_board.make_move(7,3,7,4)
            if copy_board.black_king_is_in_check():
                return True
            return False    # If not in check path is not blocked

    def make_move(self,i,j,x,y):
        # Try to make a move from board[i][j] to board[x][y]
        # Update scores when appropriate within this function
        # Update king positions where appropriate
        try:
            sym = self.pieces[i][j].symbol  # If try to move an empty SQUARE return
        except:
            return
        try:
            captured_symbol = self.pieces[x][y].symbol
        except:
            captured_symbol = None

        # Update king positions
        if sym == 'k':
            self.black_king_position = [x,y]
        elif sym == 'K':
            self.white_king_position = [x,y]

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
        if y in [0,7]:
            if captured_symbol == 'N':  # If bad white knight captured
                self.scores.bad_knights += 0.1
            elif captured_symbol == 'n':  # If bad black knight captured
                self.scores.bad_knights -= 0.1


        # Check if enpassant move was made
        if abs(i-x)==1 and abs(j-y)==1: #Diagonal move by 1
            if self.pieces[x][y]==None and self.pieces[i][j].symbol in ['p','P']:   # If this we have en passant
                self.scores.material += self.pieces[i][j].value     # Add 1 or -1 to material score
                self.pieces[i][y] = None    # Delete captured pawn by enpassant and move the capturing pawn later in the function
        
        # Check if castling move was made
        if sym in ['k', 'K'] and self.pieces[x][y] == None and abs(j-y)==2 and i==x:  # Sufficient castling condition
            # Handle the rook move here and updating king safety value (we move the king later on)
            if sym == 'k':  # Black king castling
                if y==1:    # King side castling
                    self.pieces[7][0]= None # Move rook
                    self.pieces[7][2]= Black_Rook()
                    self.scores.king_safety -= 0.14 # Update king safety score  
                elif y==5:  # Queen side castling
                    self.pieces[7][7]= None # Move rook
                    self.pieces[7][4]= Black_Rook()
                    self.scores.king_safety -= 0.13 # Update king safety score  
                
            elif sym == 'K': # White king castling
                if y==1:    # King side castling
                    self.pieces[0][0]= None # Move rook
                    self.pieces[0][2]= White_Rook()
                    self.scores.king_safety -= 0.13 # Update king safety score             
                elif y==5:  # Queen side castling
                    self.pieces[0][7]= None # Move rook
                    self.pieces[0][4]= White_Rook()
                    self.scores.king_safety -= 0.13 # Update king safety score  


        # If move is capturing move update material score
        try:
            capturing = self.pieces[i][j].value * self.pieces[x][y].value
            if capturing < 0:   # If capturing move
                self.scores.material -=self.pieces[x][y].value
        except:
            pass

        # move piece at i,j to x,y
        temp = self.pieces[i][j]
        self.pieces[i][j] = None
        self.pieces[x][y] = temp

        # Check for pawn promotion
        if j==y and abs(i-x)==1:    # If move one up or down a file check for pawn promotion
            self.pawn_promotion()

    def pawn_promotion(self):
        for i in range(8):
            if self.pieces[0][i]!= None and self.pieces[0][i].symbol=='p':
                self.pieces[0][i]= Black_Queen()
                self.scores.material -=8
            if self.pieces[7][i]!= None and self.pieces[7][i].symbol=='P':
                self.pieces[7][i]= White_Queen()
                self.scores.material +=8

    def white_king_is_in_check(self):
        white_king_pos = self.white_king_position
        row, col = white_king_pos[0], white_king_pos[1] # row and column of white king
        # Check by black pawn
        if row < 7 and col>0 and self.pieces[row+1][col-1]!=None and self.pieces[row+1][col-1].symbol=='p':
            return True
        if row < 7 and col<7 and self.pieces[row+1][col+1]!=None and self.pieces[row+1][col+1].symbol=='p':
            return True
        
        # Check by black knight
        if row >1 and col>0 and self.pieces[row-2][col-1]!=None and self.pieces[row-2][col-1].symbol=='n':
            return True
        if row >1 and col<7 and self.pieces[row-2][col+1]!=None and self.pieces[row-2][col+1].symbol=='n':
            return True
        if row>0 and col>1 and self.pieces[row-1][col-2]!=None and self.pieces[row-1][col-2].symbol=='n':
            return True
        if row>0 and col<6 and self.pieces[row-1][col+2]!=None and self.pieces[row-1][col+2].symbol=='n':
            return True
        if row < 6 and col>0 and self.pieces[row+2][col-1]!=None and self.pieces[row+2][col-1].symbol=='n':
            return True
        if row < 6 and col<7 and self.pieces[row+2][col+1]!=None and self.pieces[row+2][col+1].symbol=='n':
            return True
        if row < 7 and col>1 and self.pieces[row+1][col-2]!=None and self.pieces[row+1][col-2].symbol=='n':
            return True
        if row < 7 and col<6 and self.pieces[row+1][col+2]!=None and self.pieces[row+1][col+2].symbol=='n':
            return True

        # Check by black king (effectively)
        black_king_pos =self.black_king_position
        if abs(row - black_king_pos[0]) <2 and abs(col - black_king_pos[1]) <2:
            return True

        # Check by bishop or queen diagonally
        diagonals = self.get_diagonals(row,col) # Get strings of symbols in both diagonals
        diag1 = diagonals[0]
        diag2 = diagonals[1]

        # Remove empty squares in these strings then look for checks
        cleaned_diag1 =""
        cleaned_diag2 = ""
        for x in diag1:
            if x=='.':
                pass
            else:
                cleaned_diag1 += x
        if cleaned_diag1.find('Kq')!=-1 or cleaned_diag1.find('Kb')!=-1:
            return True
        if cleaned_diag1.find('qK')!=-1 or cleaned_diag1.find('bK')!=-1:
            return True

        for x in diag2:
            if x=='.':
                pass
            else:
                cleaned_diag2 += x
        if cleaned_diag2.find('Kq')!=-1 or cleaned_diag2.find('Kb')!=-1:
            return True
        if cleaned_diag2.find('qK')!=-1 or cleaned_diag2.find('bK')!=-1:
            return True


        # Check by rook or queen horizontally and vertically
        horizontal = self.get_rank(row)     # Get strings of symbols in both directions
        vertical = self.get_file(col)

        # Remove empty spaces in these strings then look for checks
        cleaned_horizontal = ""
        for x in horizontal:
            if x=='.':
                pass
            else:
                cleaned_horizontal += x
        if cleaned_horizontal.find('Kq')!=-1 or cleaned_horizontal.find('Kr')!=-1:
            return True
        if cleaned_horizontal.find('qK')!=-1 or cleaned_horizontal.find('rK')!=-1:
            return True

        cleaned_vertical = ""
        for x in vertical:
            if x=='.':
                pass
            else:
                cleaned_vertical += x
        if cleaned_vertical.find('Kq')!=-1 or cleaned_vertical.find('Kr')!=-1:
            return True
        if cleaned_vertical.find('qK')!=-1 or cleaned_vertical.find('rK')!=-1:
            return True


        # If we reach here the white king is not in check so return false
        return False

    def black_king_is_in_check(self):
        black_king_pos = self.black_king_position
        row, col = black_king_pos[0], black_king_pos[1] # row and column of black king
        # Check by white pawn
        if row > 0 and col>0 and self.pieces[row-1][col-1]!=None and self.pieces[row-1][col-1].symbol=='P':
            return True
        if row > 0 and col<7 and self.pieces[row-1][col+1]!=None and self.pieces[row-1][col+1].symbol=='P':
            return True
        
        # Check by white knight
        if row >1 and col>0 and self.pieces[row-2][col-1]!=None and self.pieces[row-2][col-1].symbol=='N':
            return True
        if row >1 and col<7 and self.pieces[row-2][col+1]!=None and self.pieces[row-2][col+1].symbol=='N':
            return True
        if row>0 and col>1 and self.pieces[row-1][col-2]!=None and self.pieces[row-1][col-2].symbol=='N':
            return True
        if row>0 and col<6 and self.pieces[row-1][col+2]!=None and self.pieces[row-1][col+2].symbol=='N':
            return True
        if row < 6 and col>0 and self.pieces[row+2][col-1]!=None and self.pieces[row+2][col-1].symbol=='N':
            return True
        if row < 6 and col<7 and self.pieces[row+2][col+1]!=None and self.pieces[row+2][col+1].symbol=='N':
            return True
        if row < 7 and col>1 and self.pieces[row+1][col-2]!=None and self.pieces[row+1][col-2].symbol=='N':
            return True
        if row < 7 and col<6 and self.pieces[row+1][col+2]!=None and self.pieces[row+1][col+2].symbol=='N':
            return True

        # Check by white king (effectively)
        white_king_pos =self.white_king_position
        if abs(row - white_king_pos[0]) <2 and abs(col - white_king_pos[1]) <2:
            return True

        # Check by bishop or queen diagonally
        diagonals = self.get_diagonals(row,col) # Get strings of symbols in both diagonals
        diag1 = diagonals[0]
        diag2 = diagonals[1]

        # Remove empty squares in these strings then look for checks
        cleaned_diag1 =""
        cleaned_diag2 = ""
        for x in diag1:
            if x=='.':
                pass
            else:
                cleaned_diag1 += x
        if cleaned_diag1.find('kQ')!=-1 or cleaned_diag1.find('kB')!=-1:
            return True
        if cleaned_diag1.find('Qk')!=-1 or cleaned_diag1.find('Bk')!=-1:
            return True

        for x in diag2:
            if x=='.':
                pass
            else:
                cleaned_diag2 += x
        if cleaned_diag2.find('kQ')!=-1 or cleaned_diag2.find('kB')!=-1:
            return True
        if cleaned_diag2.find('Qk')!=-1 or cleaned_diag2.find('Bk')!=-1:
            return True


        # Check by rook or queen horizontally and vertically
        horizontal = self.get_rank(row)     # Get strings of symbols in both directions
        vertical = self.get_file(col)

        # Remove empty spaces in these strings then look for checks
        cleaned_horizontal = ""
        for x in horizontal:
            if x=='.':
                pass
            else:
                cleaned_horizontal += x
        if cleaned_horizontal.find('kQ')!=-1 or cleaned_horizontal.find('kR')!=-1:
            return True
        if cleaned_horizontal.find('Qk')!=-1 or cleaned_horizontal.find('Rk')!=-1:
            return True

        cleaned_vertical = ""
        for x in vertical:
            if x=='.':
                pass
            else:
                cleaned_vertical += x
        if cleaned_vertical.find('kQ')!=-1 or cleaned_vertical.find('kR')!=-1:
            return True
        if cleaned_vertical.find('Qk')!=-1 or cleaned_vertical.find('Rk')!=-1:
            return True


        # If we reach here the black king is not in check so return false
        return False

    def board_to_string(self):
        board_string = ''
        for i in range(8):
            for j in range(8):
                if self.pieces[i][j]==None:
                    board_string += '.'
                else:
                    board_string += self.pieces[i][j].symbol
        return board_string