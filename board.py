SIZE = 4
EMPTY = 0


def create_solved_board():
    board = []
    number = 1

    for row in range(SIZE):
        row_values = []
        for col in range(SIZE):
            if row == SIZE - 1 and col == SIZE - 1:
                row_values.append(EMPTY)
            else:
                row_values.append(number)
                number += 1
        board.append(row_values)

    return board


def find_empty(board):
    for row in range(SIZE):
        for col in range(SIZE):
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

    if tile_row < 0 or tile_row >= SIZE or tile_col < 0 or tile_col >= SIZE:
        return board

    new_board = [list(row_values) for row_values in board]
    new_board[empty_row][empty_col] = new_board[tile_row][tile_col]
    new_board[tile_row][tile_col] = EMPTY

    return new_board