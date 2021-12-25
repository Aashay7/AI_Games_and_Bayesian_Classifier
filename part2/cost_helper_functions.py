# TODO : Build these functions
# ACCESS EACH CONFIG BASED ON THESE
# REFERENCES
#https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/
#http://yutow.squarespace.com/gameplaying-ai
#https://www.geeksforgeeks.org/generic-tree-level-order-traversal/
#https://www.geeksforgeeks.org/expectimax-algorithm-in-game-theory/
#https://luckytoilet.wordpress.com/2011/05/27/coding-a-tetris-ai-using-a-genetic-algorithm/
#https://towardsdatascience.com/beating-the-world-record-in-tetris-gb-with-genetics-algorithm-6c0b2f5ace9b

# SUCCESSOR - TOP K BOARD CONFIG - EXPLORE THEM ?
## [-0.1144, -0.3810,  0.1531, -0.0710,  0.7075, -0.6559,  1.6902, -1.5014, -3.6355]
## get_aggregate_height    -0.1144
## number_of_holes         -0.3810
## num_col_one_hole         0.1531
## bumpiness               -0.0710
## row_transitions          0.7075
## column_transitions      -0.6559
## num_pits                 1.6902
## deepest_well            -1.5014
## num_lines_cleared       -3.6355
def get_weights():
    # Emperically determined values.
    weights = {}
    weights['agg_ht'] = 1.6
    weights['num_holes'] = 8.3
    weights['bumps'] = 0.76
    weights['abs_mean_diff'] = 0.63
    weights['lines_cleared'] = -100000
    weights['reached_top'] = 100
    #weights['num_holes'] = 0.5
    #weights['n_pits'] = 0.07
    #weights['dp_well'] = 0.707
    #weights['num_col_holes'] = 0.46
    #weights['rt'] = 1.0
    #weights['ct'] = 1.5
    return weights

def remove_complete_lines(quintris, board, score):
    complete = [ i for (i, s) in enumerate(board) if s.count(' ') == 0 ]
    return ( [(" " * quintris.BOARD_WIDTH),] * len(complete) + [ s for s in board if s.count(' ') > 0 ], score + len(complete) )


def get_peaks(board, quintris):
    heights = []
    for i in range(quintris.BOARD_WIDTH):
        ht = 0
        for j in range(quintris.BOARD_HEIGHT):
            if board[j][i] == 'x':
                break
            else:   
                ht+=1   
        heights.append(quintris.BOARD_HEIGHT - ht)
    return heights

def get_holes(board, quintris):
    hole_list = []
    heights = get_peaks(board, quintris)
    for col,h in enumerate(heights):
        holes = 0
        for row in range(heights[col]):
            if(board[quintris.BOARD_HEIGHT - row - 1][col]) != 'x':
                holes+=1
        hole_list.append(holes)
    return hole_list

def get_aggregate_height(heights):
    return sum(heights)
    
def number_of_holes(hole_list):
    return sum(hole_list)

def num_col_atleast_one_hole(hole_list):
    num_col_atleast_one = len([hole for hole in hole_list if hole != 0])
    return num_col_atleast_one

def bumpiness(heights):
    bumps = [abs(heights[i] - heights[i+1]) for i in range(len(heights) - 1)]
    return sum(bumps)  

def row_transitions(heights, board, quintris):
    rt_list = []
    highest_peak = max(heights)
    for col,h in enumerate(heights):
        if col == quintris.BOARD_WIDTH - 1:
            break
        rt = 0
        for row in range(highest_peak):
            if(board[quintris.BOARD_HEIGHT - row - 1][col]) != board[quintris.BOARD_HEIGHT - row - 1][col+1]:
                rt+=1
        rt_list.append(rt)
    return sum(rt_list)
    
def mean_heights_difference(heights):
    mean = sum(heights) / len(heights)
    abs_diff = [abs(mean-heights[i]) for i in range(len(heights))]
    mean_abs_diff = sum(abs_diff) / len(abs_diff)
    return mean_abs_diff   

def column_transitions(heights, board, quintris):
    ct_list = []
    highest_peak = max(heights)
    for col,h in enumerate(heights):
        ct = 0
        for row in range(highest_peak):
            if(board[quintris.BOARD_HEIGHT - row - 1][col]) != board[quintris.BOARD_HEIGHT - row - 2][col]:
                ct+=1
        ct_list.append(ct)
    return sum(ct_list)

def num_pits(heights):
    return sum([height for height in heights if height == 0 ])

def deepest_well(heights, board, quintris):
    wells = []
    for i in range(len(heights)):
        if i == 0:
            w = heights[1] - heights[0]
            w = max(w,0)
        elif i == len(heights) - 1 :
            w = heights[-2] - heights[-1]
            w = max(w,0)
        else:
            w1 = heights[i-1] - heights[i] 
            w2 = heights[i+1] - heights[i]
            w = max(w1, w2, 0)
        wells.append(w)
    return max(wells)

def num_lines_cleared(old_board, board, quintris):
    lines_cleared = remove_complete_lines(quintris, board, 0)[-1]
    return lines_cleared
    
def get_reached_top(heights, quintris):
    if max(heights) >= quintris.BOARD_HEIGHT - 3 :
        return 1
    return 0

def cost_function(old_board, board, quintris):
    weights = get_weights()
    heights = get_peaks(board, quintris)
    agg_ht = get_aggregate_height(heights)
    bumps = bumpiness(heights)
    #n_pits = num_pits(heights)
    hole_list = get_holes(board, quintris)
    num_holes = number_of_holes(hole_list)
    #num_col_holes = num_col_atleast_one_hole(hole_list)
    mean_abs_diff = mean_heights_difference(heights)
    #rt = row_transitions(heights, board, quintris)
    #ct = column_transitions(heights, board, quintris)
    #sdp_well = deepest_well(heights, board, quintris)
    lines_cleared = num_lines_cleared(old_board, board, quintris)
    reached_top =  get_reached_top(heights, quintris)
    
    cost = (agg_ht * weights['agg_ht']) + (num_holes * weights['num_holes']) + \
        + (bumps * weights['bumps'])+ \
        + (lines_cleared * weights['lines_cleared']) \
        + (mean_abs_diff * weights['abs_mean_diff'])  \
        + (reached_top * weights['reached_top'])
    
    #print('\nTHE COST IS : ', cost)
    return round(cost,3)