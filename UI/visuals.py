import pygame
import random
from UI.constants import (
    screen_height,
    screen_width,
    background_image,
    whitePiece,
    blackPiece,
    PIECE_WIDTH,
    OFFSETS,
    diceImageDict,
)
from UI.state import UIState
from Compute.board import Board
from Compute.types import Color

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple Pygame Window")

ydiceoffset1 = 0
ydiceoffset2 = 0
xdieoffset1 = 0
xdieoffset2 = 0
prevdice1 = 0
prevdice2 = 0


def DrawState(state: UIState):
    global ydiceoffset1, ydiceoffset2, prevdice1, prevdice2, xdieoffset1, xdieoffset2
    # Draw the background image
    screen.blit(background_image, (0, 0))

    DrawBoard(board=state.get_board(), holding_index=state.holding_piece_previews_index)

    # Draw the dices
    dice1 = None if state.get_board().dices[0] == -1 else state.get_board().dices[0]
    dice2 = None if state.get_board().dices[1] == -1 else state.get_board().dices[1]
    if dice1 is not None and dice2 is not None:
        if dice1 != prevdice1 or dice2 != prevdice2:
            ydiceoffset1 = random.randint(-10, 10)
            ydiceoffset2 = random.randint(-10, 10)
            xdieoffset1 = random.randint(-10, 10)
            xdieoffset2 = random.randint(-10, 10)
            prevdice1 = dice1
            prevdice2 = dice2
        if state.get_board().is_white_turn:
            screen.blit(
                diceImageDict[dice1],
                (
                    screen_width * 3 / 4 - xdieoffset1 - 30,
                    screen_height / 2 - ydiceoffset1,
                ),
            )
            screen.blit(
                diceImageDict[dice2],
                (
                    screen_width * 3 / 4 - xdieoffset2 + 30,
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
    tmp = state.get_board().cuptured.copy()
    if state.holding_piece in tmp and state.holding_piece_previews_index in [24, 25]:
        tmp[
            Color.WHITE if state.holding_piece_previews_index == 24 else Color.BLACK
        ] -= 1

    for i in range(tmp[Color.WHITE]):
        screen.blit(
            whitePiece,
            [
                screen_width / 2 - PIECE_WIDTH / 2,
                screen_height / 2 + i * PIECE_WIDTH + PIECE_WIDTH / 2,
            ],
        )
    for i in range(tmp[Color.BLACK]):
        screen.blit(
            blackPiece,
            [
                screen_width / 2 - PIECE_WIDTH / 2,
                screen_height / 2 - i * PIECE_WIDTH - 3 * PIECE_WIDTH / 2,
            ],
        )

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


def DrawBoard(board: Board, holding_index=None):
    for board_index in range(6 * 4):
        if board.board[board_index] == 0:
            continue
        reduce = (
            (1 if board.board[holding_index] > 0 else -1)
            if holding_index == board_index and board.board[holding_index] != 0
            else 0
        )

        x, y = OFFSETS[board_index]
        if board.board[board_index] > 0:
            for white_piece_index in range(board.board[board_index] - reduce):
                if board_index > 11:
                    screen.blit(
                        whitePiece,
                        (x, y - white_piece_index * PIECE_WIDTH),
                    )
                else:
                    screen.blit(
                        whitePiece,
                        (x, y + white_piece_index * PIECE_WIDTH),
                    )
        else:
            for black_piece_index in range(-board.board[board_index] + reduce):
                if board_index > 11:
                    screen.blit(
                        blackPiece,
                        (x, y - black_piece_index * PIECE_WIDTH),
                    )
                else:
                    screen.blit(
                        blackPiece,
                        (x, y + black_piece_index * PIECE_WIDTH),
                    )

    available_moves = list(board.available_moves)
    for i in range(len(available_moves)):
        from_index, to_index = available_moves[i]
        if from_index == 24:  # white captured pieces
            pygame.draw.rect(
                screen,
                (255, 0, 0),
                (
                    screen_width / 2 - PIECE_WIDTH / 2,
                    screen_height / 2 + 0 * PIECE_WIDTH + PIECE_WIDTH / 2,
                    PIECE_WIDTH,
                    PIECE_WIDTH,
                ),
                3,
            )
        elif from_index == 25:  # black captured pieces
            pygame.draw.rect(
                screen,
                (0, 255, 0),
                (
                    screen_width / 2 - PIECE_WIDTH / 2,
                    screen_height / 2 - 0 * PIECE_WIDTH - 3 * PIECE_WIDTH / 2,
                    PIECE_WIDTH,
                    PIECE_WIDTH,
                ),
                3,
            )
        else:
            # normal pieces
            pygame.draw.rect(
                screen,
                (255, 0, 0),
                (
                    OFFSETS[from_index][0],
                    OFFSETS[from_index][1],
                    PIECE_WIDTH,
                    PIECE_WIDTH,
                ),
                3,
            )
        if to_index < 24:
            pygame.draw.rect(
                screen,
                (0, 255, 0),
                (OFFSETS[to_index][0], OFFSETS[to_index][1], PIECE_WIDTH, PIECE_WIDTH),
                3,
            )
