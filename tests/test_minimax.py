import pytest

from agents.agent_minimax import *
import numpy as np


def test_minimax():
    board = np.full((6, 7), NO_PLAYER, dtype=BoardPiece)

    assert minimax(board, 0, -10000000, 10000000, PLAYER1, True) == (None, 0)


def test_possible_locations():
    board = np.full((6, 7), NO_PLAYER, dtype=BoardPiece)

    assert type(possible_locations(board)) is list

    assert len(possible_locations(board)) == 7


def test_is_leaf_node():
    board = np.full((6, 7), PLAYER1, dtype=BoardPiece)

    assert type(is_leaf_node(board)) == bool
    assert is_leaf_node(board) is True


def test_calculate_area():
    area = [PLAYER1,PLAYER2,PLAYER1,PLAYER2,NO_PLAYER]

    assert -1000 <= calculate_area(area,PLAYER1) <= 200


def test_calculate_heuristic():
    board = np.full((6, 7), PLAYER1, dtype=BoardPiece)

    assert type(calculate_heuristic(board,PLAYER1)) is int
    assert calculate_heuristic(board,PLAYER1) > 0
