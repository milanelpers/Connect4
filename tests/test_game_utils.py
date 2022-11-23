import pytest

from agents.game_utils import *
import numpy as np


def test_ini_gamestate():

    assert type(initialize_game_state()) is np.ndarray


def test_print_pretty():
    board = np.full((6, 7), NO_PLAYER, dtype=BoardPiece)

    print(pretty_print_board(board))
    assert type(pretty_print_board(board)) is str


def test_string_to_board():
    board = np.full((6, 7), NO_PLAYER, dtype=BoardPiece)

    board = pretty_print_board(board)
    assert type(string_to_board(board)) is np.ndarray
    assert type(string_to_board(board)[0][0]) is BoardPiece


def test_player_action_wrong():
    board = np.full((6, 7), PLAYER1, dtype=BoardPiece)

    with pytest.raises(ValueError):
        apply_player_action(board, 1, PLAYER2)


def test_player_action_correct():
    board = np.full((6, 7), NO_PLAYER, dtype=BoardPiece)
    board_after = copy.deepcopy(board)
    board_after[0][0] = PLAYER2
    assert apply_player_action(board, 0, PLAYER2).all() == board_after.all()


def test_connected_four():
    board = np.full((6, 7), NO_PLAYER, dtype=BoardPiece)
    board1 = np.full((6, 7), PLAYER1, dtype=BoardPiece)

    assert connected_four(board, PLAYER1) is False
    assert connected_four(board1, PLAYER1) is True


def test_game_over():
    board = np.full((6, 7), NO_PLAYER, dtype=BoardPiece)
    assert connected_four(board, PLAYER1) is False
    board2 = np.full((6, 7), PLAYER1, dtype=BoardPiece)
    assert connected_four(board2, PLAYER2) is False
    board3 = np.full((6, 7), PLAYER1, dtype=BoardPiece)
    assert connected_four(board3, PLAYER1) is True
