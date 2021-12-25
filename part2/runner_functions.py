import time,sys
#from queue import PriorityQueue

from SimpleQuintris import *
from kbinput import *
from  cost_helper_functions import *
#from expectimax import *

# REFERENCE: FUNCTIONS FROM QUINTRIS_GAME.py PROVIDED BY PROF. CRANDALL


def hflip_piece(piece):
    return [ str[::-1] for str in piece ]

def rotate_piece(piece, rotation):
    rotated_90 = [ "".join([ str[i] for str in piece[::-1] ]) for i in range(0, len(piece[0])) ]
    return { 0: piece, 90: rotated_90, 180: [ str[::-1] for str in piece[::-1] ], 270: [ str[::-1] for str in rotated_90[::-1] ] }[rotation]

def combine(str1, str2):
      return "".join([ c if c != " " else str2[i] for (i, c) in enumerate(str1) ] )

def check_collision(board, score, piece, row, col, quintris):
      return col+len(piece[0]) > quintris.BOARD_WIDTH or row+len(piece) > quintris.BOARD_HEIGHT \
          or any( [ any( [ (c != " " and board[i_r+row][col+i_c] != " ") for (i_c, c) in enumerate(r) ] ) for (i_r, r) in enumerate(piece) ] )

def place_piece(board, score, piece, row, col, quintris):
    return (board[0:row] + \
              [ (board[i+row][0:col] + quintris.combine(r, board[i+row][col:col+len(r)]) + board[i+row][col+len(r):] ) for (i, r) in enumerate(piece) ] + \
              board[row+len(piece):], score)

def display_board(board):
    for i in range(len(board)):
        print('|',end='')
        for j in range(len(board[0])):
            print(board[i][j], end=' ')
        print('|',i)
    print('\n')

def get_unique_flips(piece, row, col, quintris):
    # CHECK IF FLIPPED PIECE == ORIGINAL PIECE, YES RETURN 1 ELSE 2
    flipped_piece = hflip_piece(piece)
    if flipped_piece == piece:
        return 1
    return 2

def get_unique_rotation(piece, row, col, quintris):
    # MAINTAIN A LIST OF ALL PIECES WITH 0, 90, 180, 270, rotations
    # GET LEN OF ALL UNIQUE PIECES PRESENT
    rotation_list = []
    for rotation in [0, 90, 180, 270]:
        new_piece = rotate_piece(piece, rotation)
        if new_piece not in rotation_list:
            rotation_list.append(new_piece)
    return (len(rotation_list))

def explore_best_moves(self, quintris, piece_distribution):
    #fringe = PriorityQueue()
    #moves = ''
    #root = newNode(0, '', quintris.piece)
    piece = quintris.piece
    #best_move, max_exp, new_root = evaluator(self, quintris, quintris.get_board(), piece, root)
    best_move = evaluator(self, quintris, quintris.get_board(), piece)
    if (best_move == ''):
        return ''
    print('\nPiece Distribution : ', piece_distribution)
    print('\nBest Move : ', best_move)
    return best_move

def game_commands_generator(piece, row, col, quintris):
    list_all_game_commands = []
    cmd = ''
    unique_flips = get_unique_flips(piece, row, col, quintris)
    unique_rotation = get_unique_rotation(piece, row, col, quintris)
    for i in range(unique_flips):
        cmd += 'h'*i
        s0 = cmd
        for j in range(unique_rotation):
            cmd = s0 + 'n'*j
            s1 = cmd
            for k in range(quintris.BOARD_WIDTH - min(len(piece[0]), len(piece))+1):
                if(k < col):
                    cmd = s1 + 'b'*(col-k)
                elif(k > col):
                    cmd = s1 + 'm'*(k-col)
                else:
                    cmd = s1
                if cmd not in list_all_game_commands:
                    list_all_game_commands.append(cmd)
                cmd = ''
    
    if (max(len(piece), len(piece[0])) + col) > (quintris.BOARD_WIDTH):
        delta = abs((max(len(piece), len(piece[0])) + col) - (quintris.BOARD_WIDTH-1))
        list_of_all_n_h = [cmd for cmd in list_all_game_commands if 'n' in cmd or 'h' in cmd] 
        updated_list_of_all_n_h = [('bb' + cmd + 'mm') for cmd in list_all_game_commands if 'n' in cmd or 'h' in cmd]
        updated_list_of_all_n_h_final = [cmd.replace('bbmm','').replace('bm','') for cmd in updated_list_of_all_n_h]
        for i, cmd in enumerate(list_all_game_commands):
            if(cmd in list_of_all_n_h):
                index = list_of_all_n_h.index(cmd)
                list_all_game_commands[i] = updated_list_of_all_n_h_final[index]
    return list_all_game_commands

