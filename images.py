import pygame


def load_image(path):
    return pygame.image.load(path)


def slice_image(image, rows, cols):
    tiles = [[None for _ in range(cols)] for _ in range(rows)]
    tile_width = image.get_width() // cols
    tile_height = image.get_height() // rows
    for row in range(rows):
        for col in range(cols):
            tiles[row][col] = image.subsurface(
                (col * tile_width, row * tile_height, tile_width, tile_height)
            )
    return tiles


def draw_image(screen, image, x, y):
    screen.blit(image, (x, y))
