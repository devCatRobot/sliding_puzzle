import sys

import pygame

from board import COLS, EMPTY, ROWS, is_solved, move
from effects import create_firework, draw_fireworks, tick_fireworks

DEBUG_SHUFFLE_MOVES = 5
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

TILE_COLOR = (70, 130, 180)
EMPTY_COLOR = (40, 44, 52)
TEXT_COLOR = (255, 255, 255)
BORDER_COLOR = (30, 30, 30)


def draw_board(screen, board):
    tile_width = WINDOW_WIDTH // COLS
    tile_height = WINDOW_HEIGHT // ROWS
    font_size = max(16, min(tile_width, tile_height) // 2)
    font = pygame.font.SysFont(None, font_size)

    for row in range(ROWS):
        for col in range(COLS):
            value = board[row][col]
            x = col * tile_width
            y = row * tile_height
            rect = pygame.Rect(x, y, tile_width, tile_height)

            if value == EMPTY:
                pygame.draw.rect(screen, EMPTY_COLOR, rect)
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


def draw_win_message(screen, move_count):
    font = pygame.font.SysFont(None, 32)
    message = font.render(f"Solved in {move_count} moves!", True, (255, 220, 100))
    message_rect = message.get_rect(center=(WINDOW_WIDTH // 2, 30))
    screen.blit(message, message_rect)


def handle_keydown(event, board, solved, move_count):
    if event.key == pygame.K_q:
        return False, board, solved, move_count, None

    if solved:
        return True, board, solved, move_count, None

    direction = key_to_direction(event.key)
    if direction is None:
        return True, board, solved, move_count, None

    new_board = move(board, direction)
    new_move_count = move_count
    if new_board != board:
        new_move_count += 1

    new_solved = solved
    fireworks = None
    if is_solved(new_board):
        new_solved = True
        fireworks = create_firework(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

    return True, new_board, new_solved, new_move_count, fireworks


def draw_frame(screen, board, solved, fireworks, move_count):
    screen.fill(EMPTY_COLOR)
    draw_board(screen, board)

    if solved:
        draw_fireworks(screen, fireworks)
        draw_win_message(screen, move_count)


def run_gui(board):
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
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
                running, board, solved, move_count, new_fireworks = handle_keydown(
                    event, board, solved, move_count
                )
                if new_fireworks is not None:
                    fireworks = new_fireworks

        if solved:
            fireworks, win_frames = tick_fireworks(
                fireworks, win_frames, WINDOW_WIDTH, WINDOW_HEIGHT
            )

        draw_frame(screen, board, solved, fireworks, move_count)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    from board import create_solved_board, set_grid_size, shuffle_board

    debug = "debug" in sys.argv
    set_grid_size(4, 4)
    shuffle_moves = DEBUG_SHUFFLE_MOVES if debug else None
    board = shuffle_board(create_solved_board(), shuffle_moves)
    if debug:
        print(f"Debug mode: shuffled {DEBUG_SHUFFLE_MOVES} times only.")
    run_gui(board)
