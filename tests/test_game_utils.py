import pytest
from agents.game_utils import *
import numpy as np


def test_ini_gamestate():
    board1 = 0b0000000_0000000_0000000_0000000_0000010_0001100_0000001
    board2 = 0b0000000_0000000_0000000_0000000_0000000_0000000_0000000
    print(int.bit_count(board1))
    boardarray = np.full((6,7), PLAYER1,dtype=BoardPiece)
    #print(apply_player_action((board1,board2),0,PLAYER2))
    printerino = apply_player_action((board1,board2), 0, PLAYER2)[0]
    #print(format(int(printerino),'049b'))
    #print(connected_four((board1,board2),PLAYER1))
    #board = get_bitboard(boardarray)
    #print(type(board[0]))
    #print(format(board[0], '049b'))
    #print(bin((string_to_board(pretty_print_board((board1, board2)))[0])))

    """
    board2 = initialize_game_state()
    b = get_bitboard(board2,PLAYER1)
    a = get_bitboard(board, PLAYER1)
    print(board)
    print(a)
    print(f"{a[0]:b}")
    print(f"{position:b}")
    print(b)
    print(f"{b[1]:b}")
    """

def test_count3():
    board1 = 0b0000000_0000000_0000000_0000000_0000000_0000000_0000111
    board2 = 0b0000000_0000000_0000000_0000000_0000000_0000000_0000111
    print(board1==board2)
    """
    #print(f"{board1:049d}")
    print('\n')
    print(format(board1, '049b'))
    print(format(shiftboard, '049b'))
    print('#######################################')
    print(board1)
    print(format(board1, '049b'))
    print(format(board3, '049b'))
    #
    #assert evaluate3(board2, board1) == 2
    """
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
