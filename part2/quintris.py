# Simple quintris program! v0.2
# D. Crandall, Sept 2021

## Written by : Aashay Gondalia (aagond), Harsh Atha(hatha), Sai Hari (saimorap)

from AnimatedQuintris import *
from SimpleQuintris import *
from runner_functions import *
from kbinput import *
from animatedLogic import *
import time, sys


piece_distribution = {}
PIECES = [ [ " x ", "xxx", " x "], [ "xxxxx" ], [ "xxxx", "   x" ], [ "xxxx", "  x " ], [ "xxx", "x x"], [ "xxx ", "  xx" ] ]
rotations = [0, 90, 180, 270]

class HumanPlayer:

    def get_moves(self, quintris):
        print("Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\n  h for horizontal flip\nThen press enter. E.g.: bbbnn\n")
        moves = input()
        return moves
        

    def control_game(self, quintris):
        while 1:
            c = get_char_keyboard()            
            commands =  { "b": quintris.left, "h": quintris.hflip, "n": quintris.rotate, "m": quintris.right, " ": quintris.down }
            commands[c]()
            
#####
# This is the part you'll want to modify!
# Replace our super simple algorithm with something better
#
class ComputerPlayer:
    # This function should generate a series of commands to move the piece into the "optimal"
    # position. The commands are a string of letters, where b and m represent left and right, respectively,
    # and n rotates. quintris is an object that lets you inspect the board, e.g.:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #
    # PIECES : [ " x ", "xxx", " x "], [ "xxxxx" ], [ "xxxx", "   x" ], [ "xxxx", "  x " ], [ "xxx", "x x"], [ "xxx ", "  xx" ]
    #      x         
    #     xxx       xxxxx       xxxx        xxxx         xxx         xxx 
    #      x                       x          x          x x           xx
    
    def get_moves(self, quintris):
        # super simple current algorithm: just randomly move left, right, and rotate a few times
        # Shape of the board : quintris.BOARD_HEIGHT x quintris.BOARD_WIDTH
        pieces = [rotate_piece(quintris.piece, rt) for rt in rotations]
        pieces.extend([ hflip_piece(rotate_piece(quintris.piece, rt)) for rt in rotations])
        index= [idx for idx,piece in enumerate(PIECES) if piece in pieces]
        pieceA = PIECES[index[0]]
        if (str(pieceA) not in piece_distribution.keys()):
            piece_distribution[str(pieceA)] = 0
        piece_distribution[str(pieceA)] += 1
        moves =  explore_best_moves(self, quintris, piece_distribution)
        print('\n\nPiece Distribution : \n',piece_distribution)
        print('Next Piece : ', quintris.next_piece)
        return moves

    # This is the version that's used by the animted version. This is really similar to get_moves,
    # except that it runs as a separate thread and you should access various methods and data in
    # the "quintris" object to control the movement. In particular:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #
            
    def control_game(self, quintris):
        # another super simple algorithm: just move piece to the least-full column
        while 1:
            time.sleep(0.1)
            board = quintris.get_board()
            column_heights = [ min([ r for r in range(len(board)-1, 0, -1) if board[r][c] == "x"  ] + [100,] ) for c in range(0, len(board[0]) ) ]
            index = column_heights.index(max(column_heights))
            commands =  { "b": quintris.left, "h": quintris.hflip, "n": quintris.rotate, "m": quintris.right, " ": quintris.down }

            moves = animated_explore_best_moves(self, quintris)
            for move in moves:
                commands[move]()
            quintris.down()

            if(index < quintris.col):
                quintris.left()
            elif(index > quintris.col):
                quintris.right()
            else:
                quintris.down()


###################
#### main program

(player_opt, interface_opt) = sys.argv[1:3]

try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print("unknown player!")

    if interface_opt == "simple":
        quintris = SimpleQuintris()
    elif interface_opt == "animated":
        quintris = AnimatedQuintris()
    else:
        print("unknown interface!")

    quintris.start_game(player)
    print('\n\nEND ', quintris.score)

except EndOfGame as s:
    print("\n\n\n", s)