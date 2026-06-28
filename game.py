from board import create_solved_board, is_solved, move, set_grid_size, shuffle_board


def ask_grid_size():
    while True:
        try:
            rows = int(input("Rows (n): "))
            cols = int(input("Columns (m): "))
        except ValueError:
            print("Please enter whole numbers.")
            continue

        if rows < 2 or cols < 2:
            print("Grid must be at least 2x2.")
            continue

        return rows, cols


def read_win_choice():
    import msvcrt

    while True:
        key = msvcrt.getch()

        if key in (b"n", b"N"):
            return "new"
        if key in (b"q", b"Q", b"\x03"):
            return "quit"


def run_game():
    rows, cols = ask_grid_size()
    set_grid_size(rows, cols)

    print(f"Sliding puzzle ({rows}x{cols})")
    print("Arrow keys to move. Press Q to quit.")

    while True:
        board = shuffle_board(create_solved_board())
        move_count = 0

        while True:
            print()
            for row in board:
                print(row)

            direction = read_arrow_key()
            if direction == "quit":
                print("Bye!")
                return

            new_board = move(board, direction)
            if new_board != board:
                move_count += 1
            board = new_board

            if is_solved(board):
                print()
                for row in board:
                    print(row)
                print(f"You solved it in {move_count} moves!")
                print("Press N for new puzzle, Q to quit.")
                break

        choice = read_win_choice()
        if choice == "quit":
            print("Bye!")
            break


def read_arrow_key():
    import msvcrt

    while True:
        key = msvcrt.getch()

        if key in (b"q", b"Q", b"\x03"):
            return "quit"

        if key in (b"\xe0", b"\x00"):
            arrow = msvcrt.getch()

            if arrow == b"H":
                return "up"
            if arrow == b"P":
                return "down"
            if arrow == b"K":
                return "left"
            if arrow == b"M":
                return "right"
