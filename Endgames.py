"""
    Given a board and whose turn it is, return the score evaluation of the endgame
    Or apply bonuses for moves that are good for different end games
"""

def KPk(board, turn):
    # Given a board, and whose turn it is for a white pawn and king vs king ending
    # Return the evaluation if it is known else return unknown
    if white_pawn_promo_cannot_be_stopped(board, turn):
        return 9.0
    if black_king_blocks_pawn_promo(board, turn):
        return 0
    return "unknown"

def Kkp(board, turn):
    # Given a board, and whose turn it is for a black pawn and king vs king ending
    # Return the evaluation if it is known else return unknown
    if black_pawn_promo_cannot_be_stopped(board, turn):
        return -9.0
    if white_king_blocks_pawn_promo(board, turn):
        return 0
    return "unknown"

def white_pawn_promo_cannot_be_stopped(board, turn):
    # Given a KPk board and whose turn it is return whether or not pawn promotion cannot be stopped

    # Calculate which square is promo square
    for i in range(8):
        if board.scores.white_pawns_count[i]==1:
            promo_file = i
            break

    # Calculate num moves for pawn to promote
    for i in range(2,7):
        if board.pieces[i][promo_file]=='P':
            num_moves_for_pawn_promo = 7 - i
            break
    if board.pieces[1][promo_file]=='P':
        num_moves_for_pawn_promo = 5    # Because can jump 2 squares on first move

    # Calculate min num moves for king to get to promo square
    num_king_moves = num_moves_for_king_to_reach_position(board.black_king_position, [7,promo_file])

    if turn:
        num_moves_for_pawn_promo -= 1
    else:
        num_king_moves -= 1

    # If king can catch pawn
    if num_king_moves-1 > num_moves_for_pawn_promo:
        return True
    return False

def black_pawn_promo_cannot_be_stopped(board, turn):
    # Given a Kkp board and whose turn it is, return whether or not pawn promotion cannot be stopped

    # Calculate which square is promo square
    for i in range(8):
        if board.scores.black_pawns_count[i]==1:
            promo_file = i
            break

    # Calculate num moves for pawn to promote
    for i in range(1,6):
        if board.pieces[i][promo_file]=='p':
            num_moves_for_pawn_promo = i
            break
    if board.pieces[6][promo_file]=='p':
        num_moves_for_pawn_promo = 5    # Because can jump 2 squares on first move

    # Calculate min num moves for king to get to promo square
    num_king_moves = num_moves_for_king_to_reach_position(board.white_king_position, [0,promo_file])

    if not turn:
        num_moves_for_pawn_promo -= 1
    else:
        num_king_moves -= 1

    # If king cannot catch pawn return true
    if num_king_moves-1 > num_moves_for_pawn_promo:
        return True
    return False

def num_moves_for_king_to_reach_position(king_pos, pos):
    # Given a king pos [x,y] return how many moves it will take to reach pos [i,j]
    vertical = abs(king_pos[0]-pos[0])
    horizontal = abs(king_pos[1]-pos[1])

    return max(vertical, horizontal)

def white_king_blocks_pawn_promo(board, turn):
    # Given a Kkp board and turn return whether or not white king blocks the pawn promo
    white_king_pos = board.white_king_position
    black_king_pos = board.black_king_position

    # Compute black pawn pos and promo pos
    for i in range(8):
        if board.scores.black_pawns_count[i]==1:
            black_pawn_file = i
            break
    for j in range(8):
        if board.pieces[j][black_pawn_file]=='p':
            black_pawn_pos = [j, black_pawn_file]
            break
    promo_pos = [0,black_pawn_pos[1]]

    if white_king_pos[0]+1 == black_pawn_pos[0] and white_king_pos[1]==black_pawn_pos[1]:   # If white king blocks pawn promo
        return True

    return False

def black_king_blocks_pawn_promo(board, turn):
    # Given a KPk board and turn return whether or not black king blocks the pawn promo
    white_king_pos = board.white_king_position
    black_king_pos = board.black_king_position

    # Compute white pawn pos and promo pos
    for i in range(8):
        if board.scores.white_pawns_count[i]==1:
            white_pawn_file = i
            break
    for j in range(8):
        if board.pieces[j][white_pawn_file]=='P':
            white_pawn_pos = [j, white_pawn_file]
            break
    promo_pos = [7,white_pawn_pos[1]]

    if black_king_pos[0]-1 == white_pawn_pos[0] and black_king_pos[1]==white_pawn_pos[1]:   # If white king blocks pawn promo
        return True

    return False

