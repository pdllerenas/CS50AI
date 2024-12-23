"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # return X if sum(1 if col == X else (-1 if col == O else 0) for row in board for col in row) == 0 else O
    return X if sum(1 if board[i][j] == EMPTY else 0 for i in range(3) for j in range(3)) % 2 == 1 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return set((i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY)


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] != EMPTY:
        raise Exception("Invalid move")
    cp = copy.deepcopy(board)
    cp[action[0]][action[1]] = player(board)
    return cp


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(len(board)):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[2][0] == board[1][1] == board[0][2] != EMPTY:
        return board[2][0]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return not any(EMPTY in row for row in board) or winner(board) is not None


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    return 1 if winner(board) == X else -1 if winner(board) == O else 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    if player(board) == X:
        return max(actions(board), key=lambda action: min_value(result(board, action)))
        return max_value(board)[1]
    else:
        return min(actions(board), key=lambda action: max_value(result(board, action)))
        return min_value(board)[1]

def max_value(board, alpha = float("-inf"), beta = float("inf")):
    """
    Calculates the optmial move for the maximizer
    """
    if terminal(board):
        return utility(board)
    v = float("-inf")
    for action in actions(board):
        value = min_value(result(board, action), alpha, beta)
        v = max(v, value)
        alpha = max(alpha, v)
        if beta <= alpha:
            break
    return v

def min_value(board, alpha = float("-inf"), beta = float("inf")):
    """
    Calculates the optmial move for the minimizer
    """
    if terminal(board):
        return utility(board)
    v = float("inf")
    for action in actions(board):
        value = max_value(result(board, action), alpha, beta)
        v = min(v, value)
        beta = min(beta, v)
        if beta <= alpha:
            break
        
    return v