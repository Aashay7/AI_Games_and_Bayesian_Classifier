'''
Expectimax function used for calculating the expectation of the children 
of a given node that needs to be evaluated. 
Expectimax was used to the depth of 2. Where the factor that determines where
the current piece will be placed is determined by 
{current_piece, next_piece, expected_next_to_next_piece}
'''

class Node:
    def __init__(self, cost, moves='', piece=''):
        self.cost =  cost
        self.moves = moves
        self.piece = piece
        self.child = []
   
def newNode(cost, moves, piece):   
    temp = Node(cost, moves, piece)
    return temp

def expectedValues(node):
    children = node.child
    if len(children) == 0:
        print(node.moves , 'No Children ')
        return node.cost
    else:
        children_cost = [ch.cost for ch in children]
        print('Children Cost :', children_cost)
        print('Expected Value for Node : ', node.moves, 'is ',sum(children_cost)/ len(children_cost)) 
        return children_cost    
