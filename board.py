import random

ROWS = 4
COLS = 4
EMPTY = 0


def set_grid_size(rows, cols):
    global ROWS, COLS
    ROWS = rows
    COLS = cols


def create_solved_board():
    board = []
    number = 1

    for row in range(ROWS):
        row_values = []
        for col in range(COLS):
            if row == ROWS - 1 and col == COLS - 1:
                row_values.append(EMPTY)
            else:
                row_values.append(number)
                number += 1
        board.append(row_values)

    return board


def find_empty(board):
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == EMPTY:
                return row, col

    raise ValueError("No empty cell found on the board.")


def move(board, direction):
    empty_row, empty_col = find_empty(board)

    if direction == "right":
        tile_row = empty_row
        tile_col = empty_col - 1
    elif direction == "left":
        tile_row = empty_row
        tile_col = empty_col + 1
    elif direction == "up":
        tile_row = empty_row + 1
        tile_col = empty_col
    elif direction == "down":
        tile_row = empty_row - 1
        tile_col = empty_col
    else:
        return board

    if tile_row < 0 or tile_row >= ROWS or tile_col < 0 or tile_col >= COLS:
        return board

    new_board = [list(row_values) for row_values in board]
    new_board[empty_row][empty_col] = new_board[tile_row][tile_col]
    new_board[tile_row][tile_col] = EMPTY

    return new_board


def shuffle_board(board, move_count=None):
    if move_count is None:
        move_count = 25 * ROWS * COLS // 2
    directions = ["up", "down", "left", "right"]

    for _ in range(move_count):
        direction = random.choice(directions)
        board = move(board, direction)

    return board


def is_solved(board):
    return board == create_solved_board()
