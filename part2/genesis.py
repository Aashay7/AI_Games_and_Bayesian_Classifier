# Training Genetic Algorithm
# Incomplete implementation.
import numpy as np
from quintris  import *
population = 1000 

total_games = 100
most_pieces = 500 
print(np.random.rand() - 0.5)

class ComputerPlayerTrain:
    def __init__(self, weights):
        self.weights = weights

    def get_moves(self, quintris):
        # super simple current algorithm: just randomly move left, right, and rotate a few times
        # Shape of the board : quintris.BOARD_HEIGHT x quintris.BOARD_WIDTH
        print('Piece : ', quintris.piece)        
        move =  explore_best_moves(self, quintris)
        return move
        #return random.choice("mnbh") * random.randint(1, 10)
        
    def control_game(self, quintris):
        # another super simple algorithm: just move piece to the least-full column
        while 1:
            time.sleep(0.1)
            board = quintris.get_board()
            column_heights = [ min([ r for r in range(len(board)-1, 0, -1) if board[r][c] == "x"  ] + [100,] ) for c in range(0, len(board[0]) ) ]
            index = column_heights.index(max(column_heights))

            if(index < quintris.col):
                quintris.left()
            elif(index > quintris.col):
                quintris.right()
            else:
                quintris.down()

def fitness(candidates, total_games, maxMoves):
    player = ComputerPlayerTrain([0,0,0,0,0,0,0,0])
    quintris = SimpleQuintris()

    print('Start Game : ')
    quintris.start_game(player)


if __name__ == '__main__':
    fitness(population, 100, 500)

   

