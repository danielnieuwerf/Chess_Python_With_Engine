from Pieces import *
from Board import *
from Book import *
import random

class Game():
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
        self.board = Board()
        self.selected_SQUARE = None  # i,j or None
        self.previous_move = [7,0,7,0]     # Used in en passant logic
        self.current_legal_moves = self.legal_moves()    # A list of all legal moves
        self.board_states = {}     # A mapping from board strings to how many times such a string has occurred in the game
               
    def draw_window(self, surface):
        # Draw empty board
        WHITE = (238,238,210)
        DARK = (118,150,86)
        for i in range(0,8):
            for j in range(0,8):
                if (i+j) % 2 ==1:
                    pygame.draw.rect(surface, DARK, ((i*SQUARE, j*SQUARE), (SQUARE,SQUARE))) # dark squares
                else:
                    pygame.draw.rect(surface, WHITE, ((i*SQUARE, j*SQUARE), (SQUARE,SQUARE))) # light squares
        
        # Highlight selected SQUARE
        if self.selected_SQUARE!= None:
            i,j = self.selected_SQUARE
            if (i+j)%2 ==1:
                pygame.draw.rect(surface, (100,100,100), ((j*SQUARE, i*SQUARE), (SQUARE,SQUARE)))
            else:
                pygame.draw.rect(surface, (150,150,150), ((j*SQUARE, i*SQUARE), (SQUARE,SQUARE)))

        # Draw pieces on board
        for i in range(8):
            for j in range(8):
                try:
                    surface.blit(self.board.pieces[i][j].image, (j*SQUARE, i*SQUARE))
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
        prev_move_was_white = self.board.pieces[prev_move[2]][prev_move[3]].white   # True if previous move was white piece
        prev_move_symbol = self.board.pieces[prev_move[2]][prev_move[3]].symbol     # Symbol of previous move piece e.g 'k' for black king
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
                                moves.append([i,j,i+1,j])   # Move one SQUARE forward
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
                                moves.append([i,j,i-1,j])   # Move one SQUARE forward
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
        if abs(prev_move[2]-prev_move[0])==2 and abs(self.board.pieces[prev_move[2]][prev_move[3]].value)== 1: # If previous move was made by a pawn moving 2 squares forward
            if self.white_turn:
                # Must have a white pawn at [4, i+-1] if prev move [6,i,4,i]
                if prev_move[1]>0 and self.board.pieces[4][prev_move[1]-1]!=None and self.board.pieces[4][prev_move[1]-1].symbol=='P':
                    moves.append([4,prev_move[1]-1,5,prev_move[1]])
                if prev_move[1]<7 and self.board.pieces[4][prev_move[1]+1]!=None and self.board.pieces[4][prev_move[1]+1].symbol=='P':
                    moves.append([4,prev_move[1]+1,5,prev_move[1]])
            # Black captures with en passant
            else:
                # Must have a black pawn at [3, i+-1] if prev move [1,i,3,i]
                if prev_move[1]>0 and self.board.pieces[3][prev_move[1]-1]!=None and self.board.pieces[3][prev_move[1]-1].symbol=='p':
                    moves.append([3,prev_move[1]-1,2,prev_move[1]])
                if prev_move[1]<7 and self.board.pieces[3][prev_move[1]+1]!=None and self.board.pieces[3][prev_move[1]+1].symbol=='p':
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
        
        # Make the move on a copy board if it's invalid do not add it to valid_moves
        valid_moves = []
        if self.white_turn:
            for move in moves:
                copy_game = copy.deepcopy(self)
                copy_game.board.make_move(move[0],move[1],move[2],move[3])  # Make move on copy board
                if not copy_game.board.white_king_is_in_check():
                    valid_moves.append(move)
        else:   # Black's turn
            for move in moves:
                copy_game = copy.deepcopy(self)
                copy_game.board.make_move(move[0],move[1],move[2],move[3])  # Make move on copy board
                if not copy_game.board.black_king_is_in_check():
                    valid_moves.append(move)

        return valid_moves

    def handle_new_successfully_made_move(self, move):
    # If a new move has been made update check and current_legal_moves and check for gameover etc...
        if not self.out_of_book:    # Update book
            self.update_book(move)
        self.selected_SQUARE = None     # Unselect SQUARE
        self.white_turn = not self.white_turn   # Flip turn
        self.previous_move = move  # Update previous move
        board_string = self.board.board_to_string()  # Add to board states for 3fold repetition rule
        self.move_number += 1       # Update move number
        self.update_castlability()      # If a king move was made change castability to false
        # Update check (if you were in check you aren't anymore)
        if self.black_is_in_check:
            self.black_is_in_check = False
        if self.white_is_in_check:
            self.white_is_in_check = False
        self.update_check_status()     
        self.current_legal_moves = self.legal_moves()   # Calculate new legal moves
        if self.board.reset_board_strings:  # Reset board strings when old positions are no longer possible
            self.board_states = {}
            self.board.reset_board_strings = False
        if board_string in self.board_states.keys():    # Add new board to board states
            self.board_states[board_string] +=1
        else:
            self.board_states[board_string] = 1

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
        if self.board.pieces[prev_move[2]][prev_move[3]].symbol=='k':
            self.black_king_can_castle = False
        elif self.board.pieces[prev_move[2]][prev_move[3]].symbol=='K':
            self.white_king_can_castle = False
    
    def evaluate_position_score(self):
        # Returns score to evaluate current position

        # If checkmate return +- infinity only check for this if it is check
        if self.black_won:
            return -1000000
        if self.white_won:
            return 10000000
        if self.gameIsDraw:     # If draw return 0
            return 0
        
        # For every capturing move check if the capture is unprotected
        unprotected_capturable_value = 0
        capture_squares = []    # Squares on which captures (not necessarily unprotected captures) can occur
        for move in self.current_legal_moves:
            if self.board.pieces[move[2]][move[3]]!=None and [move[2],move[3]] not in capture_squares:    # if moves onto a piece (capturing move)
                capture_squares.append([move[2],move[3]])
                copy_game = copy.deepcopy(self)     # on copy board
                copy_game.board.make_move(move[0],move[1],move[2],move[3])  # Make move on copy board
                copy_game.handle_new_successfully_made_move(move)   # Update castlability etc ( unnecessary things done in this function)
                recapturable = False
                for copy_move in copy_game.current_legal_moves:
                    if copy_move[2]== move[2] and copy_move[3]==move[3]:    # Recapturable
                        recapturable = True
                        break
                        
                if not recapturable:
                    unprotected_capturable_value -= self.board.pieces[move[2]][move[3]].value
        self.board.scores.capturable_unprotected = 0.8*unprotected_capturable_value # Update unprotected capturables value 
        
        score = self.board.scores.get_total() # Initialise score to stored board scores total

        # Bonus for mobility
        if self.white_turn:
            self.board.scores.num_legal_white_moves = len(self.current_legal_moves)
        else:
            self.board.scores.num_legal_black_moves = len(self.current_legal_moves)
        self.board.scores.update_mobility()

        # Add value for capturable piece where taker value less than taken value
        max_capture = 0
        for move in self.current_legal_moves:
            try:
                if abs(self.board.pieces[move[2]][move[3]].value)>1:    # Find capturing moves on pieces (not pawns)
                    capture_value = abs(self.board.pieces[move[2]][move[3]].value)-abs(self.board.pieces[move[0]][move[1]].value)
                    if capture_value>max_capture:
                        max_capture = copy.copy(capture_value)
            except:
                pass
        if self.white_turn:
            score += max_capture*0.7
        else:
            score -= max_capture*0.7

        # Number of developed pieces bonus
        rank_white = self.board.get_rank_without_empty_squares(0)
        rank_black = self.board.get_rank_without_empty_squares(7)
        white_undeveloped_count, black_undeveloped_count = 0,0  #number of undeveloped pieces
        for x in rank_black:
            if x in ['b','r','n','q']:
                black_undeveloped_count +=1
        for x in rank_white:
            if x in ['B','R','N','Q']:
                white_undeveloped_count +=1
        
        score += 0.02*black_undeveloped_count   # Apply bonuses
        score -= 0.02*white_undeveloped_count

        # Control of centre




        # End game
        if self.move_number > 30:
            # Ending with 3 pawns vs knight or bishop
            pass

        # Return score after adjustments
        return score

    def maximise_move_score(self):
        # Returns best move (depth 1) for white and black
        if self.white_turn: # If white calculate max min (USE ALPHA BETA PRUNING)
            best_move = self.current_legal_moves[0] # Initialise best move to the first legal move
            best_score = -1000000   # Compute best score of best move 
            for move in self.current_legal_moves:   # Try every legal white move
                copy_game = copy.deepcopy(self)     # on copy board
                copy_game.board.make_move(move[0],move[1],move[2],move[3])  # Make move on copy board
                copy_game.handle_new_successfully_made_move(move)   # Update castlability etc
                # Now it is Blacks turn... make all legal black moves
                min_score = 100000  # Make the best black move (min score move)
                for move2 in copy_game.current_legal_moves: 
                    copy_copy_game = copy.deepcopy(copy_game)    # on copycopy board
                    copy_copy_game.board.make_move(move2[0],move2[1],move2[2],move2[3])  # Make move on copycopy board
                    copy_copy_game.handle_new_successfully_made_move(move2)   # Update castlability etc
                    score = copy_copy_game.evaluate_position_score()    # Evaluate score
                    # We wish to minimise this score
                    if min_score > score:
                        min_score = copy.copy(score)
                    if move!=best_move and score < best_score:  # ALPHA BETA PRUNING
                        break
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
            best_move = self.current_legal_moves[0] # Initialise best move to the first legal move
            best_score = 1000000        # minimise score for black
            for move in self.current_legal_moves:   # Try every legal black move
                copy_game = copy.deepcopy(self)     # on copy board
                copy_game.board.make_move(move[0],move[1],move[2],move[3])  # Make move on copy board
                copy_game.handle_new_successfully_made_move(move)   # Update castlability etc
                # Now it is White's turn... make all legal black moves
                max_score = -100000  # Make the best white move (max score move)
                for move2 in copy_game.current_legal_moves: 
                    copy_copy_game = copy.deepcopy(copy_game)    # on copycopy board
                    copy_copy_game.board.make_move(move2[0],move2[1],move2[2],move2[3])  # Make move on copycopy board
                    copy_copy_game.handle_new_successfully_made_move(move2)   # Update castlability etc
                    score = copy_copy_game.evaluate_position_score()    # Evaluate score
                    # We wish to minimise this score
                    if max_score < score:
                        max_score = copy.copy(score)
                    if move!=best_move and score > best_score:  # ALPHA BETA PRUNING
                        break
                
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

    def move_string_to_move(self, move_string):
        # Return move from move string "(i,j,x,y)"
        i = int(move_string[1])
        j = int(move_string[3])
        x = int(move_string[5])
        y = int(move_string[7])

        return [i,j,x,y]

    def move_to_move_string(self, move):
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
        self.book.update_book(self.move_to_move_string(move),self.move_number)
        if len(self.book.book_moves) == 0:
            self.out_of_book = True