def createPieceConfiguration(piece, game_commands, board, piece_row, piece_col, quintris):
    for cmd in list(game_commands): 
        if cmd == 'h':
            piece = hflip_piece(piece)
        if cmd == 'n':
            piece = rotate_piece(piece, 90)
        if cmd == 'b':
            if (not check_collision(board, 0, piece, piece_row, piece_col-1, quintris)) and piece_col-1 >= 0:
                piece_col -= 1
        if cmd == 'm':
            if (not check_collision(board, 0, piece, piece_row, piece_col+1, quintris)) and piece_col+1 < quintris.BOARD_WIDTH:
                piece_col += 1 

    while not check_collision(board, 0, piece,  piece_row, piece_col, quintris):
        piece_row += 1
    
    new_board, _ = place_piece(board, 0, piece, piece_row-1, piece_col, quintris)
    return new_board
  
def get_best_cost(piece, list_game_commands, board, row, col, quintris):
    all_scores = {}
    scores_board = []
    for cmd in list_game_commands:
        try:
            new_board = createPieceConfiguration(piece, cmd, board, row, col,  quintris)
        except:
            return None, None
        score  = cost_function(board, new_board, quintris)
        all_scores[cmd] = score
        scores_board.append((cmd, score, new_board))
    return all_scores, scores_board

def evaluator(self, quintris, board, piece, ):
    '''
    - Successor function that calls the game_commands_generator that returns the list of 
    all possible commands that lead the piece to non-redundant states. 
    - 
    '''
    
    # METRICS : 
    #score_mtx = [[1*r if board[r][c] == 'x' else 0 for c in range(len(board[0]))] for r in range(len(board)) ]
    #open_space_mtx = [[1 if board[r][c] != 'x' else 0 for c in range(len(board[0]))] for r in range(len(board)) ]
    #summed_up = [sum(arr) for arr in score_mtx]
    #open_space_left = [sum(arr) for arr in open_space_mtx]
    #percent_space_left = [sum(arr) / len(arr) for arr in open_space_mtx]
    row = quintris.row
    col = quintris.col
    while not check_collision(board, 0, piece,  row, col, quintris):
        row+=1
    display_board(board)
    list_game_commands = game_commands_generator(piece, row, col, quintris)
    all_scores, scores_board = get_best_cost(piece, list_game_commands, board, quintris.row, quintris.col, quintris)
    if all_scores == None:
        return ''
    best_score = {min(all_scores, key=all_scores.get) : min(all_scores.values())}
    
    ### EXPECTIMAX - STEP 1 - Performs poorly. 
    # Observation : As the combination of state configuration of current piece and next piece 
    # are considered. 
    # Example for an 'L' shaped block there are 112 possibilities on a 25x15 board considering 
    # the 2 flip states x 4 flips states x 15 columns. =~ 120. There are boundary states which 
    # are invalid or redundant. 
    # Back to our observation - Considering the 'L' shaped piece with n=112 possibilities and 
    # some other piece with some m or n possiblilites. So, in total, we get approximately 112*112
    # possibilities. 
    # When exploring the states, when we consider the lowest cost function value of the combinations,
    # The best configuration of current_piece and next_piece for current state 
    # sets the location and configuration of the current_piece. After this the next state becomes
    # current state and when we check the configuration  
    # 
    '''
    next_piece = quintris.next_piece
    print('\n\n\nNEXT PIECE : ', next_piece, '\nBOARD ROW :', )
    next_row = 0
    next_col = 0 
    expectation_scores_board = []
    for sb in scores_board:
        print('EXPLORING NEXT STATE : ')
        #print(sb)
        current_move = sb[0]
        current_score = sb[1]
        current_board = sb[2]
        next_list_game_commands = game_commands_generator(next_piece, next_row, next_col, quintris)
        print('Current Board : ')
        display_board(current_board)
        next_all_scores, next_scores_board = get_best_cost(next_piece, next_list_game_commands, current_board, next_row, next_col, quintris)    
        #expectation_scores_board.append((current_move, current_score, current_board, ))
        #expectation = sum(next_all_scores.values()) / len(next_all_scores)
        expectation = min(next_all_scores.values())
        print('Expectation : ', expectation)
        expectation_scores_board.append((next_piece, current_move, current_score, expectation))
    
    print('\n\nEXPECTATIONS OF ALL MOVES : \n')
    
    max_val=5000
    max_exp=()
    for i in expectation_scores_board:
        if i[3] > max_val:
            max_exp = i
    print('\nMax Exp : ', max_exp )
    '''
    '''
    min_val=5000
    min_exp=()
    print('Expectation Score Board : \n', expectation_scores_board)
    for i in expectation_scores_board:
        if i[3] < min_val:
            min_exp = i
    print('\Min Exp : ', min_exp )
    
    '''
    
    print('Best Score : ', best_score)
    #return min_exp[1] #, max_exp, root
    print('Val: ',list(best_score.keys())[0])
    return list(best_score.keys())[0]