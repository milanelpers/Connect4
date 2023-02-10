from typing import Optional, Tuple

import numpy as np

from agents.game_utils import BoardPiece, SavedState, PlayerAction, NO_PLAYER, possible_actions, PLAYER1, PLAYER2, \
    check_end_state, GameState, apply_player_action, connected_four, possible_boards, pretty_print_board


def generate_move_minimax(
        board: np.ndarray, player: BoardPiece, saved_state: Optional[SavedState]
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


def minimax(board: np.ndarray, player: BoardPiece, depth: int) -> int:
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


def heuristic(board: np.ndarray) -> int:
    """Evaluates the advantage of Player 1 on given board

    Parameters
    ----------
    board : np.ndarray

    Returns
    -------
    int
        Value greater than 0 indicates an advantage for Player 1 and a values less than 0 a disadvantage
    """
    if connected_four(board, PLAYER1):
        return 100
    if connected_four(board, PLAYER2):
        return -100
    a = connected_three(board, PLAYER1) + connected_two(board, PLAYER1)
    b = connected_three(board, PLAYER2 + connected_two(board, PLAYER2))
    return a - b


def connected_three(board: np.ndarray, player: BoardPiece) -> int:
    """Counts how many three adjacent pieces equal to 'player' arranged in either direction on the given board

       Parameters
       ----------
       board : np.ndarray
           Current board
       player : BoardPiece
           Player whose turn it is

       Returns
       -------
       int
           Number of three adjacent pieces equal to 'player' arranged in either direction
       """
    connect_three_counter = 0

    for x in range(6):
        counter = 0
        for y in range(7):
            if board[x, y] == player:
                counter += 1
            else:
                counter = 0
            if counter == 3:
                connect_three_counter += 1

    for y in range(7):
        counter = 0
        for x in range(6):
            if board[x, y] == player:
                counter += 1
            else:
                counter = 0
            if counter == 3:
                connect_three_counter += 1

    offsets = [-2, -1, 0, 1, 2, 3]
    for x in offsets:
        counter = 0
        temp_array = board.diagonal(x)
        for y in range(len(temp_array)):
            if temp_array[y] == player:
                counter += 1
            else:
                counter = 0
            if counter == 3:
                connect_three_counter += 1

    for x in offsets:
        counter = 0
        temp_array = np.fliplr(board).diagonal(x)
        for y in range(len(temp_array)):
            if temp_array[y] == player:
                counter += 1
            else:
                counter = 0
            if counter == 3:
                connect_three_counter += 1

    return connect_three_counter


def connected_two(board: np.ndarray, player: BoardPiece) -> int:
    """Counts how many two adjacent pieces equal to 'player' arranged in either direction on the given board

       Parameters
       ----------
       board : np.ndarray
           Current board
       player : BoardPiece
           Player whose turn it is

       Returns
       -------
       int
           Number of two adjacent pieces equal to 'player' arranged in either direction
       """
    connect_two_counter = 0

    for x in range(6):
        counter = 0
        for y in range(7):
            if board[x, y] == player:
                counter += 1
            else:
                counter = 0
            if counter == 2:
                connect_two_counter += 1

    for y in range(7):
        counter = 0
        for x in range(6):
            if board[x, y] == player:
                counter += 1
            else:
                counter = 0
            if counter == 2:
                connect_two_counter += 1

    offsets = [-2, -1, 0, 1, 2, 3]
    for x in offsets:
        counter = 0
        temp_array = board.diagonal(x)
        for y in range(len(temp_array)):
            if temp_array[y] == player:
                counter += 1
            else:
                counter = 0
            if counter == 2:
                connect_two_counter += 1

    for x in offsets:
        counter = 0
        temp_array = np.fliplr(board).diagonal(x)
        for y in range(len(temp_array)):
            if temp_array[y] == player:
                counter += 1
            else:
                counter = 0
            if counter == 2:
                connect_two_counter += 1

    return connect_two_counter


def other_player(player: BoardPiece):
    if player == PLAYER1:
        return PLAYER2
    elif player == PLAYER2:
        return PLAYER1


def map_board_to_player_one(board: np.ndarray) -> np.ndarray:
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
    for x in range(6):
        for y in range(7):
            if board[x, y] == 0:
                board[x, y] = 0
            elif board[x, y] == 1:
                board[x, y] = 2
            elif board[x, y] == 2:
                board[x, y] = 1

    return board