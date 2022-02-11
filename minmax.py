import const
from main import available_square


# This function returns true if there are moves
# remaining on the board. It returns false if
# there are no moves left to play.

def is_moves_left(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == const.EMPTY:
                return True
    return False


def score_evaluate(board):
    # check vertical lines
    for col in range(const.BOARD_COLS):
        if board[0][col] != const.EMPTY and board[0][col] == board[1][col] and board[1][col] == board[2][col]:
            return const.POSSIBLE_SCORES[int(board[0][col])]

    # check horizontal lines
    for row in range(const.BOARD_ROWS):
        if board[row][0] != const.EMPTY and board[row][0] == board[row][1] and board[row][1] == board[row][2]:
            return const.POSSIBLE_SCORES[int(board[row][0])]

    # check asc diagonal
    if board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[0][2] != const.EMPTY:
        return const.POSSIBLE_SCORES[int(board[1][1])]

    # check DESC diagonal
    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] != const.EMPTY:
        return const.POSSIBLE_SCORES[int(board[1][1])]

    # no player does not win yet
    return 0


def ai_result(board):
    """
        :param board: the matrix of our game
        :return: the index of square that the AI ('O') thinks is the best to mark
    """
    best_score = -const.INFINITY
    best_index = (-1, -1)
    for row in range(const.BOARD_ROWS):
        for col in range(const.BOARD_COLS):
            if available_square(board, row, col):
                board[row][col] = const.AI_PLAYER
                score_per_turn = min_max(board, 0, False)
                board[row][col] = const.EMPTY
                if score_per_turn > best_score:
                    best_score = score_per_turn
                    best_index = (row, col)
    return best_index


def min_max(matrix, depth, is_maximize):
    outcome = score_evaluate(matrix)
    # If Maximizer has won the game return his/her
    # evaluated score. If Minimizer has won the game return his/her
    # evaluated score
    if outcome == 10 or outcome == -10:
        return outcome

    # If there are no more moves and no winner then
    # it is a tie
    if not is_moves_left(matrix):
        return const.POSSIBLE_SCORES[0]

    if is_maximize:
        max_score = -const.INFINITY
        for row in range(const.BOARD_ROWS):
            for col in range(const.BOARD_COLS):
                if available_square(matrix, row, col):
                    matrix[row][col] = const.AI_PLAYER
                    score = min_max(matrix, depth + 1, not is_maximize)
                    matrix[row][col] = const.EMPTY
                    max_score = max(score, max_score)
        return max_score
    else:
        # minimize score
        min_score = const.INFINITY
        for row in range(const.BOARD_ROWS):
            for col in range(const.BOARD_COLS):
                if available_square(matrix, row, col):
                    matrix[row][col] = const.HUMAN
                    score = min_max(matrix, depth + 1, not is_maximize)
                    matrix[row][col] = const.EMPTY
                    min_score = min(score, min_score)
        return min_score
