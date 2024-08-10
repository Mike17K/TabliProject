import pygame
import random
from UI.constants import (
    screen_height,
    screen_width,
    background_image,
    whitePiece,
    blackPiece,
    PIECE_WIDTH,
    diceImageDict,
)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple Pygame Window")

ydiceoffset1 = 0
ydiceoffset2 = 0
xdieoffset1 = 0
xdieoffset2 = 0
prevdice1 = 0
prevdice2 = 0


def DrawState(state):
    global ydiceoffset1, ydiceoffset2, prevdice1, prevdice2, xdieoffset1, xdieoffset2
    # Draw the background image
    screen.blit(background_image, (0, 0))

    state.board.draw(state.holding_piece_previews_index)

    # Draw the dices
    dice1 = state.board.dice1
    dice2 = state.board.dice2
    if dice1 is not None and dice2 is not None:
        if dice1 != prevdice1 or dice2 != prevdice2:
            ydiceoffset1 = random.randint(-10, 10)
            ydiceoffset2 = random.randint(-10, 10)
            xdieoffset1 = random.randint(-10, 10)
            xdieoffset2 = random.randint(-10, 10)
            prevdice1 = dice1
            prevdice2 = dice2
        if state.board.is_white_turn:
            screen.blit(
                diceImageDict[dice1],
                (
                    screen_width * 3 / 4 - xdieoffset1 - 20,
                    screen_height / 2 - ydiceoffset1,
                ),
            )
            screen.blit(
                diceImageDict[dice2],
                (
                    screen_width * 3 / 4 - xdieoffset2 + 20,
                    screen_height / 2 - ydiceoffset2,
                ),
            )
        else:
            screen.blit(
                diceImageDict[dice1],
                (screen_width / 4 - xdieoffset1 - 20, screen_height / 2 - ydiceoffset1),
            )
            screen.blit(
                diceImageDict[dice2],
                (screen_width / 4 + xdieoffset2 + 20, screen_height / 2 - ydiceoffset2),
            )

    # Draw the captured pieces
    captured_black_index = 0
    captured_white_index = 0
    tmp = state.board.captured_pieces[::]
    (
        tmp.remove(state.holding_piece)
        if state.holding_piece in tmp and state.holding_piece_previews_index in [24, 25]
        else None
    )
    for i in range(len(tmp)):
        if tmp[i] > 0:
            screen.blit(
                whitePiece,
                [
                    screen_width / 2 - PIECE_WIDTH / 2,
                    screen_height / 2
                    + captured_white_index * PIECE_WIDTH
                    + PIECE_WIDTH / 2,
                ],
            )
            captured_white_index += 1
        else:
            screen.blit(
                blackPiece,
                [
                    screen_width / 2 - PIECE_WIDTH / 2,
                    screen_height / 2
                    - captured_black_index * PIECE_WIDTH
                    - 3 * PIECE_WIDTH / 2,
                ],
            )
            captured_black_index += 1

    # Draw the holding piece
    if state.holding_piece is not None:
        x, y = pygame.mouse.get_pos()
        if state.holding_piece > 0:
            screen.blit(
                whitePiece,
                (x - PIECE_WIDTH / 2, y - PIECE_WIDTH / 2),
            )
        else:
            screen.blit(
                blackPiece,
                (x - PIECE_WIDTH / 2, y - PIECE_WIDTH / 2),
            )
