from typing import Optional, Tuple

import numpy as np

from agents.game_utils import BoardPiece, SavedState, PlayerAction, NO_PLAYER, possible_actions, PLAYER1, PLAYER2, \
    check_end_state, GameState, apply_player_action, connected_four, possible_boards, pretty_print_board


def generate_move_minimax(
        board: tuple, player: BoardPiece, saved_state: Optional[SavedState]
) -> Tuple[PlayerAction, Optional[SavedState]]:
    """Chooses the best action based on the minimax algorithm given a board and the current player

    Parameters
    ----------
    board : np.ndarray
        Current Board
    player : BoardPiece
        Player whose turn it is
    saved_state : SavedState, optional
        Cached results

    Returns
    -------
    PlayerAction
        The column the piece will be "dropped" into
    """
    # The board is always mapped to PLAYER1 so
    # minimax can assume that PLAYER1 is always the maximizing player

    if player == PLAYER2:
        board = map_board_to_player_one(board)
        player = PLAYER1

    depth = 4

    best_action = 0
    best_evaluation = -999999

    for action in possible_actions(board):
        temp_evaluation = minimax(apply_player_action(board, action, player), other_player(player), depth)
        if temp_evaluation > best_evaluation:
            best_evaluation = temp_evaluation
            best_action = action

    return best_action, saved_state


def minimax(board: tuple, player: BoardPiece, depth: int) -> int:
    """Evaluates a board for a given player simulated to a given depth to ensure the highest advantage

    Parameters
    ----------
    board : np.ndarray
        Current board
    player : BoardPiece
        Player whose turn it is
    depth : int
        Depth to which the simulation is carried out

    Returns
    -------
    int
        An int representing the advantageousness of a board
    """
    state_of_game = check_end_state(board, player)
    game_is_lost = check_end_state(board, other_player(player)) == GameState.IS_WIN
    if depth == 0 or state_of_game != GameState.STILL_PLAYING or game_is_lost:
        return heuristic(board)
    if player == PLAYER1:
        max_evaluation = -999999
        for x in possible_boards(board, PLAYER1):
            board_evaluation = minimax(x, PLAYER2, depth - 1)
            max_evaluation = max(max_evaluation, board_evaluation)
        return max_evaluation
    else:
        min_evaluation = 999999
        for x in possible_boards(board, PLAYER2):
            board_evaluation = minimax(x, PLAYER1, depth - 1)
            min_evaluation = min(min_evaluation, board_evaluation)
        return min_evaluation


def heuristic(board: tuple) -> int:
    """Evaluates the advantage of Player 1 on given board

    Parameters
    ----------
    board : tuple of player bitboards

    Returns
    -------
    int
        Value greater than 0 indicates an advantage for Player 1 and a values less than 0 a disadvantage
    """
    if connected_four(board, PLAYER1):
        return 100
    if connected_four(board, PLAYER2):
        return -100
    a = count_three(board, PLAYER1) + count_two(board, PLAYER1) + count_one(board, PLAYER1)
    b = count_three(board, PLAYER2) + count_two(board, PLAYER2) + count_one(board, PLAYER2)
    return a - b


def count_three(board: tuple, player: BoardPiece):
    board1 = board[0]
    board2 = board[1]
    invboard = ~(board1 | board2)
    if player == PLAYER1:
        check = board1
    else:
        check = board2
    r7b = check >> 7
    l7b = check << 7
    r14b = check >> 14
    l14b = check << 14
    r16b = check >> 16
    l16b = check << 16
    r8b = check >> 8
    l8b = check << 8
    r6b = check >> 6
    l6b = check << 6
    r12b = check >> 12
    l12b = check << 12

    # check horizontal
    result = invboard & r7b & r14b & (check >> 21)

    result |= invboard & r7b & r14b & l7b

    result |= invboard & r7b & l7b & l14b

    result |= invboard & l7b & l14b & (check << 21)

    # check diagonals going right
    result |= invboard & r8b & r16b & (check >> 24)

    result |= invboard & r8b & r16b & l8b

    result |= invboard & r8b & l8b & l16b

    result |= invboard & l8b & l16b & (check << 24)

    # check diagonals going left
    result |= invboard & r6b & r12b & (check >> 18)

    result |= invboard & r6b & r12b & l6b

    result |= invboard & r6b & l6b & l12b

    result |= invboard & l6b & l12b & (check << 18)

    # check vertical
    result |= invboard & (check << 1) & (check << 2) & (check << 3)

    result = int.bit_count(result)
    return result


def count_two(board: tuple, player: BoardPiece):
    board1 = board[0]
    board2 = board[1]
    invboard = ~(board1 | board2)
    if player == PLAYER1:
        check = board1
    else:
        check = board2

    invboard = ~(board1 | board2)
    r7b = check >> 7
    r14b = check >> 14
    l7b = check << 7
    l14b = check << 14
    r8b = check >> 8
    l8b = check << 8
    l16b = check << 16
    r16b = check >> 16
    r6b = check >> 6
    l6b = check << 6
    r12b = check >> 12
    l12b = check << 12

    # check horizontal left
    result = invboard & r7b & r14b
    result |= invboard & r7b & r14b
    result |= invboard & r7b & l7b

    # check horizontal right
    result |= invboard & l7b & l14b

    # check for diagonals going right
    result |= invboard & l8b & l16b

    result |= invboard & r8b & r16b
    result |= invboard & r8b & r16b
    result |= invboard & r8b & l8b

    # check diagonals going left
    result |= invboard & r6b & r12b
    result |= invboard & r6b & r12b
    result |= invboard & r6b & l6b
    result |= invboard & l6b & l12b

    # check vertical
    result |= invboard & (check << 1) & (check << 2)
    result = int.bit_count(result)
    return result


def count_one(board: tuple, player: BoardPiece):
    board1 = board[0]
    board2 = board[1]
    invboard = ~(board1 | board2)
    if player == PLAYER1:
        check = board1
    else:
        check = board2
    # check horizontal left
    result = invboard & (check >> 7)

    # check horizontal right
    result |= invboard & (check << 7)

    # check vertical
    result |= invboard & (check << 1)
    result = int.bit_count(result)
    return result
def other_player(player: BoardPiece):
    if player == PLAYER1:
        return PLAYER2
    elif player == PLAYER2:
        return PLAYER1


def map_board_to_player_one(board: tuple) -> tuple:
    """Creates a board with the BoardPieces of Player1 and Player2 switched

    Parameters
    ----------
    board : np.ndarray
        Current Board

    Returns
    -------
    np.ndarray
        A modified board with the BoardPieces of Player1 and Player2 switched
    """
    return board[1], board[0]
