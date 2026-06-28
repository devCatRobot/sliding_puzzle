from board import create_solved_board, move

def run_game():
    board = create_solved_board()

    print("Sliding puzzle (4x4)")
    print("Arrow keys to move. Press Q to quit.")

    while True:
        print()
        for row in board:
            print(row)

        direction = read_arrow_key()
        if direction == "quit":
            print("Bye!")
            break

        board = move(board, direction)

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