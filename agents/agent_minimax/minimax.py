from agents.game_utils import *
from typing import Union
import random
import math


def generate_move(board: np.ndarray, player: BoardPiece, saved_state: Optional[SavedState])\
        -> tuple[Union[PlayerAction, None], Optional[SavedState]]:
    return minimax(board, 4, -10000000, 10000000, player, True)[0], saved_state


def minimax(board: np.ndarray, depth:int, alpha: int,
            beta: int, player: BoardPiece, is_maximizing_player: bool) -> tuple[Union[int, None], int]:
    possible_columns = possible_locations(board)
    is_leaf = is_leaf_node(board)

    if depth == 0 or is_leaf:
        if is_leaf:
            if connected_four(board, PLAYER1):
                return None, 100000
            elif connected_four(board, PLAYER2):
                return None, -100000
            else:
                return None, 0
        else:
            return None, calculate_heuristic(board, PLAYER1)
    if is_maximizing_player:
        value = -math.inf
        player_action = random.choice(possible_columns)
        for i in possible_columns:
            board_copy = board.copy()
            apply_player_action(board_copy, player_action, player)

            opponent = PLAYER2
            if player == PLAYER2:
                opponent = PLAYER1

            new_value = minimax(board_copy, depth-1, alpha, beta, opponent,  False)[1]

            value = max(value, new_value)

            if new_value > value:
                player_action = i

            alpha = max(alpha, value)
            if alpha >= beta:
                break

        return player_action, value
    else:
        value = math.inf
        player_action = random.choice(possible_columns)
        for i in possible_columns:
            board_copy = board.copy()
            apply_player_action(board_copy, player_action, player)

            opponent = PLAYER2
            if player == PLAYER2:
                opponent = PLAYER1

            new_value = minimax(board_copy, depth-1, alpha, beta, opponent, True)[1]

            value = min(value, new_value)

            if new_value < value:
                value = new_value
                player_action = i

            beta = min(beta, value)
            if alpha >= beta:
                break

        return player_action, value


"""
returns a list of all columns that are not full yet
"""


def possible_locations(board: np.ndarray) -> list:
    possible_locs = []

    for i in range(7):
        if board[5][i] == NO_PLAYER:
            possible_locs.append(i)
    return possible_locs


"""
check if the minimax algorithm can't calculate any further because game is over
"""


def is_leaf_node(board: np.ndarray):
    return connected_four(board,PLAYER1) or connected_four(board,PLAYER2) or len(possible_locations(board)) == 0


"""
approximate a value for the list by counting own pieces and assigning values to the amount of found pieces
"""


def calculate_area(area: list, player: BoardPiece ):
    value = 0

    # make sure to calculate for the right player
    opponent = PLAYER2
    if player == PLAYER2:
        opponent = PLAYER1

    # if 4 pieces return highest value, different scaling possible for more accurate play
    if area.count(player) >= 4:
        value += 200
    # check if less than 4 pieces in area that there are enough empty spaces so winning is still possible
    elif area.count(player) == 3 and area.count(NO_PLAYER) >= 1:
        value += 20
    elif area.count(player) == 2 and area.count(NO_PLAYER) >= 2:
        value += 5
    # make sure to be aware of opponents ability to connect 4 as well, by reducing score if a threat of loss exists
    if area.count(opponent) == 3 and area.count(NO_PLAYER) >= 1:
        value -= 1000

    return  value


"""
to improve runtime and code readability split calculations into areas to independently score
"""


def calculate_heuristic(board:np.ndarray, player: BoardPiece) -> int:
    heuristic = 0

    # calculate heuristic by going through rows
    for i in range(6):
        rows_array = []
        for j in list(board[i, :]):
            rows_array.append(int(j))
        for h in range(4):
            area = rows_array[h:h+4]
            heuristic += calculate_area(area, player)

    # calculate heuristic by going through columns
    for i in range(7):
        columns_array = []
        for j in list(board[:, i]):
            columns_array.append(int(j))
        for h in range(3):
            area = columns_array[h:h+4]
            heuristic += calculate_area(area, player)

    # calculate heuristic by going through diagonals going right
    for i in range(3):
        for j in range(4):
            area = []
            for h in range(4):
                area.append([board[i + h][j + h]])
                heuristic += calculate_area(area, player)

    # calculate heuristic by going through diagonals going left
    for i in range(3):
        for j in range(4):
            area = []
            for h in range(4):
                area.append([board[i+3 - h][j + h]])
                heuristic += calculate_area(area, player)

    return heuristic
