import random

from agents.game_utils import *
def generate_move_random(
    board: np.ndarray, player: BoardPiece, saved_state: Optional[SavedState]
) -> tuple[PlayerAction, Optional[SavedState]]:
    # Choose a valid, non-full column randomly and return it as `action`
    list= []
    for i in range(7):
        if(board[5][i]==NO_PLAYER):
            list.append(i)
    action =random.choice(list)
    return action, saved_state