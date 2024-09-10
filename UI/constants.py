import pygame

scale = 0.5

screen_width = 1024 * scale
screen_height = 1024 * scale

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


# Load images
background_image = pygame.transform.scale(
    pygame.image.load("images/tabli.png"), (int(screen_width), int(screen_height))
)
whitePiece = pygame.transform.scale(
    pygame.image.load("images/white.png"), (PIECE_WIDTH, PIECE_WIDTH)
)
blackPiece = pygame.transform.scale(
    pygame.image.load("images/black.png"), (PIECE_WIDTH, PIECE_WIDTH)
)

# load dice images
diceImageDict = {
    1: pygame.transform.scale(
        pygame.image.load("images/dice1.png"), (int(50 * scale), int(50 * scale))
    ),
    2: pygame.transform.scale(
        pygame.image.load("images/dice2.png"), (int(50 * scale), int(50 * scale))
    ),
    3: pygame.transform.scale(
        pygame.image.load("images/dice3.png"), (int(50 * scale), int(50 * scale))
    ),
    4: pygame.transform.scale(
        pygame.image.load("images/dice4.png"), (int(50 * scale), int(50 * scale))
    ),
    5: pygame.transform.scale(
        pygame.image.load("images/dice5.png"), (int(50 * scale), int(50 * scale))
    ),
    6: pygame.transform.scale(
        pygame.image.load("images/dice6.png"), (int(50 * scale), int(50 * scale))
    ),
}
