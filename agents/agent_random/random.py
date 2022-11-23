import random

from agents.game_utils import *

"""
A random action from all possible ones is returned.
"""


def generate_move_random(
    board: np.ndarray, player: BoardPiece, saved_state: Optional[SavedState]
) -> tuple[PlayerAction, Optional[SavedState]]:
    # Choose a valid, non-full column randomly and return it as `action`
    mlist = []
    for i in range(7):
        if board[5][i] == NO_PLAYER:
            mlist.append(i)
    action = random.choice(mlist)
    return action, saved_state
