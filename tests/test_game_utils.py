import copy

import pytest

from agents.game_utils import *
import numpy as np

type = np.int8
def test_board_exist():
    a = np.array([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]
                     ,[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]
                     ,[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
                     ,dtype=type)

    assert initialize_game_state().all() == a.all()

def test_sache():
    board = np.full((6, 7), NO_PLAYER, dtype=BoardPiece)
    board[0][0]= PLAYER1
    board[1][0] = PLAYER1
    board[2][0] = PLAYER1
    board[3][0] = PLAYER1
    board[4][0] = PLAYER1
    board[5][0] = PLAYER1

    a= pretty_print_board(board)
    a= string_to_board(a)

    assert a.all() == board.all()

def test_player_action_wrong():
    board = np.full((6, 7), PLAYER1, dtype=BoardPiece)

    with pytest.raises(ValueError):
        apply_player_action(board,1,PLAYER2)

def test_player_action_correct():
    board = np.full((6, 7), NO_PLAYER, dtype=BoardPiece)
    boardafter = copy.deepcopy(board)
    boardafter[0][0] = PLAYER2
    assert apply_player_action(board,1,PLAYER2).all() == boardafter.all()

def test_game_over():
    board = np.full((6, 7), NO_PLAYER, dtype=BoardPiece)
    assert connected_four(board,PLAYER1)==False
    board2 = np.full((6, 7), PLAYER1, dtype=BoardPiece)
    assert connected_four(board2,PLAYER2)==False
    board3 = np.full((6,7),PLAYER1,dtype=BoardPiece)
    assert connected_four(board3,PLAYER1)==True

def test_game_state():
    board = np.full((6, 7), NO_PLAYER, dtype=BoardPiece)
    assert check_end_state(board,PLAYER1) == GameState.STILL_PLAYING
    #test with board thats full but no winner
