import pyximport; pyximport.install()
from Pieces import *
from Book import *
import random
from Endgames import *
from cprofilev import *
from CythonCharBoard import *
import cython

class Game():
    move_number : cython.int
    white_king_can_castle : cython.bint
    black_king_can_castle : cython.bint
    white_turn : cython.bint
    white_is_in_check : cython.bint
    black_is_in_check : cython.bint
    gameover : cython.bint
    checkmate : cython.bint
    stalemate : cython.bint
    gameIsDraw : cython.bint
    white_won : cython.bint
    black_won : cython.bint
    out_of_book : cython.bint

    def __init__(self):
        self.white_king_can_castle = True
        self.black_king_can_castle = True
        self.white_turn = True
        self.white_is_in_check = False
        self.black_is_in_check = False
        self.move_number = 1
        self.gameover, self.checkmate, self.stalemate = False, False, False
        self.gameIsDraw, self.white_won, self.black_won = False, False, False
        self.out_of_book = False
        self.book = Book()
        self.board = CCharBoard()
        self.selected_SQUARE = None  # i,j or None
        self.previous_move = [7,0,7,0]     # Used in en passant logic
        self.board_states = {}     # A mapping from board strings to how many times such a string has occurred in the game
        self.current_legal_moves = []
        self.current_legal_moves = self.legal_moves()    # A list of all legal moves
         
    def resign(self):
        self.gameover = True
        if self.white_turn:
            self.black_won = True
        else:
            self.white_won = True

    def is_check(self):
        # If white turn check if white king is under threat
        if self.white_turn:
            threats_bb = self.board.create_bitboard_direct_threats_to_king(True)
            if threats_bb.bits[self.board.white_king_position[0]][self.board.white_king_position[1]] == 1:
                self.white_is_in_check = True
        # Same for black king
        else:
            threats_bb = self.board.create_bitboard_direct_threats_to_king(False)
            if threats_bb.bits[self.board.black_king_position[0]][self.board.black_king_position[1]] == 1:
                self.black_is_in_check = True

    def is_checkmate(self):
        # If w/b turn and w/b king is in check and number of legal moves is 0 return true 
        if (self.white_is_in_check or self.black_is_in_check) and len(self.current_legal_moves)==0:
            return True
        return False    

    def is_stalemate(self):
        # No legal moves and not in check
        if len(self.current_legal_moves)==0 and not (self.black_is_in_check or self.white_is_in_check):
            return True
        return False

    def is_draw_by_threefold_repetition(self):
        for value in self.board_states.values():
            if value == 3:
                return True
        return False

    def update_check_status(self):
        # Updates check status
        prev_move = self.previous_move  # Previous move played- check if this piece revealed check or is checking opponents king
        prev_move_was_white = self.board.pieces[prev_move[2]][prev_move[3]].isupper()   # True if previous move was white piece
        prev_move_symbol = self.board.pieces[prev_move[2]][prev_move[3]]     # Symbol of previous move piece e.g 'k' for black king
        if prev_move_was_white: #Check if black king is now in check
            self.white_is_in_check = False  # White not in check
            # Revealed checks
                #
                #   MUST CONSIDER EN PASSANT DISCOVERED CHECK IN REVEALED SECTIONS
                #    AND DISCOVERED CASTLING CHECKS and pawn promo?
                #
            row, column = prev_move[0], prev_move[1]    # Row and column of initial position of previous move
            black_king_position = self.board.black_king_position
            if black_king_position[0]==row:    # If prev move initially shared a rank with black king
                rank = self.board.get_rank_without_empty_squares(row)
                if rank.find('kQ')!=-1 or rank.find('Qk')!=-1:
                    self.black_is_in_check = True
                    return
                if rank.find('Rk')!=-1 or rank.find('kR')!=-1:
                    self.black_is_in_check = True
                    return
            if black_king_position[1]==column:  # If prev move initially shared a file with black king
                file = self.board.get_file_without_empty_squares(column)
                if file.find('kQ')!=-1 or file.find('Qk')!=-1:
                    self.black_is_in_check = True
                    return
                if file.find('Rk')!=-1 or file.find('kR')!=-1:
                    self.black_is_in_check = True
                    return
            if abs(black_king_position[0]-row)==abs(black_king_position[1]-column): # If prev move initially shared a diagonal with black king
                diagonals = self.board.get_diagonals_without_empty_squares(black_king_position[0], black_king_position[1]) # Get strings of symbols in both diagonals 
                diag1 = diagonals[0]
                diag2 = diagonals[1]
                if diag1.find('kQ')!=-1 or diag1.find('kB')!=-1:
                    self.black_is_in_check = True
                    return
                if diag1.find('Qk')!=-1 or diag1.find('Bk')!=-1:
                    self.black_is_in_check = True
                    return
                if diag2.find('kQ')!=-1 or diag2.find('kB')!=-1:
                    self.black_is_in_check = True
                    return
                if diag2.find('Qk')!=-1 or diag2.find('Bk')!=-1:
                    self.black_is_in_check = True
                    return
            # Direct checks
            if prev_move_symbol == 'N':
                # Knight check
                if (abs(black_king_position[0]-prev_move[2])==2 and abs(black_king_position[1]-prev_move[3])==1) or (abs(black_king_position[0]-prev_move[2])==1 and abs(black_king_position[1]-prev_move[3])==2):
                    self.black_is_in_check = True
                    return
                else:
                    self.black_is_in_check = False
                    return
            if prev_move_symbol == 'P':   
                if black_king_position[0]==(1+prev_move[2]) and abs(black_king_position[1]-prev_move[3])==1:    # Column difference of 1 and black king pos row 1 more than pawn row
                    self.black_is_in_check = True
                    return
                else:
                    self.black_is_in_check = False
                    return
            if prev_move_symbol in ['B', 'Q']:
                diagonals = self.board.get_diagonals_without_empty_squares(black_king_position[0], black_king_position[1])  # Get both diagonals strings
                diag1 = diagonals[0]
                diag2 = diagonals[1]
                if diag1.find('kQ')!=-1 or diag1.find('kB')!=-1:
                    self.black_is_in_check = True
                    return
                if diag1.find('Qk')!=-1 or diag1.find('Bk')!=-1:
                    self.black_is_in_check = True
                    return
                if diag2.find('kQ')!=-1 or diag2.find('kB')!=-1:
                    self.black_is_in_check = True
                    return
                if diag2.find('Qk')!=-1 or diag2.find('Bk')!=-1:
                    self.black_is_in_check = True
                    return
            if prev_move_symbol in ['R', 'Q']:
                rank = self.board.get_rank_without_empty_squares(black_king_position[0])
                if rank.find('kQ')!=-1 or rank.find('Qk')!=-1:
                    self.black_is_in_check = True
                    return
                if rank.find('Rk')!=-1 or rank.find('kR')!=-1:
                    self.black_is_in_check = True
                    return
                file = self.board.get_file_without_empty_squares(black_king_position[0])
                if file.find('kQ')!=-1 or file.find('Qk')!=-1:
                    self.black_is_in_check = True
                    return
                if file.find('Rk')!=-1 or file.find('kR')!=-1:
                    self.black_is_in_check = True
                    return
            
            self.black_is_in_check = False
            return    # Black king not in check
        else: #Check if white king is now in check
            self.black_is_in_check = False  # Black not in check
            # Revealed checks
                #
                #   MUST CONSIDER EN PASSANT DISCOVERED CHECK IN REVEALED SECTIONS
                #    AND DISCOVERED CASTLING CHECKS and pawn promo?
                #
            row, column = prev_move[0], prev_move[1]    # Row and column of initial position of previous move
            white_king_position = self.board.white_king_position
            if white_king_position[0]==row:    # If prev move initially shared a rank with white king
                rank = self.board.get_rank_without_empty_squares(row)
                if rank.find('Kq')!=-1 or rank.find('qK')!=-1:
                    self.white_is_in_check = True
                    return
                if rank.find('rK')!=-1 or rank.find('Kr')!=-1:
                    self.white_is_in_check = True
                    return
            if white_king_position[1]==column:  # If prev move initially shared a file with white king
                file = self.board.get_file_without_empty_squares(column)
                if file.find('Kq')!=-1 or file.find('qK')!=-1:
                    self.white_is_in_check = True
                    return
                if file.find('rK')!=-1 or file.find('Kr')!=-1:
                    self.white_is_in_check = True
                    return
            if abs(white_king_position[0]-row)==abs(white_king_position[1]-column): # If prev move initially shared a diagonal with white king
                diagonals = self.board.get_diagonals_without_empty_squares(white_king_position[0], white_king_position[1]) # Get strings of symbols in both diagonals 
                diag1 = diagonals[0]
                diag2 = diagonals[1]
                if diag1.find('Kq')!=-1 or diag1.find('Kb')!=-1:
                    self.white_is_in_check = True
                    return
                if diag1.find('qK')!=-1 or diag1.find('bK')!=-1:
                    self.white_is_in_check = True
                    return
                if diag2.find('Kq')!=-1 or diag2.find('Kb')!=-1:
                    self.white_is_in_check = True
                    return
                if diag2.find('qK')!=-1 or diag2.find('bK')!=-1:
                    self.white_is_in_check = True
                    return
            # Prev move directly checks the white king
            if prev_move_symbol == 'n':
                # Knight check
                if (abs(white_king_position[0]-prev_move[2])==2 and abs(white_king_position[1]-prev_move[3])==1) or (abs(white_king_position[0]-prev_move[2])==1 and abs(white_king_position[1]-prev_move[3])==2):
                    self.white_is_in_check = True
                    return
                else:
                    self.white_is_in_check = False
                    return
            if prev_move_symbol == 'p':   
                if white_king_position[0]==(prev_move[2]-1) and abs(white_king_position[1]-prev_move[3])==1:    # Column difference of 1 and white king pos row 1 more than pawn row
                    self.white_is_in_check = True
                    return
                else:
                    self.white_is_in_check = False
                    return
            if prev_move_symbol in ['b', 'q']:
                diagonals = self.board.get_diagonals_without_empty_squares(white_king_position[0], white_king_position[1])  # Get both diagonals strings
                diag1 = diagonals[0]
                diag2 = diagonals[1]
                if diag1.find('Kq')!=-1 or diag1.find('Kb')!=-1:
                    self.white_is_in_check = True
                    return
                if diag1.find('qK')!=-1 or diag1.find('bK')!=-1:
                    self.white_is_in_check = True
                    return
                if diag2.find('Kq')!=-1 or diag2.find('Kb')!=-1:
                    self.white_is_in_check = True
                    return
                if diag2.find('qK')!=-1 or diag2.find('bK')!=-1:
                    self.white_is_in_check = True
                    return
            if prev_move_symbol in ['r', 'q']:
                rank = self.board.get_rank_without_empty_squares(white_king_position[0])
                if rank.find('Kq')!=-1 or rank.find('qK')!=-1:
                    self.white_is_in_check = True
                    return
                if rank.find('rK')!=-1 or rank.find('Kr')!=-1:
                    self.white_is_in_check = True
                    return
                file = self.board.get_file_without_empty_squares(white_king_position[0])
                if file.find('Kq')!=-1 or file.find('qK')!=-1:
                    self.white_is_in_check = True
                    return
                if file.find('rK')!=-1 or file.find('Kr')!=-1:
                    self.white_is_in_check = True
                    return
            
            self.white_is_in_check = False
            return   # White king not in check

    def legal_moves(self):
        cdef int i, j, up, down, right, left, up_right, up_left , down_right, down_left
        moves = []  # Store legal moves here
        # White's move (loop thorugh board to find white pieces)
        if self.white_turn:
            for i in range(8):
                for j in range(8):
                # Piece must be white
                    if self.board.pieces[i][j].isupper():                        
                        # Pawn
                        if self.board.pieces[i][j] == 'P':
                            if i<7 and self.board.pieces[i+1][j]=='.':
                                moves.append([i,j,i+1,j])   # Move one SQUARE forward
                            if i == 1 and self.board.pieces[2][j]=='.' and self.board.pieces[3][j]=='.':
                                moves.append([i,j,i+2,j])   # Move two squares forward on
                            if i<7 and j<7 and (self.board.pieces[i+1][j+1]!= '.' and not self.board.pieces[i+1][j+1].isupper()):
                                moves.append([i,j,i+1,j+1]) # Capture piece
                            if i<7 and j>0 and (self.board.pieces[i+1][j-1]!= '.' and not self.board.pieces[i+1][j-1].isupper()):
                                moves.append([i,j,i+1,j-1]) # Capture piece
                        
                        # Knight
                        elif self.board.pieces[i][j] == 'N':
                            if i>0 and j>1 and ((self.board.pieces[i-1][j-2]=='.') or (not self.board.pieces[i-1][j-2].isupper())):
                                moves.append([i,j,i-1,j-2])
                            if i>0 and j<6 and ((self.board.pieces[i-1][j+2]=='.') or (not self.board.pieces[i-1][j+2].isupper())):
                                moves.append([i,j,i-1,j+2])
                            if i>1 and j<7 and ((self.board.pieces[i-2][j+1]=='.') or (not self.board.pieces[i-2][j+1].isupper())):
                                moves.append([i,j,i-2,j+1])
                            if i>1 and j>0 and ((self.board.pieces[i-2][j-1]=='.') or (not self.board.pieces[i-2][j-1].isupper())):
                                moves.append([i,j,i-2,j-1])
                            if i<7 and j>1 and ((self.board.pieces[i+1][j-2]=='.') or (not self.board.pieces[i+1][j-2].isupper())):
                                moves.append([i,j,i+1,j-2])
                            if i<7 and j<6 and ((self.board.pieces[i+1][j+2]=='.') or (not self.board.pieces[i+1][j+2].isupper())):
                                moves.append([i,j,i+1,j+2])
                            if i<6 and j<7 and ((self.board.pieces[i+2][j+1]=='.') or (not self.board.pieces[i+2][j+1].isupper())):
                                moves.append([i,j,i+2,j+1])
                            if i<6 and j>0 and ((self.board.pieces[i+2][j-1]=='.') or (not self.board.pieces[i+2][j-1].isupper())):
                                moves.append([i,j,i+2,j-1])


                        # King
                        elif self.board.pieces[i][j] == 'K':
                            if i>0 and ((self.board.pieces[i-1][j]=='.') or (not self.board.pieces[i-1][j].isupper())):
                                moves.append([i,j,i-1,j])
                            if i>0 and j>0 and ((self.board.pieces[i-1][j-1]=='.') or (not self.board.pieces[i-1][j-1].isupper())):
                                moves.append([i,j,i-1,j-1])
                            if i>0 and j<7 and ((self.board.pieces[i-1][j+1]=='.') or (not self.board.pieces[i-1][j+1].isupper())):
                                moves.append([i,j,i-1,j+1])
                            if i<7 and ((self.board.pieces[i+1][j]=='.') or (not self.board.pieces[i+1][j].isupper())):
                                moves.append([i,j,i+1,j])
                            if i<7 and j>0 and ((self.board.pieces[i+1][j-1]=='.') or (not self.board.pieces[i+1][j-1].isupper())):
                                moves.append([i,j,i+1,j-1])
                            if i<7 and j<7 and ((self.board.pieces[i+1][j+1]=='.') or (not self.board.pieces[i+1][j+1].isupper())):
                                moves.append([i,j,i+1,j+1])
                            if j>0 and ((self.board.pieces[i][j-1]=='.') or (not self.board.pieces[i][j-1].isupper())):
                                moves.append([i,j,i,j-1])
                            if j<7 and ((self.board.pieces[i][j+1]=='.') or (not self.board.pieces[i][j+1].isupper())):
                                moves.append([i,j,i,j+1])
                            

                        # Vertical and horizontal moves by rooks and queens
                        elif self.board.pieces[i][j] in ['R','Q']:
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
                        if self.board.pieces[i][j] in ['B','Q']:
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
                    if self.board.pieces[i][j]!= '.' and not self.board.pieces[i][j].isupper():                        
                        # Pawn
                        if self.board.pieces[i][j] == 'p':
                            if i>0 and self.board.pieces[i-1][j]=='.':
                                moves.append([i,j,i-1,j])   # Move one SQUARE forward
                            if i == 6 and self.board.pieces[5][j]=='.' and self.board.pieces[4][j]=='.':
                                moves.append([i,j,4,j])   # Move two squares forward on
                            if i>0 and j<7 and (self.board.pieces[i-1][j+1]!= '.' and self.board.pieces[i-1][j+1].isupper()):
                                moves.append([i,j,i-1,j+1]) # Capture piece
                            if i>0 and j>0 and (self.board.pieces[i-1][j-1]!= '.' and self.board.pieces[i-1][j-1].isupper()):
                                moves.append([i,j,i-1,j-1]) # Capture piece
                        
                        # Knight
                        elif self.board.pieces[i][j] == 'n':
                            if i>0 and j>1 and ((self.board.pieces[i-1][j-2]=='.') or (self.board.pieces[i-1][j-2].isupper())):
                                moves.append([i,j,i-1,j-2])
                            if i>0 and j<6 and ((self.board.pieces[i-1][j+2]=='.') or (self.board.pieces[i-1][j+2].isupper())):
                                moves.append([i,j,i-1,j+2])
                            if i>1 and j<7 and ((self.board.pieces[i-2][j+1]=='.') or (self.board.pieces[i-2][j+1].isupper())):
                                moves.append([i,j,i-2,j+1])
                            if i>1 and j>0 and ((self.board.pieces[i-2][j-1]=='.') or (self.board.pieces[i-2][j-1].isupper())):
                                moves.append([i,j,i-2,j-1])
                            if i<7 and j>1 and ((self.board.pieces[i+1][j-2]=='.') or (self.board.pieces[i+1][j-2].isupper())):
                                moves.append([i,j,i+1,j-2])
                            if i<7 and j<6 and ((self.board.pieces[i+1][j+2]=='.') or (self.board.pieces[i+1][j+2].isupper())):
                                moves.append([i,j,i+1,j+2])
                            if i<6 and j<7 and ((self.board.pieces[i+2][j+1]=='.') or (self.board.pieces[i+2][j+1].isupper())):
                                moves.append([i,j,i+2,j+1])
                            if i<6 and j>0 and ((self.board.pieces[i+2][j-1]=='.') or (self.board.pieces[i+2][j-1].isupper())):
                                moves.append([i,j,i+2,j-1])


                        # King
                        elif self.board.pieces[i][j] == 'k':
                            if i>0 and ((self.board.pieces[i-1][j]=='.') or (self.board.pieces[i-1][j].isupper())):
                                moves.append([i,j,i-1,j])
                            if i>0 and j>0 and ((self.board.pieces[i-1][j-1]=='.') or (self.board.pieces[i-1][j-1].isupper())):
                                moves.append([i,j,i-1,j-1])
                            if i>0 and j<7 and ((self.board.pieces[i-1][j+1]=='.') or (self.board.pieces[i-1][j+1].isupper())):
                                moves.append([i,j,i-1,j+1])
                            if i<7 and ((self.board.pieces[i+1][j]=='.') or (self.board.pieces[i+1][j].isupper())):
                                moves.append([i,j,i+1,j])
                            if i<7 and j>0 and ((self.board.pieces[i+1][j-1]=='.') or (self.board.pieces[i+1][j-1].isupper())):
                                moves.append([i,j,i+1,j-1])
                            if i<7 and j<7 and ((self.board.pieces[i+1][j+1]=='.') or (self.board.pieces[i+1][j+1].isupper())):
                                moves.append([i,j,i+1,j+1])
                            if j>0 and ((self.board.pieces[i][j-1]=='.') or (self.board.pieces[i][j-1].isupper())):
                                moves.append([i,j,i,j-1])
                            if j<7 and ((self.board.pieces[i][j+1]=='.') or (self.board.pieces[i][j+1].isupper())):
                                moves.append([i,j,i,j+1])
                            

                        # Vertical and horizontal moves by rooks and queens
                        elif self.board.pieces[i][j] in ['r','q']:
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
                        if self.board.pieces[i][j] in ['b','q']:
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
        if abs(prev_move[2]-prev_move[0])==2 and self.board.pieces[prev_move[2]][prev_move[3]] in ['p','P']: # If previous move was made by a pawn moving 2 squares forward
            if self.white_turn:
                # Must have a white pawn at [4, i+-1] if prev move [6,i,4,i]
                if prev_move[1]>0 and self.board.pieces[4][prev_move[1]-1]!='.' and self.board.pieces[4][prev_move[1]-1]=='P':
                    moves.append([4,prev_move[1]-1,5,prev_move[1]])
                if prev_move[1]<7 and self.board.pieces[4][prev_move[1]+1]!='.' and self.board.pieces[4][prev_move[1]+1]=='P':
                    moves.append([4,prev_move[1]+1,5,prev_move[1]])
            # Black captures with en passant
            else:
                # Must have a black pawn at [3, i+-1] if prev move [1,i,3,i]
                if prev_move[1]>0 and self.board.pieces[3][prev_move[1]-1]!='.' and self.board.pieces[3][prev_move[1]-1]=='p':
                    moves.append([3,prev_move[1]-1,2,prev_move[1]])
                if prev_move[1]<7 and self.board.pieces[3][prev_move[1]+1]!='.' and self.board.pieces[3][prev_move[1]+1]=='p':
                    moves.append([3,prev_move[1]+1,2,prev_move[1]])
            
        # Castling
        if self.white_turn and not self.white_is_in_check and self.white_king_can_castle:
            rank0 = self.board.get_rank(0)  # If white king can castle we know the white king is at [0][3]
            if rank0.find('R..K')!=-1 and not self.board.king_side_castle_blocked(self.white_turn):
                moves.append([0,3,0,1])
            if rank0.find('K...R')!=-1 and not self.board.queen_side_castle_blocked(self.white_turn):
                moves.append([0,3,0,5])
        if (not self.white_turn) and (not self.black_is_in_check) and self.black_king_can_castle:
            rank7 = self.board.get_rank(7)  # If black king can castle we know the black king is at [7][3]
            if rank7.find('r..k')!=-1 and not self.board.king_side_castle_blocked(self.white_turn):
                moves.append([7,3,7,1])
            if rank7.find('k...r')!=-1 and not self.board.queen_side_castle_blocked(self.white_turn):
                moves.append([7,3,7,5])
        
        # Make sure each move does not leave self in check
        valid_moves = []    # If move does not leave self in check add it here
        direct_threats = self.board.create_bitboard_direct_threats_to_king(king_colour_is_white = self.white_turn) # Create Bit board of threats to our king
        # direct_threats.print()
        shields_to_our_king = self.board.create_bitboard_shields_to_king(self.white_turn)   # Create bit board of shields to our king
        # shields_to_our_king.print()
        # Loop through candidate legal moves
        if self.white_turn:
            for move in moves:              
                # If move is king move and king not in check must move to safe square
                if self.board.pieces[move[0]][move[1]]=='K':
                    if direct_threats.bits[move[2]][move[3]]==1:    # Invalid move
                        continue
                    if direct_threats.bits[move[0]][move[1]]==0 and direct_threats.bits[move[2]][move[3]]==0:    # Valid move when king not in check moves to safe square
                        valid_moves.append(move)
                        continue
                # If moving piece is not a shield to our king and king is not on a threatened square
                if shields_to_our_king.bits[move[0]][move[1]]==0 and direct_threats.bits[self.board.white_king_position[0]][self.board.white_king_position[1]]==0:
                    valid_moves.append(move)
                    continue

                # For other moves make the move on a copy board and see if the king is in check
                copy_game = copy.deepcopy(self)
                copy_game.board.make_move(move[0],move[1],move[2],move[3])  # Make move on copy board
                if not copy_game.board.white_king_is_in_check():
                    valid_moves.append(move)
        else:   # Black's turn
            for move in moves:
                # If move is king move must move to safe square
                if self.board.pieces[move[0]][move[1]]=='k':
                    if direct_threats.bits[move[2]][move[3]]==1:    # Invalid move
                        continue
                    if direct_threats.bits[move[0]][move[1]]==0 and direct_threats.bits[move[2]][move[3]]==0:    # Valid move (not check to not check)
                        valid_moves.append(move)
                        continue
                # If moving piece is not a shield to our king and king is not on a threatened square
                if shields_to_our_king.bits[move[0]][move[1]]==0 and direct_threats.bits[self.board.black_king_position[0]][self.board.black_king_position[1]]==0:
                    valid_moves.append(move)
                    continue
                # For other moves make the move and see if the king is in check
                copy_game = copy.deepcopy(self)
                copy_game.board.make_move(move[0],move[1],move[2],move[3])  # Make move on copy board
                if not copy_game.board.black_king_is_in_check():
                    valid_moves.append(move)

        return valid_moves

    def handle_new_successfully_made_move(self, move):
    # If a new move has been made update check and current_legal_moves and check for gameover etc...
        if not self.out_of_book:    # Update book if we are not already out of book
            self.update_book(move)
        self.selected_SQUARE = None     # Unselect SQUARE
        self.white_turn = not self.white_turn   # Flip turn
        self.previous_move = copy.copy(move)  # Update previous move
        board_string = self.board.board_to_string()  # Add to board states for 3fold repetition rule
        self.move_number += 1       # Update move number
        self.update_castlability()      # If a king move was made change castability to false
        # Update check (if you were in check you aren't anymore)
        if self.black_is_in_check:
            self.black_is_in_check = False
        if self.white_is_in_check:
            self.white_is_in_check = False
        self.is_check() # Check if the board is in check and update whether or not white/black is in check

        self.current_legal_moves = self.legal_moves()   # Calculate new legal moves
        if self.board.reset_board_strings:  # Reset board strings when old positions are no longer possible (when a pawn moves forward)
            self.board_states = {}  # Empty dictionary
            self.board.reset_board_strings = False
        if board_string in self.board_states.keys():    # Add new board to board states
            self.board_states[board_string] +=1
        else:
            self.board_states[board_string] = 1

        # If no legal moves check for check mate and stalemate
        if len(self.current_legal_moves) == 0:
            # Check for checkmate
            if self.is_checkmate():
                self.checkmate = True
                self.gameover = True
                if self.white_turn:
                    self.black_won = True
                else:
                    self.white_won = True
                #print('checkmate')

             # Check for stalemate
            if self.is_stalemate():
                self.gameIsDraw = True
                self.gameover = True
                self.stalemate = True
                #print('draw by stalemate')

        # Draw by threefold repetition
        if self.is_draw_by_threefold_repetition():
            self.gameIsDraw = True
            self.gameover = True
            #print('draw by threefold repetition')

        # Draw by lack of material
        if self.board.is_draw_by_lack_of_material():
            self.gameIsDraw = True
            self.gameover = True
            #print('draw by lack of material')

          
    def update_castlability(self):
        # If a king move was made change castlability to false
        prev_move = self.previous_move
        if self.board.pieces[prev_move[2]][prev_move[3]]=='k':
            self.black_king_can_castle = False
        elif self.board.pieces[prev_move[2]][prev_move[3]]=='K':
            self.white_king_can_castle = False
    
    def evaluate_position_score(self):
        """Returns score to evaluate current position"""

        # If checkmate return +- infinity only check for this if it is check
        if self.gameover:
            if self.black_won:
                return -10000
            if self.white_won:
                return 10000
            if self.gameIsDraw:     
                return 0



        # If forced checkmate return +- 100000
        # if self.is_forced_checkmate():
            
        
        # Direct threats bitboards
        direct_threats_to_white_bitboard = self.board.create_bitboard_direct_threats_to_king(True)
        direct_threats_to_black_bitboard = self.board.create_bitboard_direct_threats_to_king(False)

        # For every capturing move check if the capture is unprotected
        unprotected_capturable_value = 0
        capture_squares = []    # Squares on which captures (not necessarily unprotected captures) can occur
        for move in self.current_legal_moves:
            if self.board.pieces[move[2]][move[3]]!='.' and [move[2],move[3]] not in capture_squares:    # if moves onto a piece (capturing move)
                capture_squares.append([move[2],move[3]])
                if self.white_turn: # White making the capture
                    if direct_threats_to_white_bitboard.bits[move[2]][move[3]]==0:  # Not seen by black (not recapturable)
                        unprotected_capturable_value -= self.board.char_to_value(self.board.pieces[move[2]][move[3]])
                else:   # Black making the capture
                    if direct_threats_to_black_bitboard.bits[move[2]][move[3]]==0:  # Not seen by white (not recapturable)
                        unprotected_capturable_value -= self.board.char_to_value(self.board.pieces[move[2]][move[3]])
                    
        self.board.scores.capturable_unprotected = 0.8*unprotected_capturable_value # Update unprotected capturables value 


        # Update control of board score
        self.board.scores.control_of_board = (direct_threats_to_black_bitboard.number_of_ones()-direct_threats_to_white_bitboard.number_of_ones())*0.01

         # Initialise score to stored board scores total
        score = self.board.scores.get_total()

        # Add temporary bonus for castling to encourage castling

        # Add value for capturable piece where taker value less than taken value
        max_capture = 0
        max_capture_move = None
        for move in self.current_legal_moves:
            try:
                if abs(self.board.char_to_value(self.board.pieces[move[2]][move[3]]))>1:    # Find capturing moves on pieces (not pawns)
                    capture_value = abs(self.board.char_to_value(self.board.pieces[move[2]][move[3]]))-abs(self.board.char_to_value(self.board.pieces[move[0]][move[1]]))
                    if capture_value>max_capture:
                        max_capture = copy.copy(capture_value)
                        max_capture_move = copy.copy(move)
            except:
                pass
        if max_capture_move !=None:
            if self.white_turn:
                # If recapturable
                if direct_threats_to_white_bitboard.bits[max_capture_move[2]][max_capture_move[3]]==1:
                    score += max_capture*0.8
                else: # Not recapturable
                    score+= max_capture*0.2
            else:   # Black's move
                # If recapturable
                if direct_threats_to_black_bitboard.bits[max_capture_move[2]][max_capture_move[3]]==1:
                    score -= max_capture*0.8
                else: # Not recapturable
                    score-= max_capture*0.2


        # Rook on open file (SPILT INTO SEMI OPEN FILE AND FILE use pawn counts in this logic for efficiency)
        rook_on_open_file = 0
        for i in range(8):
            file = self.board.get_file(i)
            if file.find("r...")!=-1:
                rook_on_open_file -= 0.07
            if file.find("...r")!=-1:
                rook_on_open_file -= 0.07
            if file.find("R...")!=-1:
                rook_on_open_file += 0.07
            if file.find("...R")!=-1:
                rook_on_open_file += 0.07
        self.board.scores.rook_on_open_file = rook_on_open_file
        

        # End game
        if self.move_number > 40:
            self.board.scores.reset_castling_bonus()    # Reset castling bonus to 0
            pieces_string = self.board.get_pieces_string()  # Calculate what pieces we have left
            # KPk end game
            if pieces_string == "KPk":
                KPk_score = KPk(self.board, self.white_turn)
                if KPk_score != "unknown":
                    return KPk_score
            elif pieces_string == "Kkp":
                Kkp_score = Kkp(self.board, self.white_turn)
                if Kkp_score != "unknown":
                    return Kkp_score
            elif pieces_string == "KRk":
                return white_rook_endgame(self)
            elif pieces_string == "Kkr":
                return black_rook_endgame(self)

        # Return score after adjustments
        return score

    def maximise_move_score_depth_1(self):
        # Returns best move depth 1 (looking 1 move ahead)
        cdef double score
        if self.white_turn:
            best_move = None
            best_score = -10000
            for move in self.current_legal_moves:
                copy_game = copy.deepcopy(self)     # on copy board
                copy_game.board.make_move(move[0],move[1],move[2],move[3])  # Make move on copy board
                copy_game.handle_new_successfully_made_move(move)   # Update castlability etc
                score = copy_game.evaluate_position_score()
                if score > best_score:
                    best_score = copy.copy(score)
                    best_move = copy.copy(move)
            return best_move
        else:   # Blacks turn 
            best_move = None
            best_score = 10000
            for move in self.current_legal_moves:
                copy_game = copy.deepcopy(self)     # on copy board
                copy_game.board.make_move(move[0],move[1],move[2],move[3])  # Make move on copy board
                copy_game.handle_new_successfully_made_move(move)   # Update castlability etc
                score = copy_game.evaluate_position_score()
                if score < best_score:
                    best_score = copy.copy(score)
                    best_move = copy.copy(move)
            return best_move

    def maximise_move_score(self):
        # Returns best move (depth 2) for white and black
        if self.white_turn: # If white calculate max min (USE ALPHA BETA PRUNING)
            try:
                best_move = self.current_legal_moves[0] # Initialise best move to the first legal move
            except:
                return
            likely_replies = [] # Candidate good moves for black
            best_score = -1000000   # Compute best score of best move 
            for move in self.current_legal_moves:   # Try every legal white move
                copy_game = copy.deepcopy(self)     # on copy board
                copy_game.board.make_move(move[0],move[1],move[2],move[3])  # Make move on copy board
                copy_game.handle_new_successfully_made_move(move)   # Update castlability etc
                # Now it is Blacks turn... make all legal black moves
                min_score = 100000  # Make the best black move (min score move)
                for likely_reply in likely_replies:
                    if likely_reply in copy_game.current_legal_moves:  # Remove and insert likely_reply at front of list
                        copy_game.current_legal_moves.remove(copy.copy(likely_reply))  
                        copy_game.current_legal_moves.insert(0,copy.copy(likely_reply))
                best_reply = None  # Used to add new good replies for black

                # If no legal moves in response to move it is game over in this line 
                if len(copy_game.current_legal_moves) == 0:
                    score = copy_game.evaluate_position_score()
                    if score > best_score:
                        best_score = copy.copy(score)
                        best_move = copy.copy(move)

                # Try every response to move
                for move2 in copy_game.current_legal_moves: 
                    copy_copy_game = copy.deepcopy(copy_game)    # on copycopy board
                    copy_copy_game.board.make_move(move2[0],move2[1],move2[2],move2[3])  # Make move on copycopy board
                    copy_copy_game.handle_new_successfully_made_move(move2)   # Update castlability etc
                    score = copy_copy_game.evaluate_position_score()    # Evaluate score
                    # We wish to minimise this score
                    if min_score > score:
                        min_score = copy.copy(score)
                        best_reply = copy.copy(move2)  # Update best reply
                    if move!=best_move and score < best_score:  # ALPHA BETA PRUNING
                        break
                if best_reply!=None and best_reply not in likely_replies:    # Add best reply to likely replies
                    likely_replies.append(best_reply)
                if min_score>best_score:    # maximise these min scores
                    best_score = copy.deepcopy(min_score)
                    best_move = copy.deepcopy(move)
                if min_score == best_score:
                    x = random.randint(1,4) # For sake of variety
                    if x==3:    
                        best_score = copy.deepcopy(min_score)
                        best_move = copy.deepcopy(move)
            return best_move
        else:       # Black's turn calculate min max
            try:
                best_move = self.current_legal_moves[0] # Initialise best move to the first legal move
            except:
                pass
            likely_replies = []  # Candidate good moves for white
            best_score = 1000000        # minimise score for black
            for move in self.current_legal_moves:   # Try every legal black move
                copy_game = copy.deepcopy(self)     # on copy board
                copy_game.board.make_move(move[0],move[1],move[2],move[3])  # Make move on copy board
                copy_game.handle_new_successfully_made_move(move)   # Update castlability etc
                for likely_reply in likely_replies:
                    if likely_reply in copy_game.current_legal_moves:  # If likely reply is legal move Remove and insert likely_reply at front of list
                        copy_game.current_legal_moves.remove(copy.copy(likely_reply))  
                        copy_game.current_legal_moves.insert(0,copy.copy(likely_reply))
                # Now it is White's turn... make all legal black moves
                max_score = -100000  # Make the best white move (max score move)
                best_reply = None  # Used to add new good replies for white
                
                # If no legal moves in response to move it is game over in this line 
                if len(copy_game.current_legal_moves) == 0:
                    score = copy_game.evaluate_position_score()
                    if score < best_score:
                        best_score = copy.copy(score)
                        best_move = copy.copy(move)

                # Try every response to move
                for move2 in copy_game.current_legal_moves: 
                    copy_copy_game = copy.deepcopy(copy_game)    # on copycopy board
                    copy_copy_game.board.make_move(move2[0],move2[1],move2[2],move2[3])  # Make move on copycopy board
                    copy_copy_game.handle_new_successfully_made_move(move2)   # Update castlability etc
                    score = copy_copy_game.evaluate_position_score()    # Evaluate score
                    # We wish to minimise this score
                    if max_score < score:
                        max_score = copy.copy(score)
                        best_reply = copy.copy(move2)
                    if move!=best_move and score > best_score:  # ALPHA BETA PRUNING
                        break
                if best_reply!=None and best_reply not in likely_replies:    # Add best reply to likely replies
                    likely_replies.append(best_reply)
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
        if not self.out_of_book:    # If not out of book make book move and update book
            move_string = self.book.choose_book_move(self.move_number)
            self.book.update_book(move_string,self.move_number) # Update book
            if len(self.book.book_moves)==0:
                self.out_of_book = True
            if move_string !='':
                return self.move_string_to_move(move_string)
            else:
                self.out_of_book = True
                
        if depth == 1:
            return self.maximise_move_score()

        elif depth>1:
            if self.white_turn:         # White turn
                max_score = -10000000
                move_decision = None    #move we return
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
                move_decision = None
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

    def move_string_to_move(self, move_string):
        # Return move from move string "(i,j,x,y)"
        i = int(move_string[1])
        j = int(move_string[3])
        x = int(move_string[5])
        y = int(move_string[7])

        return [i,j,x,y]

    def move_to_move_string(self, move):
        # Given move [i,j,x,y] return string "(i,j,x,y)"
        i = str(move[0])
        j = str(move[1])
        k = str(move[2])
        l = str(move[3])
        string ="("
        for x in [i,j,k]:
            string+=x
            string+=','
        string+= l
        string+= ")"

        return string

    def update_book(self, move):
        # Given a move update the book 
        self.book.update_book(self.move_to_move_string(move),self.move_number)
        if len(self.book.book_moves) == 0:
            self.out_of_book = True

    
    # Best move depth 1
    