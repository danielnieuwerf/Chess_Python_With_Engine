import pygame
import copy
import random

# Initialise Pygame
pygame.init()

width, height = 800, 800
rows, columns = 8, 8
square = 80
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_icon(pygame.image.load('blackpawn.png')) # Icon
pygame.display.set_caption("Python Chess")  # Set Caption
# Piece classes
class Piece():
    def __init__(self):
        self.image = None
        self.value = 0.0
        self.white = True
        self.symbol = 'x'

    def __deepcopy__(self,memo):
        cp = Piece()
        cp.value = self.value
        cp.white = self.white
        cp.symbol = self.symbol
        return copy.copy(cp)


class Black_Pawn(Piece):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('blackpawn.png')
        self.image = pygame.transform.scale(self.image, (square, square))
        self.value = -1
        self.white = False
        self.symbol = 'p'

class Black_Rook(Piece):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('blackrook.png')
        self.image = pygame.transform.scale(self.image, (square, square))
        self.value = -5
        self.white = False
        self.symbol = 'r'

class Black_Knight(Piece):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('blackknight.png')
        self.image = pygame.transform.scale(self.image, (square, square))
        self.value = -3
        self.white = False
        self.symbol = 'n'

class Black_Bishop(Piece):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('blackbishop.png')
        self.image = pygame.transform.scale(self.image, (square, square))
        self.value = -3.15
        self.white = False
        self.symbol = 'b'

class Black_Queen(Piece):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('blackqueen.png')
        self.image = pygame.transform.scale(self.image, (square, square))
        self.value = -9
        self.white = False
        self.symbol = 'q'

class Black_King(Piece):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('blackking.png')
        self.image = pygame.transform.scale(self.image, (square, square))
        self.value = 0
        self.white = False
        self.symbol = 'k'

class White_Pawn(Piece):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('whitepawn.png')
        self.image = pygame.transform.scale(self.image, (square, square))
        self.value = 1
        self.white = True
        self.symbol = 'P'

class White_Rook(Piece):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('whiterook.png')
        self.image = pygame.transform.scale(self.image, (square, square))
        self.value = 5
        self.white = True
        self.symbol = 'R'

class White_Knight(Piece):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('whiteknight.png')
        self.image = pygame.transform.scale(self.image, (square, square))
        self.value = 3
        self.white = True
        self.symbol = 'N'

class White_Bishop(Piece):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('whitebishop.png')
        self.image = pygame.transform.scale(self.image, (square, square))
        self.value = 3.15
        self.white = True
        self.symbol = 'B'

class White_Queen(Piece):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('whitequeen.png')
        self.image = pygame.transform.scale(self.image, (square, square))
        self.value = 9
        self.white = True
        self.symbol = 'Q'

class White_King(Piece):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('whiteking.png')
        self.image = pygame.transform.scale(self.image, (square, square))
        self.value = 0
        self.white = True
        self.symbol = 'K'


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
                file += "." # Empty square

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
                rank += "." # Empty square

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
        # If try to move an empty square return
        try:
            sym = self.pieces[i][j].symbol
        except:
            return

        # Check if enpassant move was made
        if abs(i-x)==1 and abs(j-y)==1: #Diagonal move by 1
            if self.pieces[x][y]==None and self.pieces[i][j].symbol in ['p','P']:   # If this we have en passant
                self.pieces[i][y] = None    # Delete captured pawn by enpassant and move the capturing pawn later in the function
        
        # Check if castling move was made
        if self.pieces[i][j].symbol in ['k', 'K'] and self.pieces[x][y] == None and abs(j-y)==2 and i==x:  # Castling condition
            if y==1:
                if x==0:
                    self.pieces[x][2]= White_Rook()
                else:
                    self.pieces[x][2]= Black_Rook()
                self.pieces[x][0]= None # Moves Rook (King is moved later on in this function)
            elif y==5:
                if x==0:
                    self.pieces[x][4]= White_Rook()
                else:
                    self.pieces[x][4] = Black_Rook()
                self.pieces[x][7]= None


        # move piece at i,j to x,y
        temp = self.pieces[i][j]
        self.pieces[i][j] = None
        self.pieces[x][y] = temp

        # Check for pawn promotion
        self.pawn_promotion()

    def pawn_promotion(self):
        for i in range(8):
            if self.pieces[0][i]!= None and self.pieces[0][i].symbol=='p':
                self.pieces[0][i]= Black_Queen()
            if self.pieces[7][i]!= None and self.pieces[7][i].symbol=='P':
                self.pieces[7][i]= White_Queen()

    def white_king_position(self):
        i, j = 0, 0 # Indexes
        for row in self.pieces:
            j = 0
            for piece in row:
                if piece!=None and piece.symbol == 'K':
                    return [i,j]
                j+=1
            i+=1
        return [-1,-1]

    def black_king_position(self):
        i, j = 0, 0 # Indexes
        for row in self.pieces:
            j = 0
            for piece in row:
                if piece!=None and piece.symbol == 'k':
                    return [i,j]
                j+=1
            i+=1
        return [-1,-1]

    def white_king_is_in_check(self):
        white_king_pos = self.white_king_position()
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
        black_king_pos =self.black_king_position()
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
        black_king_pos = self.black_king_position()
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
        white_king_pos =self.white_king_position()
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

