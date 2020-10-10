"""
    Given a board and whose turn it is, return the score evaluation of the endgame
    Or apply bonuses for moves that are good for different end games
"""

def KPk(board, turn):
    # Given a board, and whose turn it is for a white pawn and king vs king ending
    # Return the evaluation if it is known else return unknown
    if white_pawn_promo_cannot_be_stopped(board, turn):
        return 9.0
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

    #
    print("pawn promo", num_moves_for_pawn_promo)
    print("king moves", num_king_moves)
    if num_king_moves-1 > num_moves_for_pawn_promo: # If king can catch pawn
        return True
    return False

def num_moves_for_king_to_reach_position(king_pos, pos):
    # Given a king pos [x,y] return how many moves it will take to reach pos [i,j]
    vertical = abs(king_pos[0]-pos[0])
    horizontal = abs(king_pos[1]-pos[1])

    return max(vertical, horizontal)


# Do kK and only pawns endgame

# KRk endgame... KQk endgame


# Create the same functions for black 