from Pieces import *
from Board import *
import random

class Game():
    def __init__(self):
        self.white_king_can_castle = True
        self.black_king_can_castle = True
        self.white_turn = True
        self.gameover, self.checkmate, self.stalemate = False, False, False
        self.gameIsDraw, self.white_won, self.black_won = False, False, False
        self.board = Board()
        self.selected_SQUARE = None  # i,j or None
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
        self.selected_SQUARE = None     # Unselect SQUARE
        self.white_turn = not self.white_turn   # Flip turn
        self.previous_move = move  # Update previous move
        board_string = self.board.board_to_string()  # Add to board states for 3fold repetition rule
        self.move_number += 1       # Update move number
        if board_string in self.board_states.keys():    # Add new board to board states
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
        if self.board.pieces[prev_move[2]][prev_move[3]]== None: # Must not be an empty SQUARE
            return
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

        score = self.board.scores.get_total() # Initialise score to stored board scores total


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

        # Bonus points for kicking an opponents piece with a pawn
        for i in range(1,7):  # Ranks 1 to 6
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