class Game():
    def __init__(self):
        self.white_king_can_castle = True
        self.black_king_can_castle = True
        self.white_turn = True
        self.gameover, self.checkmate, self.stalemate = False, False, False
        self.gameIsDraw, self.white_won, self.black_won = False, False, False
        self.board = Board()
        self.selected_square = None  # i,j or None
        self.previous_move = None     # Used in en passant logic
        self.current_legal_moves = self.legal_moves()    # A list of all legal moves
        self.board_states = {}     # A mapping from board strings to how many times such a string has occurred in the game
        self.move_number = 0       

    def draw_window(self, surface):
        # Draw empty board
        WHITE = (238,238,210)
        DARK = (118,150,86)
        for i in range(0,8):
            for j in range(0,8):
                if (i+j) % 2 ==1:
                    pygame.draw.rect(surface, DARK, ((i*square, j*square), (square,square))) # dark squares
                else:
                    pygame.draw.rect(surface, WHITE, ((i*square, j*square), (square,square))) # light squares
        
        # Highlight selected square
        if self.selected_square!= None:
            i,j = self.selected_square
            if (i+j)%2 ==1:
                pygame.draw.rect(surface, (100,100,100), ((j*square, i*square), (square,square)))
            else:
                pygame.draw.rect(surface, (150,150,150), ((j*square, i*square), (square,square)))

        # Draw pieces on board
        for i in range(8):
            for j in range(8):
                try:
                    surface.blit(self.board.pieces[i][j].image, (j*square, i*square))
                except:
                    pass

        pygame.display.update()

    def resign(self):
        self.gameover = True
        if self.white_turn:
            self.black_won = True
        else:
            self.white_won = True

    def is_checkmate(self):
        # If w/b turn and w/b king is in check and number of legal moves is 0 return true 
        if self.white_turn and len(self.current_legal_moves)==0 and self.board.white_king_is_in_check():
            return True
        if (not self.white_turn) and len(self.current_legal_moves)==0 and self.board.black_king_is_in_check():
            return True
        return False    

    def is_stalemate(self):
        if len(self.current_legal_moves)==0 and (not self.board.black_king_is_in_check()) and (not self.board.white_king_is_in_check()):
            return True
        return False

    def is_draw_by_threefold_repetition(self):
        for value in self.board_states.values():
            if value == 3:
                return True
        return False

    def legal_moves(self):
        moves = []  # Store legal moves here

        # White's move (loop thorugh board to find white pieces)
        if self.white_turn:
            for i in range(8):
                for j in range(8):
                # Piece must be white
                    if self.board.pieces[i][j]!= None and self.board.pieces[i][j].white:                        
                        # Pawn
                        if self.board.pieces[i][j].symbol == 'P':
                            if i<7 and self.board.pieces[i+1][j]==None:
                                moves.append([i,j,i+1,j])   # Move one square forward
                            if i == 1 and self.board.pieces[2][j]==None and self.board.pieces[3][j]==None:
                                moves.append([i,j,i+2,j])   # Move two squares forward on
                            if i<7 and j<7 and (self.board.pieces[i+1][j+1]!= None and not self.board.pieces[i+1][j+1].white):
                                moves.append([i,j,i+1,j+1]) # Capture piece
                            if i<7 and j>0 and (self.board.pieces[i+1][j-1]!= None and not self.board.pieces[i+1][j-1].white):
                                moves.append([i,j,i+1,j-1]) # Capture piece
                        
                        # Knight
                        elif self.board.pieces[i][j].symbol == 'N':
                            if i>0 and j>1 and ((self.board.pieces[i-1][j-2]==None) or (not self.board.pieces[i-1][j-2].white)):
                                moves.append([i,j,i-1,j-2])
                            if i>0 and j<6 and ((self.board.pieces[i-1][j+2]==None) or (not self.board.pieces[i-1][j+2].white)):
                                moves.append([i,j,i-1,j+2])
                            if i>1 and j<7 and ((self.board.pieces[i-2][j+1]==None) or (not self.board.pieces[i-2][j+1].white)):
                                moves.append([i,j,i-2,j+1])
                            if i>1 and j>0 and ((self.board.pieces[i-2][j-1]==None) or (not self.board.pieces[i-2][j-1].white)):
                                moves.append([i,j,i-2,j-1])
                            if i<7 and j>1 and ((self.board.pieces[i+1][j-2]==None) or (not self.board.pieces[i+1][j-2].white)):
                                moves.append([i,j,i+1,j-2])
                            if i<7 and j<6 and ((self.board.pieces[i+1][j+2]==None) or (not self.board.pieces[i+1][j+2].white)):
                                moves.append([i,j,i+1,j+2])
                            if i<6 and j<7 and ((self.board.pieces[i+2][j+1]==None) or (not self.board.pieces[i+2][j+1].white)):
                                moves.append([i,j,i+2,j+1])
                            if i<6 and j>0 and ((self.board.pieces[i+2][j-1]==None) or (not self.board.pieces[i+2][j-1].white)):
                                moves.append([i,j,i+2,j-1])


                        # King
                        elif self.board.pieces[i][j].symbol == 'K':
                            if i>0 and ((self.board.pieces[i-1][j]==None) or (not self.board.pieces[i-1][j].white)):
                                moves.append([i,j,i-1,j])
                            if i>0 and j>0 and ((self.board.pieces[i-1][j-1]==None) or (not self.board.pieces[i-1][j-1].white)):
                                moves.append([i,j,i-1,j-1])
                            if i>0 and j<7 and ((self.board.pieces[i-1][j+1]==None) or (not self.board.pieces[i-1][j+1].white)):
                                moves.append([i,j,i-1,j+1])
                            if i<7 and ((self.board.pieces[i+1][j]==None) or (not self.board.pieces[i+1][j].white)):
                                moves.append([i,j,i+1,j])
                            if i<7 and j>0 and ((self.board.pieces[i+1][j-1]==None) or (not self.board.pieces[i+1][j-1].white)):
                                moves.append([i,j,i+1,j-1])
                            if i<7 and j<7 and ((self.board.pieces[i+1][j+1]==None) or (not self.board.pieces[i+1][j+1].white)):
                                moves.append([i,j,i+1,j+1])
                            if j>0 and ((self.board.pieces[i][j-1]==None) or (not self.board.pieces[i][j-1].white)):
                                moves.append([i,j,i,j-1])
                            if j<7 and ((self.board.pieces[i][j+1]==None) or (not self.board.pieces[i][j+1].white)):
                                moves.append([i,j,i,j+1])
                            

                        # Vertical and horizontal moves by rooks and queens
                        elif self.board.pieces[i][j].symbol in ['R','Q']:
                            up, down, right, left = 0,0,0,0 # Indicates how many squares the piece can move in each direction
                            file_string = self.board.get_file(j)    
                            rank_string = self.board.get_rank(i)

                            if j<7: # Right
                                x = j+1
                                while x<8 and rank_string[x]=='.':
                                    x+=1
                                    right+=1

                                # If blocked by an opposite colour piece can capture it
                                if x<8 and rank_string[x].islower():
                                    right += 1

                            if j>0: # Left
                                x = j - 1
                                while x>-1 and rank_string[x]=='.':
                                    x-=1
                                    left+=1

                                # If blocked by an opposite colour piece can capture it
                                if x>-1 and rank_string[x].islower():
                                    left += 1

                            if i>0: # Down (in column index)
                                x = i - 1
                                while x>-1 and file_string[x]=='.':
                                    x-=1
                                    down+=1

                                # If blocked by an opposite colour piece can capture it
                                if x>-1 and file_string[x].islower():
                                    down+=1

                            if i<7: # Up
                                x = i+1
                                while x<8 and file_string[x]=='.':
                                    x += 1
                                    up += 1
                                # If blocked by an opposite colour piece can capture it
                                if x<8 and file_string[x].islower():
                                    up += 1

                            # Add all up down left right moves to moves 
                            if right>0:
                                for x in range(1,right+1):    
                                    moves.append([i,j,i,j+x])

                            if left>0:
                                for x in range(1,left+1):
                                    moves.append([i,j,i,j-x])
                            if up>0:
                                for x in range(1,up+1):
                                    moves.append([i,j,i+x,j])
                            if down>0:
                                for x in range(1,down+1):
                                    moves.append([i,j,i-x,j])


                        # Diagonal moves by bishops and queens
                        if self.board.pieces[i][j].symbol in ['B','Q']:
                            diagonals = self.board.get_diagonals(i,j)
                            diag1, diag2 = diagonals[0], diagonals[1] # These are strings of length 8 like 'q.r..B..'
                            up_right, up_left , down_right, down_left = 0,0,0,0 # Indicates how many squares the piece can move in each direction

                            # South east diagonal (diag1)
                            if not (i==7 or j==7):  # Down + right
                                x = min(i,j)+1    # min(i,j) is index of our piece in the diag1 string
                                while x<len(diag1) and diag1[x]=='.':
                                    down_right += 1
                                    x += 1
                                # If blocked by an opposite colour piece can capture it
                                if x!=len(diag1) and diag1[x].islower():
                                    down_right += 1

                            if not (i==0 or j==0):  # Up + left
                                x = min(i,j) - 1    # min(i,j) is index of our piece in the diag1 string
                                while x>-1 and diag1[x]=='.':
                                    up_left += 1
                                    x -=1
                                # If blocked by an opposite colour piece can capture it
                                if x!=-1 and diag1[x].islower():
                                    up_left += 1                            

                            # South west diagonal (diag2)
                            if not (i==7 or j==0):  # Down + left
                                x = min(i,7-j)+1  # min(i,7-j) is index of our piece in the diag2 string
                                while x<len(diag2) and diag2[x]=='.':
                                    down_left += 1
                                    x += 1
                                # If blocked by an opposite colour piece can capture it
                                if x!=len(diag2) and diag2[x].islower():
                                    down_left += 1 

                            if not (i==0 or j==7):  # Up + right
                                x = min(i,7-j)-1  # min(i,7-j) is index of our piece in the diag2 string
                                while x>-1 and diag2[x]=='.':
                                    up_right += 1
                                    x -= 1
                                # If blocked by an opposite colour piece can capture it
                                if x!=-1 and diag2[x].islower():
                                    up_right += 1

                            # Add all the up and down (left and right) moves to moves 
                            if up_right>0:
                                for x in range(1,up_right+1):    
                                    moves.append([i,j,i-x,j+x])
                            if up_left>0:
                                for x in range(1,up_left+1):
                                    moves.append([i,j,i-x,j-x])
                            if down_right>0:
                                for x in range(1,down_right+1):
                                    moves.append([i,j,i+x,j+x])
                            if down_left>0:
                                for x in range(1,down_left+1):
                                    moves.append([i,j,i+x,j-x])

        # Black's turn (loop through board to find black pieces)
        else:
            for i in range(8):
                for j in range(8):
                # Piece must be black
                    if self.board.pieces[i][j]!= None and not self.board.pieces[i][j].white:                        
                        # Pawn
                        if self.board.pieces[i][j].symbol == 'p':
                            if i>0 and self.board.pieces[i-1][j]==None:
                                moves.append([i,j,i-1,j])   # Move one square forward
                            if i == 6 and self.board.pieces[5][j]==None and self.board.pieces[4][j]==None:
                                moves.append([i,j,4,j])   # Move two squares forward on
                            if i>0 and j<7 and (self.board.pieces[i-1][j+1]!= None and self.board.pieces[i-1][j+1].white):
                                moves.append([i,j,i-1,j+1]) # Capture piece
                            if i>0 and j>0 and (self.board.pieces[i-1][j-1]!= None and self.board.pieces[i-1][j-1].white):
                                moves.append([i,j,i-1,j-1]) # Capture piece
                        
                        # Knight
                        elif self.board.pieces[i][j].symbol == 'n':
                            if i>0 and j>1 and ((self.board.pieces[i-1][j-2]==None) or (self.board.pieces[i-1][j-2].white)):
                                moves.append([i,j,i-1,j-2])
                            if i>0 and j<6 and ((self.board.pieces[i-1][j+2]==None) or (self.board.pieces[i-1][j+2].white)):
                                moves.append([i,j,i-1,j+2])
                            if i>1 and j<7 and ((self.board.pieces[i-2][j+1]==None) or (self.board.pieces[i-2][j+1].white)):
                                moves.append([i,j,i-2,j+1])
                            if i>1 and j>0 and ((self.board.pieces[i-2][j-1]==None) or (self.board.pieces[i-2][j-1].white)):
                                moves.append([i,j,i-2,j-1])
                            if i<7 and j>1 and ((self.board.pieces[i+1][j-2]==None) or (self.board.pieces[i+1][j-2].white)):
                                moves.append([i,j,i+1,j-2])
                            if i<7 and j<6 and ((self.board.pieces[i+1][j+2]==None) or (self.board.pieces[i+1][j+2].white)):
                                moves.append([i,j,i+1,j+2])
                            if i<6 and j<7 and ((self.board.pieces[i+2][j+1]==None) or (self.board.pieces[i+2][j+1].white)):
                                moves.append([i,j,i+2,j+1])
                            if i<6 and j>0 and ((self.board.pieces[i+2][j-1]==None) or (self.board.pieces[i+2][j-1].white)):
                                moves.append([i,j,i+2,j-1])


                        # King
                        elif self.board.pieces[i][j].symbol == 'k':
                            if i>0 and ((self.board.pieces[i-1][j]==None) or (self.board.pieces[i-1][j].white)):
                                moves.append([i,j,i-1,j])
                            if i>0 and j>0 and ((self.board.pieces[i-1][j-1]==None) or (self.board.pieces[i-1][j-1].white)):
                                moves.append([i,j,i-1,j-1])
                            if i>0 and j<7 and ((self.board.pieces[i-1][j+1]==None) or (self.board.pieces[i-1][j+1].white)):
                                moves.append([i,j,i-1,j+1])
                            if i<7 and ((self.board.pieces[i+1][j]==None) or (self.board.pieces[i+1][j].white)):
                                moves.append([i,j,i+1,j])
                            if i<7 and j>0 and ((self.board.pieces[i+1][j-1]==None) or (self.board.pieces[i+1][j-1].white)):
                                moves.append([i,j,i+1,j-1])
                            if i<7 and j<7 and ((self.board.pieces[i+1][j+1]==None) or (self.board.pieces[i+1][j+1].white)):
                                moves.append([i,j,i+1,j+1])
                            if j>0 and ((self.board.pieces[i][j-1]==None) or (self.board.pieces[i][j-1].white)):
                                moves.append([i,j,i,j-1])
                            if j<7 and ((self.board.pieces[i][j+1]==None) or (self.board.pieces[i][j+1].white)):
                                moves.append([i,j,i,j+1])
                            

                        # Vertical and horizontal moves by rooks and queens
                        elif self.board.pieces[i][j].symbol in ['r','q']:
                            up, down, right, left = 0,0,0,0 # Indicates how many squares the piece can move in each direction
                            file_string = self.board.get_file(j)    
                            rank_string = self.board.get_rank(i)

                            if j<7: # Right
                                x = j+1
                                while x<8 and rank_string[x]=='.':
                                    x+=1
                                    right+=1

                                # If blocked by an opposite colour piece can capture it
                                if x<8 and rank_string[x].isupper():
                                    right += 1

                            if j>0: # Left
                                x = j - 1
                                while x>-1 and rank_string[x]=='.':
                                    x-=1
                                    left+=1

                                # If blocked by an opposite colour piece can capture it
                                if x>-1 and rank_string[x].isupper():
                                    left += 1

                            if i>0: # Down (in column index)
                                x = i - 1
                                while x>-1 and file_string[x]=='.':
                                    x-=1
                                    down+=1

                                # If blocked by an opposite colour piece can capture it
                                if x>-1 and file_string[x].isupper():
                                    down+=1

                            if i<7: # Up
                                x = i+1
                                while x<8 and file_string[x]=='.':
                                    x += 1
                                    up += 1
                                # If blocked by an opposite colour piece can capture it
                                if x<8 and file_string[x].isupper():
                                    up += 1

                            # Add all up down left right moves to moves 
                            if right>0:
                                for x in range(1,right+1):    
                                    moves.append([i,j,i,j+x])

                            if left>0:
                                for x in range(1,left+1):
                                    moves.append([i,j,i,j-x])
                            if up>0:
                                for x in range(1,up+1):
                                    moves.append([i,j,i+x,j])
                            if down>0:
                                for x in range(1,down+1):
                                    moves.append([i,j,i-x,j])


                        # Diagonal moves by bishops and queens
                        if self.board.pieces[i][j].symbol in ['b','q']:
                            diagonals = self.board.get_diagonals(i,j)
                            diag1, diag2 = diagonals[0], diagonals[1] # These are strings of length 8 like 'q.r..B..'
                            up_right, up_left , down_right, down_left = 0,0,0,0 # Indicates how many squares the piece can move in each direction

                            # South east diagonal (diag1)
                            if not (i==7 or j==7):  # Down + right
                                x = min(i,j)+1    # min(i,j) is index of our piece in the diag1 string
                                while x<len(diag1) and diag1[x]=='.':
                                    down_right += 1
                                    x += 1
                                # If blocked by an opposite colour piece can capture it
                                if x!=len(diag1) and diag1[x].isupper():
                                    down_right += 1

                            if not (i==0 or j==0):  # Up + left
                                x = min(i,j) - 1    # min(i,j) is index of our piece in the diag1 string
                                while x>-1 and diag1[x]=='.':
                                    up_left += 1
                                    x -=1
                                # If blocked by an opposite colour piece can capture it
                                if x!=-1 and diag1[x].isupper():
                                    up_left += 1                            

                            # South west diagonal (diag2)
                            if not (i==7 or j==0):  # Down + left
                                x = min(i,7-j)+1  # min(i,7-j) is index of our piece in the diag2 string
                                while x<len(diag2) and diag2[x]=='.':
                                    down_left += 1
                                    x += 1
                                # If blocked by an opposite colour piece can capture it
                                if x!=len(diag2) and diag2[x].isupper():
                                    down_left += 1 

                            if not (i==0 or j==7):  # Up + right
                                x = min(i,7-j)-1  # min(i,7-j) is index of our piece in the diag2 string
                                while x>-1 and diag2[x]=='.':
                                    up_right += 1
                                    x -= 1
                                # If blocked by an opposite colour piece can capture it
                                if x!=-1 and diag2[x].isupper():
                                    up_right += 1

                            # Add all the up and down (left and right) moves to moves 
                            if up_right>0:
                                for x in range(1,up_right+1):    
                                    moves.append([i,j,i-x,j+x])
                            if up_left>0:
                                for x in range(1,up_left+1):
                                    moves.append([i,j,i-x,j-x])
                            if down_right>0:
                                for x in range(1,down_right+1):
                                    moves.append([i,j,i+x,j+x])
                            if down_left>0:
                                for x in range(1,down_left+1):
                                    moves.append([i,j,i+x,j-x])
        

        # White captures with en passant
        prev_move = self.previous_move
        black_pawn_moves = []
        for i in range(8):
            black_pawn_moves.append([6,i,4,i])     # All possible moves 2 forward by black pawn
        if self.white_turn and prev_move in black_pawn_moves:
            # Must have a white pawn at [4, i+-1] if prev move [6,i,4,i]
            if prev_move[1]>0 and self.board.pieces[4][prev_move[1]-1]!=None and self.board.pieces[4][prev_move[1]-1].symbol=='P':
                moves.append([4,prev_move[1]-1,5,prev_move[1]])
            if prev_move[1]<7 and self.board.pieces[4][prev_move[1]+1]!=None and self.board.pieces[4][prev_move[1]+1].symbol=='P':
                moves.append([4,prev_move[1]+1,5,prev_move[1]])

        # Black captures with en passant
        prev_move = self.previous_move
        white_pawn_moves = []
        for i in range(8):
            white_pawn_moves.append([1,i,3,i])     # All possible moves 2 forward by white pawn
        if self.white_turn== False and prev_move in white_pawn_moves:
            # Must have a black pawn at [3, i+-1] if prev move [1,i,3,i]
            if prev_move[1]>0 and self.board.pieces[3][prev_move[1]-1]!=None and self.board.pieces[3][prev_move[1]-1].symbol=='p':
                moves.append([3,prev_move[1]-1,2,prev_move[1]])
            if prev_move[1]<7 and self.board.pieces[3][prev_move[1]+1]!=None and self.board.pieces[3][prev_move[1]+1].symbol=='p':
                moves.append([3,prev_move[1]+1,2,prev_move[1]])
            
        # Castling
        if self.white_turn and self.white_king_can_castle:
            rank0 = self.board.get_rank(0)  # If white king can castle we know the white king is at [0][3]
            if rank0.find('R..K')!=-1 and not self.board.king_side_castle_blocked(self.white_turn):
                moves.append([0,3,0,1])
            if rank0.find('K...R')!=-1 and not self.board.queen_side_castle_blocked(self.white_turn):
                moves.append([0,3,0,5])
        if (not self.white_turn) and self.black_king_can_castle:
            rank7 = self.board.get_rank(7)  # If black king can castle we know the black king is at [7][3]
            if rank7.find('r..k')!=-1 and not self.board.king_side_castle_blocked(self.white_turn):
                moves.append([7,3,7,1])
            if rank7.find('k...r')!=-1 and not self.board.queen_side_castle_blocked(self.white_turn):
                moves.append([7,3,7,5])
        

        # Make the move on a copy board if it's invalid do not add it to valid_moves
        valid_moves = []
        for move in moves:
            copy_board = copy.deepcopy(self.board)
            copy_board.make_move(move[0],move[1],move[2],move[3])  # Make move on copy board

            if not self.white_turn and copy_board.black_king_is_in_check():
                pass
            elif self.white_turn and copy_board.white_king_is_in_check():
                pass
            else:
                valid_moves.append(move)

        return valid_moves

    def handle_new_successfully_made_move(self, move):
    # If a new move has been made update current_legal_moves and check for gameover etc...
        self.selected_square = None     # Unselect square
        self.white_turn = not self.white_turn   # Flip turn
        self.previous_move = move  # Update previous move
        board_string = self.board.board_to_string()  # Add to board states for 3fold repetition rule
        self.move_number += 1       # Update move number
        if board_string in self.board_states.keys():
            self.board_states[board_string] +=1
        else:
            self.board_states[board_string] = 1

        self.current_legal_moves = self.legal_moves()   # Calculate new legal moves


        # If a king move was made change castability to false
        self.update_castlability()

        # Draw by threefold repetition
        if self.is_draw_by_threefold_repetition():
            self.gameIsDraw = True
            self.gameover = True
            print('draw by threefold repetition')

        # Check for checkmate
        if self.is_checkmate():
            self.checkmate = True
            self.gameover = True
            if self.white_turn:
                self.black_won = True
            else:
                self.white_won = True
            print('checkmate')

        # Draw by lack of material
        if self.board.is_draw_by_lack_of_material():
            self.gameIsDraw = True
            self.gameover = True
            print('draw by lack of material')

        # Check for stalemate
        if self.is_stalemate():
            self.gameIsDraw = True
            self.gameover = True
            print('draw by stalemate')

    def update_castlability(self):
        # If a king move was made change castlability to false
        prev_move = self.previous_move
        if prev_move == None:   # Must have a previous move
            return 
        if self.board.pieces[prev_move[2]][prev_move[3]]== None: # Must not be an empty square
            return
        if self.board.pieces[prev_move[2]][prev_move[3]].symbol=='k':
            self.black_king_can_castle = False
        elif self.board.pieces[prev_move[2]][prev_move[3]].symbol=='K':
            self.white_king_can_castle = False
    
    def evaluate_position_score(self):
        # Returns score to evaluate current position
        score = 0.0   # Initialise score to 0

        # If checkmate return +- infinity only check for this if it is check
        if self.black_won:
            return -1000000
        if self.white_won:
            return 10000000

        # If draw return 0
        if self.gameIsDraw:
            return 0

        # Count all the pieces on the board
        for i in range(8):
            for j in range(8):
                try:
                    score += self.board.pieces[i][j].value
                except:
                    pass


        # Bonus for check
        if self.board.white_king_is_in_check():
            score -=0.03
        elif self.board.black_king_is_in_check():
            score += 0.03

        # Bonus for manuveurability

        if self.white_turn:
            score += len(self.current_legal_moves)*0.003
        else:
            score -= len(self.current_legal_moves)*0.003

        # Add value for capturable pieces
        max_capture = 0
        for move in self.current_legal_moves:
            try:
                if self.board.pieces[move[2]][move[3]].white != self.white_turn:    # Find capturing moves
                    capture_value = abs(self.board.pieces[move[2]][move[3]].value)-abs(self.board.pieces[move[0]][move[1]].value)
                if capture_value>max_capture:
                    max_capture = copy.copy(capture_value)
            except:
                pass
        if self.white_turn:
            score += max_capture*0.7
        else:
            score -= max_capture*0.7

        # Penalty for knights on edge of board
        for i in [0,7]:
            file = self.board.get_file_without_empty_squares(i)
            for x in file:
                if x=='n':
                    score+= 0.1
                elif x=='N':
                    score-=0.1

        # Number of developed pieces bonus
        rank_white = self.board.get_rank_without_empty_squares(0)
        rank_black = self.board.get_rank_without_empty_squares(7)
        white_count, black_count = 0,0  #number of undeveloped pieces
        for x in rank_black:
            if x in ['b','r','n','q']:
                black_count +=1
        for x in rank_white:
            if x in ['B','R','N','Q']:
                white_count +=1
        
        score += 0.02*black_count   # Apply bonus
        score -= 0.02*white_count

        # Bonus points for kicking an opponents piece with a pawn
        for i in range(8):
            for j in range(8):
                if self.board.pieces[i][j]!=None and self.board.pieces[i][j].symbol=='P':
                    if j>0 and self.board.pieces[i+1][j-1]!=None and self.board.pieces[i+1][j-1].symbol in ['k', 'n', 'b', 'r','q']:
                        score+= 0.04
                    if j<7 and self.board.pieces[i+1][j+1]!=None and self.board.pieces[i+1][j+1].symbol in ['k', 'n', 'b', 'r','q']:
                        score+= 0.04
                if self.board.pieces[i][j]!=None and self.board.pieces[i][j].symbol=='p':
                    if j>0 and self.board.pieces[i-1][j-1]!=None and self.board.pieces[i-1][j-1].symbol in ['K', 'N', 'B', 'R','Q']:
                        score-= 0.04
                    if j<7 and self.board.pieces[i-1][j+1]!=None and self.board.pieces[i-1][j+1].symbol in ['K', 'N', 'B', 'R','Q']:
                        score-= 0.04

        # Control of centre
        # for each pawn in centre gain points only before move 18
        if self.move_number <18:
            for i in range(2,5):
                for j in range(3,6):
                    if self.board.pieces[i][j]!=None and self.board.pieces[i][j].symbol=='P':
                        score += 0.1

            for i in range(3,6):
                for j in range(3,6):
                    if self.board.pieces[i][j]!=None and self.board.pieces[i][j].symbol=='p':
                        score-=0.1

        # Double pawn penalty (triple pawn etc...)
        for i in range(8):
            file = self.board.get_file(i)
            white_pawns, black_pawns = 0, 0 # Number of white and black pawns in the file
            for x in file:
                if x=='p':
                    black_pawns+=1
                elif x=='P':
                    white_pawns+=1

            if white_pawns>1:
                score -= (1.08+white_pawns-3)
            elif black_pawns>1:
                score += (1.08+black_pawns-3)
        
        # Safe king
        # castling
        if self.move_number < 15:
            if self.board.pieces[0][1]!= None and self.board.pieces[0][1].symbol == 'K':
                score+=0.25
            if self.board.pieces[7][1]!= None and self.board.pieces[7][1].symbol =='k':
                score -= 0.25
            if self.board.pieces[0][5]!= None and self.board.pieces[0][5].symbol == 'K':
                score += 0.23
            if self.board.pieces[7][5]!= None and self.board.pieces[7][5].symbol == 'k':
                score -= 0.23

        # Connected rooks bonus
        for i in range(8):
            file = self.board.get_file_without_empty_squares(i)
            rank = self.board.get_rank_without_empty_squares(i)
            if file.find('rr')!=-1:
                score-=0.16
            elif file.find('RR')!=-1:
                score+=0.16
            if rank.find('rr')!=-1:
                score-=0.07
            elif rank.find('RR')!=-1:
                score+=0.07

        # End game
        if self.move_number > 30:
            # Ending with 3 pawns vs knight or bishop
            pass

        # Return score after adjustments
        return score

    def maximise_move_score(self):
        # Returns best move (depth 1) for white and black
        if self.white_turn:
            best_move = []
            best_score = -1000000
            for move in self.current_legal_moves:   # Try every legal white move
                copy_game = copy.deepcopy(self)     # on copy board
                copy_game.board.make_move(move[0],move[1],move[2],move[3])  # Make move on copy board
                copy_game.handle_new_successfully_made_move(move)   # Update castlability etc
                # Now it is Blacks turn... make all legal black moves
                min_score = 100000  # Make the best black move (min score move)
                for move2 in copy_game.current_legal_moves: 
                    #print('move2:', move2)
                    copy_copy_game = copy.deepcopy(copy_game)    # on copycopy board
                    copy_copy_game.board.make_move(move2[0],move2[1],move2[2],move2[3])  # Make move on copycopy board
                    copy_copy_game.handle_new_successfully_made_move(move2)   # Update castlability etc
                    score = copy_copy_game.evaluate_position_score()    # Evaluate score
                    # We wish to minimise this score
                    if min_score > score:
                        min_score = copy.copy(score)
                    
                if min_score>best_score:    # maximise these min scores
                    best_score = copy.deepcopy(min_score)
                    best_move = copy.deepcopy(move)
                if min_score == best_score:
                    x = random.randint(1,4) # For sake of variety
                    if x==3:    
                        best_score = copy.deepcopy(min_score)
                        best_move = copy.deepcopy(move)

            return best_move

        else:       # Black's turn
            best_move = []
            best_score = 1000000        # minimise score for black
            for move in self.current_legal_moves:   # Try every legal black move
                copy_game = copy.deepcopy(self)     # on copy board
                copy_game.board.make_move(move[0],move[1],move[2],move[3])  # Make move on copy board
                copy_game.handle_new_successfully_made_move(move)   # Update castlability etc
                # Now it is White's turn... make all legal black moves
                max_score = -100000  # Make the best white move (max score move)
                for move2 in copy_game.current_legal_moves: 
                    #print('move2:', move2)
                    copy_copy_game = copy.deepcopy(copy_game)    # on copycopy board
                    copy_copy_game.board.make_move(move2[0],move2[1],move2[2],move2[3])  # Make move on copycopy board
                    copy_copy_game.handle_new_successfully_made_move(move2)   # Update castlability etc
                    score = copy_copy_game.evaluate_position_score()    # Evaluate score
                    # We wish to minimise this score
                    if max_score < score:
                        max_score = copy.copy(score)
                    
                
                if max_score<best_score:    # minimise these max scores
                    best_score = copy.deepcopy(max_score)
                    best_move = copy.deepcopy(move)
                elif max_score == best_score:
                    x = random.randint(1,4) # For sake of variety
                    if x==3:    
                        best_score = copy.deepcopy(max_score)
                        best_move = copy.deepcopy(move)

            return best_move

    def engine_move_decision(self, depth = 1):
        if depth == 1:
            return self.maximise_move_score()

        elif depth>1:
            if self.white_turn:         # White turn
                max_score = -10000000
                for move in self.current_legal_moves:   # Try every legal white move
                    copy_game = copy.deepcopy(self)     # on copy board
                    copy_game.board.make_move(move[0],move[1],move[2],move[3])  # Make move on copy board
                    copy_game.handle_new_successfully_made_move(move)   # Update castlability etc
                    try:    # Try to make the best move depth-1 
                        best_move = copy_game.engine_move_decision(depth-1)
                        copy_game.board.make_move(best_move[0],best_move[1],best_move[2],best_move[3])    # Make best move
                        copy_game.handle_new_successfully_made_move(best_move)   # Update castlability etc
                    except: # Fails if game ends and there's no move depth-1
                        pass
                    score = copy_game.evaluate_position_score()
                    if score> max_score:
                        max_score = copy.copy(score)
                        move_decision = copy.deepcopy(move)
                    print(move)
                    print(score)
                return move_decision

            else:         # Black turn
                min_score = 10000000
                for move in self.current_legal_moves:   # Try every legal white move
                    copy_game = copy.deepcopy(self)     # on copy board
                    copy_game.board.make_move(move[0],move[1],move[2],move[3])  # Make move on copy board
                    copy_game.handle_new_successfully_made_move(move)   # Update castlability etc
                    try:    # Try to make the best move depth-1 
                        best_move = copy_game.engine_move_decision(depth-1)
                        copy_game.board.make_move(best_move[0],best_move[1],best_move[2],best_move[3])    # Make best move
                        copy_game.handle_new_successfully_made_move(best_move)   # Update castlability etc
                    except: # Fails if game ends and there's no move depth-1
                        pass
                    score = copy_game.evaluate_position_score()
                    print(move)
                    print(score)
                    if score< min_score:
                        max_score = copy.copy(score)
                        move_decision = copy.deepcopy(move)

                return move_decision


        return



