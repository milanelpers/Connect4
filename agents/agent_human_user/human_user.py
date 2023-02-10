import numpy as np

from agents.game_utils import BoardPiece, PlayerAction, SavedState, NO_PLAYER, INDEX_HIGHEST_ROW
from typing import Optional, Callable


def user_move(board: tuple,
              _player: BoardPiece,
              saved_state: Optional[SavedState]) -> tuple[PlayerAction, SavedState]:
    is_valid_move = False
    while not is_valid_move:
        input_move_string = query_user(input)
        try:
            is_valid_move = handle_illegal_moves(board, input_move_string)
        except TypeError:
            print('Not the right format, try an integer.')
        except IndexError:
            print('Selected integer is not in the range of possible columns (0 - 6).')
        except ValueError:
            print('Selected column is full.')
    input_move_integer = PlayerAction(input_move_string)
    return input_move_integer, saved_state


def query_user(prompt_function: Callable):
    usr_input = prompt_function("Column? ")
    return usr_input


def handle_illegal_moves(board: tuple, column: PlayerAction):
    try:
        column = PlayerAction(column)
    except:
        raise TypeError

    is_in_range = PlayerAction(0) <= column <= PlayerAction(6)
    if not is_in_range:
        raise IndexError

    mask = board[0] | board[1]
    column0full = 0b0000000_0000000_0000000_0000000_0000000_0000000_0100000
    column1full = 0b0000000_0000000_0000000_0000000_0000000_0100000_0000000
    column2full = 0b0000000_0000000_0000000_0000000_0100000_0000000_0000000
    column3full = 0b0000000_0000000_0000000_0100000_0000000_0000000_0000000
    column4full = 0b0000000_0000000_0100000_0000000_0000000_0000000_0000000
    column5full = 0b0000000_0100000_0000000_0000000_0000000_0000000_0000000
    column6full = 0b0100000_0000000_0000000_0000000_0000000_0000000_0000000
    columncheck = [column0full, column1full, column2full, column3full, column4full, column5full, column6full]
    is_open = mask & columncheck[column] == 0

    if not is_open:
        raise ValueError

    return True