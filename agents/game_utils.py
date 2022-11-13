import copy
from enum import Enum
import numpy as np

BoardPiece = np.int8  # The data type (dtype) of the board
NO_PLAYER = BoardPiece(0)  # board[i, j] == NO_PLAYER where the position is empty
PLAYER1 = BoardPiece(1)  # board[i, j] == PLAYER1 where player 1 (player to move first) has a piece
PLAYER2 = BoardPiece(2)  # board[i, j] == PLAYER2 where player 2 (player to move second) has a piece

BoardPiecePrint = str  # dtype for string representation of BoardPiece
NO_PLAYER_PRINT = BoardPiecePrint(' ')
PLAYER1_PRINT = BoardPiecePrint('X')
PLAYER2_PRINT = BoardPiecePrint('O')

PlayerAction = np.int8  # The column to be played


class GameState(Enum):
    IS_WIN = 1
    IS_DRAW = -1
    STILL_PLAYING = 0


def initialize_game_state() -> np.ndarray:
    """
    Returns an ndarray, shape (6, 7) and data type (dtype) BoardPiece, initialized to 0 (NO_PLAYER).
    """
    return np.full((6, 7),NO_PLAYER,dtype=BoardPiece)


def pretty_print_board(board: np.ndarray) -> str:
    """
    Should return `board` converted to a human readable string representation,
    to be used when playing or printing diagnostics to the console (stdout). The piece in
    board[0, 0] should appear in the lower-left. Here's an example output, note that we use
    PLAYER1_Print to represent PLAYER1 and PLAYER2_Print to represent PLAYER2):
    |==============|
    |              |
    |              |
    |    X X       |
    |    O X X     |
    |  O X O O     |
    |  O O X X     |
    |==============|
    |0 1 2 3 4 5 6 |
    """
    a = '\n|===============|'
    for i in range(5, -1, -1):
        a += '\n|'
        for j in range(7):
            if (board[i][j] == PLAYER1):
                a += ' '
                a += PLAYER1_PRINT
            elif (board[i][j] == PLAYER2):
                a += ' '
                a += PLAYER2_PRINT
            else:
                a += ' '
                a += NO_PLAYER_PRINT
        a += ' |'
    a += '\n|===============|'
    a += '\n| 0 1 2 3 4 5 6 |'
    return a


def string_to_board(pp_board: str) -> np.ndarray:
    """
    Takes the output of pretty_print_board and turns it back into an ndarray.
    This is quite useful for debugging, when the agent crashed and you have the last
    board state as a string.
    """
    a = pp_board
    a = a.replace('=', '')
    a = a.replace('|', '')
    a = a.replace(' ', '')
    a = a[:len(a) - 7]

    split = a.split('\n')
    string = split[2:8]
    board = np.full((6, 7), NO_PLAYER, dtype=BoardPiece)
    for i in range(5, -1, -1):
        count = 0
        for j in string[i]:
            if (j == PLAYER1_PRINT):
                board[5 - i][count] = PLAYER1
            elif (j == PLAYER2_PRINT):
                board[5 - i][count] = PLAYER2
            count += 1

    return board

def apply_player_action(board: np.ndarray, action: PlayerAction, player: BoardPiece) -> np.ndarray:
    """
    Sets board[i, action] = player, where i is the lowest open row. Raises a ValueError
    if action is not a legal move. If it is a legal move, the modified version of the
    board is returned and the original board should remain unchanged (i.e., either set
    back or copied beforehand).
    """
    #create a real copy so board does not get changed
    newboard= copy.deepcopy(board)
    pieceplaced = 0
    if(0<=action<=6):
        if(board[5][action] == NO_PLAYER):
            for i in range(6):
                if (board[i][action] == NO_PLAYER and pieceplaced == 0):
                    newboard[i][action] = player
                    pieceplaced = 1
        else:
            raise ValueError('This column is full you cannot play here!')
    else:
        raise ValueError('Must be a number from 0 to 6')
    return newboard

def connected_four(board: np.ndarray, player: BoardPiece) -> bool:
    """
    Returns True if there are four adjacent pieces equal to `player` arranged
    in either a horizontal, vertical, or diagonal line. Returns False otherwise.
    """
    #rows = 6 columns = 7

    #check horizontally for win
    for c in range(4):
        for r in range(6):
            if (board[r][c]==player and board[r][c+1]==player and board[r][c+2]==player and board[r][c+3]==player):
                return True

    #check vertically for win
    for c in range(7):
        for r in range(3):
            if (board[r][c]==player and board[r+1][c]==player and board[r+2][c]==player and board[r+3][c]==player):
                return True

    #check for diagonals going right
    for c in range(4):
        for r in range(3):
            if (board[r][c]==player and board[r+1][c+1]==player and board[r+2][c+2]==player and board[r+3][c+3]==player):
                return True

    #check for diagonals going left
    for c in range(4):
        for r in range(3,6):
            if (board[r][c]==player and board[r-1][c+1]==player and board[r-2][c+2]==player and board[r-3][c+3]==player):
                return True
    return False
def check_end_state(board: np.ndarray, player: BoardPiece) -> GameState:
    """
    Returns the current game state for the current `player`, i.e. has their last
    action won (GameState.IS_WIN) or drawn (GameState.IS_DRAW) the game,
    or is play still on-going (GameState.STILL_PLAYING)?
    """
    if(connected_four(board,player)==True):
        return GameState.IS_WIN
    elif(board[5][0]!=NO_PLAYER and board[5][1]!=NO_PLAYER and board[5][2]!=NO_PLAYER and board[5][3]!=NO_PLAYER
        and board[5][4]!=NO_PLAYER and board[5][5]!=NO_PLAYER and board[5][6]!=NO_PLAYER):
        return GameState.IS_DRAW
    else:
        return GameState.STILL_PLAYING