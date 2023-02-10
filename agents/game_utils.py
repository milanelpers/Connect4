import copy
from enum import Enum
import numpy as np
from typing import Callable, Optional


BOARD_COLS = 7
BOARD_ROWS = 6
BOARD_SHAPE = (6, 7)
INDEX_HIGHEST_ROW = BOARD_ROWS - 1
INDEX_LOWEST_ROW = 0

BoardPiece = np.int64  # The data type (dtype) of the board
NO_PLAYER = BoardPiece(0)  # board[i, j] == NO_PLAYER where the position is empty
PLAYER1 = BoardPiece(1)  # board[i, j] == PLAYER1 where player 1 (player to move first) has a piece
PLAYER2 = BoardPiece(2)  # board[i, j] == PLAYER2 where player 2 (player to move second) has a piece

BoardPiecePrint = str  # dtype for string representation of BoardPiece
NO_PLAYER_PRINT = BoardPiecePrint(' ')
PLAYER1_PRINT = BoardPiecePrint('X')
PLAYER2_PRINT = BoardPiecePrint('O')

PlayerAction = np.int64  # The column to be played


class GameState(Enum):
    IS_WIN = 1
    IS_DRAW = -1
    STILL_PLAYING = 0


class SavedState:
    pass


GenMove = Callable[
    [np.ndarray, BoardPiece, Optional[SavedState]],  # Arguments for the generate_move function
    tuple[PlayerAction, Optional[SavedState]]  # Return type of the generate_move function
]


def initialize_game_state():
    """
    returns a tuple of the bitboards for player1 and player2
    """
    board1 = 0b0000000_0000000_0000000_0000000_0000000_0000000_0000000
    board2 = 0b0000000_0000000_0000000_0000000_0000000_0000000_0000000
    return board1, board2


def get_bitboard(board: np.ndarray) -> tuple:
    board1, board2 = '', ''
    for j in range(6, -1, -1):
        board1 += '0'
        board2 += '0'
        for i in range(0, 6):
            board1 += ['0', '1'][board[i, j] == PLAYER1]
            board2 += ['0', '1'][board[i, j] == PLAYER2]
    board1 = format(int(board1, 2), '049b')
    board2 = format(int(board2, 2), '049b')
    return int(board1, 2), int(board2, 2)


def connected_four(board: tuple, player: BoardPiece):
    if player == PLAYER1:
        position = board[0]
    else:
        position = board[1]
    #Horizontal
    check = position & (position >> 7)
    if check & (check >> 14):
        return True
    #Vertical
    check = position & (position >> 1)
    if check & (check >> 2):
        return True
    #Diagonal going left
    check = position & (position >> 6)
    if check & (check >> 12):
        return True
    #Diagonal going right
    check = position & (position >> 8)
    if check & (check >> 16):
        return True
    return False


def apply_player_action(board: tuple, action: PlayerAction, player: BoardPiece) -> tuple:
    board1 = board[0]
    board2 = board[1]
    mask = board1 | board2
    if player == PLAYER1:
        new_mask = mask | (mask + (1 << (action*7)))
        board1 = board2 ^ new_mask
    else:
        new_mask = mask | (mask + (1 << (action*7)))
        board2 = board1 ^ new_mask
    return board1, board2


def pretty_print_board(board: tuple) -> str:
    board1 = board[0]
    board2 = board[1]
    mask = board1 | board2

    p1str = str(bin(board1))[2:]
    maskstr = str(bin(mask))[2:]
    p2str = str(bin(board2))[2:]

    if len(p1str) < 49:
        for i in range(49-len(p1str)):
            p1str = '0' + p1str
    if len(maskstr) < 49:
        for i in range(49-len(maskstr)):
            maskstr = '0' + maskstr
    if len(p2str) < 49:
        for i in range(49-len(p2str)):
            p2str = '0' + p2str
    string = '\n|===============|'
    for j in range(6):
        string += '\n|'
        for i in range(j+43,0,-7):
            if maskstr[i] == '0':
                string += ' '
                string += '-'
            elif maskstr[i]=='1' and p1str[i]=='1':
                string += ' '
                string += PLAYER1_PRINT
            elif maskstr[i]=='1' and p2str[i]=='1':
                string += ' '
                string += PLAYER2_PRINT
        string += ' |'
    string += '\n|===============|'
    string += '\n| 0 1 2 3 4 5 6 |'
    return string


def string_to_board(pp_board: str) -> tuple:
    string = pp_board
    string = string.replace('=', '')
    string = string.replace('|', '')
    string = string.replace(' ', '')
    string = string[:len(string) - 7]

    # split string by lines
    split = string.split('\n')
    string = split[2:8]
    board1, board2 = '', ''
    for j in range(6, -1, -1):
        board1 += '0'
        board2 += '0'
        for i in range(0, 6):
            board1 += ['0', '1'][string[i][j] == PLAYER1_PRINT]
            board2 += ['0', '1'][string[i][j] == PLAYER2_PRINT]
    board1 = format(int(board1, 2), '049b')
    board2 = format(int(board2, 2), '049b')
    return int(board1, 2), int(board2, 2)



"""
Was supposed to be run with numba for faster calculations, but had problems with that
"""


def possible_actions(board: tuple) -> list:
    """Generates a list of all possible actions that could be played on the given board

    Parameters
    ----------
    board : np.ndarray
        Current board

    Returns
    -------
    list
        A list of all columns of the board that have a BoardPiece representing NO_PLAYER
    """
    possible_actions_list = []
    mask = board[0] | board[1]
    column0full = 0b0000000_0000000_0000000_0000000_0000000_0000000_0100000
    column1full = 0b0000000_0000000_0000000_0000000_0000000_0100000_0000000
    column2full = 0b0000000_0000000_0000000_0000000_0100000_0000000_0000000
    column3full = 0b0000000_0000000_0000000_0100000_0000000_0000000_0000000
    column4full = 0b0000000_0000000_0100000_0000000_0000000_0000000_0000000
    column5full = 0b0000000_0100000_0000000_0000000_0000000_0000000_0000000
    column6full = 0b0100000_0000000_0000000_0000000_0000000_0000000_0000000
    columncheck = [column0full, column1full, column2full, column3full, column4full, column5full, column6full]
    for col, value in enumerate(columncheck):
        if mask & value == 0:
            possible_actions_list.append(col)

    return possible_actions_list


def possible_boards(board: tuple, player: BoardPiece) -> list:
    """Generates a list of all possible boards, that can exist one action deep on a given board from a given player

    Parameters
    ----------
    board : np.ndarray
        Current board
    player : BoardPiece
        Player whose turn it is

    Returns
    -------
    list
        A list of all possible boards after applying all possible actions on the board from the player
    """
    possible_boards_list = []
    for x in possible_actions(board):
        possible_boards_list.append(apply_player_action(board, x, player))
    return possible_boards_list


def check_end_state(board, player):
    board1 = board[0]
    board2 = board[1]
    drawnboard = 0b0111111_0111111_0111111_0111111_0111111_0111111_0111111
    mask = board1 | board2

    if connected_four(board, player):
        return GameState.IS_WIN
    elif mask == drawnboard:
        return GameState.IS_DRAW
    else:
        return GameState.STILL_PLAYING




