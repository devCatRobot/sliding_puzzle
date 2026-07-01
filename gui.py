import os
import sys

import pygame

import board
from board import EMPTY, is_solved, move
from effects import create_firework, draw_fireworks, tick_fireworks

DEBUG_SHUFFLE_MOVES = 5
DEFAULT_WINDOW_SIZE = 400
MIN_TILE_SIZE = 40

TILE_COLOR = (70, 130, 180)
EMPTY_COLOR = (40, 44, 52)
TEXT_COLOR = (255, 255, 255)
BORDER_COLOR = (30, 30, 30)


def draw_board(screen, puzzle, image_tiles=None, window_width=DEFAULT_WINDOW_SIZE, window_height=DEFAULT_WINDOW_SIZE):
    tile_width = window_width // board.COLS
    tile_height = window_height // board.ROWS
    font_size = max(16, min(tile_width, tile_height) // 2)
    font = pygame.font.SysFont(None, font_size)

    for row in range(board.ROWS):
        for col in range(board.COLS):
            value = puzzle[row][col]
            x = col * tile_width
            y = row * tile_height
            rect = pygame.Rect(x, y, tile_width, tile_height)

            if value == EMPTY:
                pygame.draw.rect(screen, EMPTY_COLOR, rect)
            elif image_tiles is not None:
                solved_row = (value - 1) // board.COLS
                solved_col = (value - 1) % board.COLS
                screen.blit(image_tiles[solved_row][solved_col], (x, y))
            else:
                pygame.draw.rect(screen, TILE_COLOR, rect)
                text = font.render(str(value), True, TEXT_COLOR)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

            pygame.draw.rect(screen, BORDER_COLOR, rect, 2)


def key_to_direction(key):
    if key == pygame.K_UP:
        return "up"
    if key == pygame.K_DOWN:
        return "down"
    if key == pygame.K_LEFT:
        return "left"
    if key == pygame.K_RIGHT:
        return "right"
    return None


def draw_win_message(screen, move_count, window_width):
    font = pygame.font.SysFont(None, 32)
    message = font.render(f"Solved in {move_count} moves!", True, (255, 220, 100))
    message_rect = message.get_rect(center=(window_width // 2, 30))
    screen.blit(message, message_rect)


def handle_keydown(event, puzzle, solved, move_count, window_width, window_height):
    if event.key == pygame.K_q:
        return False, puzzle, solved, move_count, None

    if solved:
        return True, puzzle, solved, move_count, None

    direction = key_to_direction(event.key)
    if direction is None:
        return True, puzzle, solved, move_count, None

    new_puzzle = move(puzzle, direction)
    new_move_count = move_count
    if new_puzzle != puzzle:
        new_move_count += 1

    new_solved = solved
    fireworks = None
    if is_solved(new_puzzle):
        new_solved = True
        fireworks = create_firework(window_width // 2, window_height // 2)

    return True, new_puzzle, new_solved, new_move_count, fireworks


def ask_image_path():
    while True:
        image_path = input("Image path (empty for numbers): ").strip()
        if image_path.startswith('"') and image_path.endswith('"'):
            image_path = image_path[1:-1]

        if not image_path:
            return None

        if os.path.isfile(image_path):
            return image_path

        print("File not found. Try again.")


def ask_grid_size_for_window(window_width, window_height):
    from game import ask_grid_size

    max_rows = window_height // MIN_TILE_SIZE
    max_cols = window_width // MIN_TILE_SIZE

    if max_rows < 2 or max_cols < 2:
        print(
            f"Window is {window_width}x{window_height}. "
            f"Need at least {MIN_TILE_SIZE * 2}x{MIN_TILE_SIZE * 2} for a 2x2 puzzle."
        )
        sys.exit(1)

    print(f"Max grid for this size: {max_rows} rows x {max_cols} columns.")

    while True:
        rows, cols = ask_grid_size()
        tile_width = window_width // cols
        tile_height = window_height // rows

        if tile_width >= MIN_TILE_SIZE and tile_height >= MIN_TILE_SIZE:
            return rows, cols

        print(
            f"Each tile would be {tile_width}x{tile_height} px. "
            f"Minimum tile size is {MIN_TILE_SIZE}x{MIN_TILE_SIZE} px."
        )
        print(f"Use at most {max_rows} rows and {max_cols} columns.")


def draw_frame(screen, puzzle, solved, fireworks, move_count, image_tiles, window_width, window_height):
    screen.fill(EMPTY_COLOR)
    draw_board(screen, puzzle, image_tiles, window_width, window_height)

    if solved:
        draw_fireworks(screen, fireworks)
        draw_win_message(screen, move_count, window_width)


def run_gui(puzzle, image_tiles=None, window_width=DEFAULT_WINDOW_SIZE, window_height=DEFAULT_WINDOW_SIZE):
    pygame.init()

    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Sliding Puzzle")

    clock = pygame.time.Clock()
    running = True
    move_count = 0
    solved = False
    fireworks = []
    win_frames = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                running, puzzle, solved, move_count, new_fireworks = handle_keydown(
                    event, puzzle, solved, move_count, window_width, window_height
                )
                if new_fireworks is not None:
                    fireworks = new_fireworks

        if solved:
            fireworks, win_frames = tick_fireworks(
                fireworks, win_frames, window_width, window_height
            )

        draw_frame(
            screen, puzzle, solved, fireworks, move_count, image_tiles, window_width, window_height
        )
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    from board import create_solved_board, set_grid_size, shuffle_board
    from game import ask_grid_size
    from images import load_image, slice_image

    debug = "debug" in sys.argv

    window_width = DEFAULT_WINDOW_SIZE
    window_height = DEFAULT_WINDOW_SIZE
    image_path = ask_image_path()
    image = None
    if image_path is not None:
        pygame.init()
        image = load_image(image_path)
        window_width = image.get_width()
        window_height = image.get_height()
        pygame.display.set_mode((window_width, window_height))

    rows, cols = ask_grid_size_for_window(window_width, window_height)
    set_grid_size(rows, cols)

    image_tiles = None
    if image is not None:
        image = image.convert()
        image_tiles = slice_image(image, board.ROWS, board.COLS)

    shuffle_moves = DEBUG_SHUFFLE_MOVES if debug else None
    puzzle = shuffle_board(create_solved_board(), shuffle_moves)
    if debug:
        print(f"Debug mode: shuffled {DEBUG_SHUFFLE_MOVES} times only.")
    run_gui(puzzle, image_tiles, window_width, window_height)