# Game loop
new_game = Game()


# Engine is black, player is white
while new_game.gameover == False:
    # Draw game window
    new_game.draw_window(screen)

    # Listen for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:    
            new_game.gameover = True
        # Player turn 
        if new_game.white_turn:
            if event.type == pygame.MOUSEBUTTONDOWN:    
                x, y = pygame.mouse.get_pos()
                if x< 8*square and y<8*square:      # If click on board    
                    if new_game.selected_square == None:    # Select square
                        new_game.selected_square = y//square, x//square
                    else:   # If already selected try to make the move
                        i, j = new_game.selected_square
                        new_game.selected_square = y//square, x//square
                        # Move request successful
                        if [i,j,y//square,x//square] in new_game.current_legal_moves:
                            new_game.board.make_move(i,j,y//square,x//square)   # Make move
                            new_game.handle_new_successfully_made_move([i,j,y//square,x//square])
                            print(new_game.previous_move)
                            new_game.draw_window(screen)
                        # Move request unsuccessful
                        else:
                            new_game.selected_square = y//square, x//square     # Select new square

    # Engine move
    if not new_game.white_turn:
        try:
            engine_move = new_game.engine_move_decision(depth=1)
            new_game.board.make_move(engine_move[0],engine_move[1],engine_move[2],engine_move[3])   # Make move
            new_game.handle_new_successfully_made_move(engine_move)
            print(str(new_game.move_number)+" " +str(new_game.previous_move))
        except:
            print('Engine resigns')
            new_game.resign()
            
        




# 2 engines
while new_game.gameover==False:
    # Draw game window
    new_game.draw_window(screen)

    # Listen for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:    
            new_game.gameover = True
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass

    # Engine move
    if new_game.white_turn:
        engine_move = new_game.engine_move_decision(depth=1)
        new_game.board.make_move(engine_move[0],engine_move[1],engine_move[2],engine_move[3])   # Make move
        new_game.handle_new_successfully_made_move(engine_move)
        print(str(new_game.move_number)+" " +str(new_game.previous_move))
    else:
        engine_move = new_game.engine_move_decision(depth=1)
        new_game.board.make_move(engine_move[0],engine_move[1],engine_move[2],engine_move[3])   # Make move
        new_game.handle_new_successfully_made_move(engine_move)
        print(str(new_game.move_number)+" " +str(new_game.previous_move))
        
    # Check for game over
    if new_game.gameover:
        del new_game
        new_game = Game()
        print('GAMEOVER')




# Engine is white, player is black
while new_game.gameover == False:
    # Draw game window
    new_game.draw_window(screen)

    # Listen for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:    
            new_game.gameover = True
        # Player turn 
        if not new_game.white_turn:
            if event.type == pygame.MOUSEBUTTONDOWN:    
                x, y = pygame.mouse.get_pos()
                if x< 8*square and y<8*square:      # If click on board    
                    if new_game.selected_square == None:    # Select square
                        new_game.selected_square = y//square, x//square
                    else:   # If already selected try to make the move
                        i, j = new_game.selected_square
                        new_game.selected_square = y//square, x//square
                        # Move request successful
                        if [i,j,y//square,x//square] in new_game.current_legal_moves:
                            new_game.board.make_move(i,j,y//square,x//square)   # Make move
                            new_game.handle_new_successfully_made_move([i,j,y//square,x//square])
                            print(new_game.previous_move)
                            new_game.draw_window(screen)
                        # Move request unsuccessful
                        else:
                            new_game.selected_square = y//square, x//square     # Select new square

    # Engine move
    if new_game.white_turn:
        engine_move = new_game.engine_move_decision(depth=2)
        new_game.board.make_move(engine_move[0],engine_move[1],engine_move[2],engine_move[3])   # Make move
        new_game.handle_new_successfully_made_move(engine_move)
        print(str(new_game.move_number)+" " +str(new_game.previous_move))

    




# 2 Players
while True:
    # Draw game window
    new_game.draw_window(screen)

    # Listen for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:    
            new_game.gameover = True
            
        if event.type == pygame.MOUSEBUTTONDOWN:    
            x, y = pygame.mouse.get_pos()
            if x< 8*square and y<8*square:      # If click on board    
                if new_game.selected_square == None:    # Select square
                    new_game.selected_square = y//square, x//square
                else:   # If already selected try to make the move
                    i, j = new_game.selected_square
                    new_game.selected_square = y//square, x//square
                    # Move request successful
                    if [i,j,y//square,x//square] in new_game.current_legal_moves:
                        new_game.board.make_move(i,j,y//square,x//square)   # Make move
                        new_game.handle_new_successfully_made_move([i,j,y//square,x//square])
                        print(new_game.previous_move)
                    # Move request unsuccessful
                    else:
                        new_game.selected_square = y//square, x//square     # Select new square
         

    # Check for game over
    if new_game.gameover:
        del new_game
        new_game = Game()
        print('GAMEOVER')
