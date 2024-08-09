import pygame

scale = 0.5

screen_width = 1024 * scale
screen_height = 1024 * scale

# Load images
background_image = pygame.image.load("images/tabli.png")
whitePiece = pygame.image.load("images/white.png")
blackPiece = pygame.image.load("images/black.png")

# constants
SECTION_TOP_LEFT = [16 * scale, 16 * scale]  # x,y
SECTION_TOP_RIGHT = [534 * scale, 16 * scale]  # x,y
SECTION_BOTTOM_LEFT = [16 * scale, 1008 * scale]  # x,y
SECTION_BOTTOM_RIGHT = [534 * scale, 1008 * scale]  # x,y

PIECE_WIDTH = 78.76 * scale

OFFSETS = (
    [[SECTION_TOP_LEFT[0] + PIECE_WIDTH * i, SECTION_TOP_LEFT[1]] for i in range(6)]
    + [[SECTION_TOP_RIGHT[0] + PIECE_WIDTH * i, SECTION_TOP_RIGHT[1]] for i in range(6)]
    + [
        [
            SECTION_BOTTOM_RIGHT[0] + PIECE_WIDTH * i,
            SECTION_BOTTOM_RIGHT[1] - PIECE_WIDTH,
        ]
        for i in range(6)
    ][::-1]
    + [
        [SECTION_BOTTOM_LEFT[0] + PIECE_WIDTH * i, SECTION_BOTTOM_LEFT[1] - PIECE_WIDTH]
        for i in range(6)
    ][::-1]
)