def white_rook_endgame(game):
    # Return score for white rook endgame 
    # Add value to score for cutting off the board with the white rook
    # Successfully checkmates but takes more moves than necessary.
    black_king_pos = game.board.black_king_position
    white_king_pos = game.board.white_king_position

    # If black turn and black king can take the white rook return 0
    if not game.white_turn:
        # If white rook is one square away from black king
        for i in [-1, 0, -1]:
            for j in [-1, 0, -1]:
                try:
                    if game.board.pieces[black_king_pos[0] + i][black_king_pos[1] + j] == 'R':   # If black king sees white rook
                        if max(abs(game.board.white_king_position[0] - (black_king_pos[0] + i)), abs(game.board.white_king_position[1] - (black_king_pos[1] + j)))!=1:    # If white king does not protect white rook
                            return 0
                except:
                    pass

    # If black's turn and black king in a corner check for stalemate
    if game.white_turn == False and black_king_pos[0] in [0,7] and black_king_pos[1] in [0,7]:
        # If we reach here in the function we know the rook cannot be captured
        if game.board.pieces[1][1] == 'R' and black_king_pos[0] == 0 and black_king_pos[1] == 0:
            return 0
        if game.board.pieces[1][6] == 'R' and black_king_pos[0] == 0 and black_king_pos[1] == 7:
            return 0
        if game.board.pieces[6][1] == 'R' and black_king_pos[0] == 7 and black_king_pos[1] == 0:
            return 0
        if game.board.pieces[6][6] == 'R' and black_king_pos[0] == 7 and black_king_pos[1] == 7:
            return 0

    # If checkmate return 10000
    if black_king_pos[0] in [0, 7]:
        if abs(white_king_pos[0]-black_king_pos[0]) == 2 and white_king_pos[1] == black_king_pos[1]:    
            # Since the rook cannot be captured by the king if it is in row black_king_pos[0] then it is checkmate
            for i in range(8):
                if game.board.pieces[black_king_pos[0]][i] == 'R':  # It is checkmate
                    return 10000

    if black_king_pos[1] in [0, 7]:
        if abs(white_king_pos[1]-black_king_pos[1]) == 2 and white_king_pos[0] == black_king_pos[0]:    
            # Since the rook cannot be captured by the king if it is in row black_king_pos[0] then it is checkmate
            for i in range(8):
                if game.board.pieces[i][black_king_pos[1]] == 'R':  # It is checkmate
                    return 10000

    # Score based on black king position
    scores = [
        [ 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0],
        [ 7.0, 6.5, 6.5, 6.5, 6.5, 6.5, 6.5, 7.0],
        [ 7.0, 6.5, 6.0, 6.0, 6.0, 6.0, 6.5, 7.0],
        [ 7.0, 6.5, 6.0, 5.5, 5.5, 6.0, 6.5, 7.0],
        [ 7.0, 6.5, 6.0, 5.5, 5.5, 6.0, 6.5, 7.0],
        [ 7.0, 6.5, 6.0, 6.0, 6.0, 6.0, 6.5, 7.0],
        [ 7.0, 6.5, 6.5, 6.5, 6.5, 6.5, 6.5, 7.0],
        [ 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0]     
        ]

    distance_between_kings = distance_between_two_kings(game.board)
    bonus_for_closeness_of_kings = (8-distance_between_kings)*0.3
    return scores[black_king_pos[0]][black_king_pos[1]] + bonus_for_closeness_of_kings

