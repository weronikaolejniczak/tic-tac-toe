from sys import maxsize

function_calls = 0


# MOVE CLASS

class Move:
    def __init__(self, index, score):
        self.index = index
        self.score = score


# HELPER FUNCTIONS

# check if the board is full
def check_if_full(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                return False

    return True


def generate_possible_moves(board):
    empty_cells = []

    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                empty_cells.append([i, j])

    return empty_cells


# return True if there are available moves remaining on the board,
# return False if there are no moves left to play
def is_moves_left(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                return True

    return False


def find_best_move(board):
    global function_calls
    function_calls = 0
    best_value = -maxsize
    best_move = [None, None]

    # traverse all cells, evaluate minimax function for all empty cells and return the cell with optimal value
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                # make_move(board, i, j, -1)
                move_value, minimaxed_move = minimax(board, 0, True, -maxsize, +maxsize)
                # undo_move(board, i, j)

                if len(minimaxed_move) > 1:
                    if move_value > best_value:
                        best_move[0] = minimaxed_move[0]
                        best_move[1] = minimaxed_move[1]
                        best_value = move_value
                if len(minimaxed_move) == 0:
                    best_move[0] = i
                    best_move[1] = j

    print("The value of the best move is: {}\n".format(best_value))

    return best_move


def evaluate(board, depth):
    # check ROWS for victory
    for row in range(3):
        if board[row][0] == board[row][1] and board[row][1] == board[row][2] and board[row][2] == 1:
            return 10 - depth
        elif board[row][0] == board[row][1] and board[row][1] == board[row][2] and board[row][2] == -1:
            return -10 + depth

    # check COLUMNS for victory
    for col in range(3):
        if board[0][col] == board[1][col] and board[1][col] == board[2][col] and board[2][col] == 1:
            return 10 - depth
        elif board[0][col] == board[1][col] and board[1][col] == board[2][col] and board[2][col] == -1:
            return -10 + depth

    # check DIAGONALS for victory
    # anti-diagonal win
    if board[0][0] == board[1][1] == board[2][2] == 1:
        return 10 - depth
    elif board[0][0] == board[1][1] == board[2][2] == -1:
        return -10 + depth

    # diagonal win
    if board[0][2] == board[1][1] == board[2][0] == 1:
        return 10 - depth
    elif board[0][2] == board[1][1] == board[2][0] == -1:
        return -10 + depth

    return 0


# rewrite value at board index with 0
def undo_move(board, row, column):
    board[row][column] = 0


# rewrite value at board index with player sign
def make_move(board, row, column, player):
    board[row][column] = player


# MINI-MAX ALGORITHM


def minimax(board, depth, maximizing_player, alpha, beta):
    global function_calls
    function_calls += 1

    score = evaluate(board, depth)
    # print("[{} FC] Score {} at depth {}".format(function_calls, score, depth))

    moves = []

    # print the board at each function call
    # for row in board:
    #    print(row)

    # maximizer won
    if score > 0:
        # print("MAXIMIZER WON!")
        return score, moves

    # minimizer won
    if score < 0:
        # print("MINIMIZER WON!")
        return score, moves

    # there are no more moves and no winner, it is a draw
    if not is_moves_left(board) and check_if_full(board):
        # print("NOBODY WON!")
        return 0, moves

    # if it's maximizer's turn...
    if maximizing_player:
        # print("maximizer's turn at depth {}\n".format(depth))
        best_value = -maxsize

        # traverse all the cells
        for i in range(3):
            for j in range(3):
                # if cell is empty...
                if board[i][j] == 0:
                    # make the move
                    make_move(board, i, j, 1)
                    # value
                    value = minimax(board, depth + 1, not maximizing_player, alpha, beta)[0]
                    # undo the move
                    undo_move(board, i, j)
                    # call minimax recursively and choose maximum value
                    best_value = max(best_value, value)
                    # alpha
                    alpha = max(alpha, best_value)
                    if beta <= alpha:
                        break
                    # save the move and its score
                    if best_value > 0:
                        moves.append(Move([i, j], best_value))
                        # print("\n")
                        # print("Index: {}, Score: {}\n".format(moves[0].index, moves[0].score))
                        # print("--------------------------\n\n")
                        return best_value, moves[0].index

        return best_value, moves

    # if it's minimizer's turn...
    else:
        # print("minimizer's turn at depth {}\n".format(depth))
        best_value = +maxsize

        # traverse all the cells
        for i in range(3):
            for j in range(3):
                # if cell is empty...
                if board[i][j] == 0:
                    # make the move
                    make_move(board, i, j, -1)
                    # value
                    value = minimax(board, depth + 1, not maximizing_player, alpha, beta)[0]
                    # undo the move
                    undo_move(board, i, j)
                    # call minimax recursively and choose minimum value
                    best_value = min(best_value, value)
                    # beta
                    beta = min(beta, best_value)
                    if beta <= alpha:
                        break
                    # save the move and its score
                    if best_value < 0:
                        moves.append(Move([i, j], best_value))
                        # print("\n")
                        # print("Index: {}, Score: {}\n".format(moves[0].index, moves[0].score))
                        # print("--------------------------\n\n")
                        return best_value, moves[0].index

        return best_value, moves


# PRINTING to console


def rename_signs(pos):
    sign = " "

    if pos == -1:
        sign = "O"
    elif pos == 1:
        sign = "X"

    return sign


def print_board(board):
    # "board" is a 2-dimensional list of integers representing the board
    print(' ' + rename_signs(board[0][0]) + ' | ' + rename_signs(board[0][1]) + ' | ' + rename_signs(board[0][2]))
    print('-----------')
    print(' ' + rename_signs(board[1][0]) + ' | ' + rename_signs(board[1][1]) + ' | ' + rename_signs(board[1][2]))
    print('-----------')
    print(' ' + rename_signs(board[2][0]) + ' | ' + rename_signs(board[2][1]) + ' | ' + rename_signs(board[2][2]))


def main():
    """
    BOARD = [
                [1, -1, 1],
                [-1, -1, 1],
                [0, 0, 0],
            ]

    # correct: [1, 1]
    BOARD = [
                [1, 0, -1],
                [0, 0, 0],
                [-1, 0, 1],
            ]

    # correct: [1, 0], also [2, 1]
    BOARD = [
                [1, -1, -1],
                [0, 0, -1],
                [1, 0, 1],
            ]

    # partially correct: knows to interrupt MINIMIZER, but doesn't pick win [2][1]
    BOARD = [
                [1, 0, -1],
                [-1, 0, -1],
                [1, 0, 1],
            ]

    # correct: [1, 0]
    BOARD = [
                [1, -1, -1],
                [0, 0, -1],
                [1, -1, 1],
            ]

    # correct: [1, 1]
    BOARD = [
                [1, -1, -1],
                [0, 0, -1],
                [0, -1, 1],
            ]

    # correct: [1, 1]
    BOARD = [
                [-1, -1, 1],
                [0, 0, -1],
                [1, 0, 0],
            ]

    # IMPORTANT!!!
    # correct: [0, 2]
    BOARD = [
                [1, 1, 0],
                [0, -1, 0],
                [-1, 0, 0],
            ]

    # NOT CORRECT! DOESN'T PICK [0, 2], MINIMIZER WINS
    BOARD = [
                [1, 0, 0],
                [0, -1, 0],
                [-1, 0, 0],
            ]

    # but if AI goes first CORRECT:
    BOARD = [
                [1, 0, 0],
                [0, -1, 0],
                [-1, 0, 1],
            ]

    best_move = find_best_move(BOARD)
    print(best_move)
    """


main()