def black_rook_endgame(game):
    # Return score for black rook endgame 
    # Add value to score for cutting off the board with the black rook
    # Successfully checkmates but takes more moves than necessary.
    black_king_pos = game.board.black_king_position
    white_king_pos = game.board.white_king_position

    # If white turn and white king can take the black rook return 0
    if game.white_turn:
        # If black rook is one square away from white king
        for i in [-1, 0, -1]:
            for j in [-1, 0, -1]:
                try:
                    if game.board.pieces[white_king_pos[0] + i][white_king_pos[1] + j] == 'r':   # If white king sees black rook
                        if max(abs(black_king_pos[0] - (white_king_pos[0] + i)), abs(black_king_pos[1] - (white_king_pos[1] + j)))!=1:    # If black king does not protect white rook
                            return 0
                except:
                    pass

    # If white's turn and white king in a corner check for stalemate
    if game.white_turn and white_king_pos[0] in [0,7] and white_king_pos[1] in [0,7]:
        # If we reach here in the function we know the rook cannot be captured
        if game.board.pieces[1][1] == 'r' and white_king_pos[0] == 0 and white_king_pos[1] == 0:
            return 0
        if game.board.pieces[1][6] == 'r' and white_king_pos[0] == 0 and white_king_pos[1] == 7:
            return 0
        if game.board.pieces[6][1] == 'r' and white_king_pos[0] == 7 and white_king_pos[1] == 0:
            return 0
        if game.board.pieces[6][6] == 'r' and white_king_pos[0] == 7 and white_king_pos[1] == 7:
            return 0

    # If checkmate return -10000
    if white_king_pos[0] in [0, 7]:
        if abs(white_king_pos[0]-black_king_pos[0]) == 2 and white_king_pos[1] == black_king_pos[1]:    
            # Since the rook cannot be captured by the king if it is in row white_king_pos[0] then it is checkmate
            for i in range(8):
                if game.board.pieces[white_king_pos[0]][i] == 'r':  # It is checkmate
                    return -10000

    if white_king_pos[1] in [0, 7]:
        if abs(white_king_pos[1]-black_king_pos[1]) == 2 and white_king_pos[0] == black_king_pos[0]:    
            # Since the rook cannot be captured by the king if it is in row black_king_pos[0] then it is checkmate
            for i in range(8):
                if game.board.pieces[i][white_king_pos[1]] == 'r':  # It is checkmate
                    return -10000

    # Score based on black king position
    scores = [
        [ 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0],
        [ 7.0, 6.5, 6.5, 6.5, 6.5, 6.5, 6.5, 7.0],
        [ 7.0, 6.5, 6.0, 6.0, 6.0, 6.0, 6.5, 7.0],
        [ 7.0, 6.5, 6.0, 5.5, 5.5, 6.0, 6.5, 7.0],
        [ 7.0, 6.5, 6.0, 5.5, 5.5, 6.0, 6.5, 7.0],
        [ 7.0, 6.5, 6.0, 6.0, 6.0, 6.0, 6.5, 7.0],
        [ 7.0, 6.5, 6.5, 6.5, 6.5, 6.5, 6.5, 7.0],
        [ 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0]     
        ]

    distance_between_kings = distance_between_two_kings(game.board)
    bonus_for_closeness_of_kings = (8-distance_between_kings)*0.3
    return -scores[white_king_pos[0]][white_king_pos[1]] - bonus_for_closeness_of_kings

def white_queen_endgame(board, turn):
    # Board with only a white queen and kings
    black_king_pos = board.black_king_position
    # Score based on black king position
    scores = [
        [ 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0],
        [ 7.0, 6.5, 6.5, 6.5, 6.5, 6.5, 6.5, 7.0],
        [ 7.0, 6.5, 6.0, 6.0, 6.0, 6.0, 6.5, 7.0],
        [ 7.0, 6.5, 6.0, 5.5, 5.5, 6.0, 6.5, 7.0],
        [ 7.0, 6.5, 6.0, 5.5, 5.5, 6.0, 6.5, 7.0],
        [ 7.0, 6.5, 6.0, 6.0, 6.0, 6.0, 6.5, 7.0],
        [ 7.0, 6.5, 6.5, 6.5, 6.5, 6.5, 6.5, 7.0],
        [ 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0]     
        ]

    distance_between_kings = distance_between_two_kings(board)
    bonus_for_closeness_of_kings = (8-distance_between_kings)*0.3
    return 3+scores[black_king_pos[0]][black_king_pos[1]] + bonus_for_closeness_of_kings

def black_queen_endgame(board, turn):
    white_king_pos = board.white_king_position
    # Score based on black king position
    scores = [
        [ 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0],
        [ 7.0, 6.5, 6.5, 6.5, 6.5, 6.5, 6.5, 7.0],
        [ 7.0, 6.5, 6.0, 6.0, 6.0, 6.0, 6.5, 7.0],
        [ 7.0, 6.5, 6.0, 5.5, 5.5, 6.0, 6.5, 7.0],
        [ 7.0, 6.5, 6.0, 5.5, 5.5, 6.0, 6.5, 7.0],
        [ 7.0, 6.5, 6.0, 6.0, 6.0, 6.0, 6.5, 7.0],
        [ 7.0, 6.5, 6.5, 6.5, 6.5, 6.5, 6.5, 7.0],
        [ 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0]     
        ]

    distance_between_kings = distance_between_two_kings(board)
    bonus_for_closeness_of_kings = (8-distance_between_kings)*0.3
    return -3 - scores[white_king_pos[0]][white_king_pos[1]] - bonus_for_closeness_of_kings

def distance_between_two_kings(board):
    # Given a board return the distance between the two kings
    black_king_pos = board.black_king_position
    white_king_pos = board.white_king_position
    return max(abs(black_king_pos[0]-white_king_pos[0]),abs(black_king_pos[1]-white_king_pos[1]))

# If there are only pawns left return the score evaluation if it is known

# Pass pwans get a bonus score

def pawns_only_endgame(board, turn):
    # Given a board that only contains kings and pawns return the score evaluation if it is known
    pass
    # Find furthest forward white pawns
    # Find furthest forward black pawns
    # If pawn is a pass pawn ( no threats on it's path to promo)
    
    # And also opponent king cannot reach in time
    # Add bonus
    # Only if opponent can't promote same time or before
