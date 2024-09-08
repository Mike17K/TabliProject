import pygame
from UI.constants import (
    screen_height,
    PIECE_WIDTH,
    SECTION_TOP_LEFT,
    SECTION_TOP_RIGHT,
    OFFSETS,
)
from UI.state import UIState


def get_board_index(x, y) -> int:
    # if the click is on the middle section
    if SECTION_TOP_LEFT[0] + 6 * PIECE_WIDTH < x < SECTION_TOP_RIGHT[0]:
        if y < screen_height / 2:
            return 25
        if y > screen_height / 2:
            return 24
    for i in range(6 * 4):
        if OFFSETS[i][0] < x < OFFSETS[i][0] + PIECE_WIDTH:
            if y < screen_height / 2 and i < 12:
                return i
            if y > screen_height / 2 and i >= 12:
                return i
    return None



def handleEvents(event, state: UIState):
    board = state.get_board()
    if event.type == pygame.MOUSEBUTTONDOWN:
        clicked_index = get_board_index(*pygame.mouse.get_pos())
        # if there is not piece on the clicked index do nothing
        if (
            state.holding_piece is None
            and clicked_index in [24, 25]
            and (
                1 in board.captured_pieces
                if clicked_index == 24
                else -1 in board.captured_pieces
            )
            and board.is_white_turn == (clicked_index == 24)
        ):
            state.holding_piece = 1 if clicked_index == 24 else -1
            state.holding_piece_previews_index = clicked_index
        if (
            clicked_index is not None
            and 0 <= clicked_index < 24
            and board.board[clicked_index] != 0
            and board.is_white_turn == (board.board[clicked_index] > 0)
        ):
            state.holding_piece = 1 if board.board[clicked_index] > 0 else -1
            state.holding_piece_previews_index = clicked_index
    if event.type == pygame.MOUSEBUTTONUP:
        if state.holding_piece is not None:
            clicked_index = get_board_index(*pygame.mouse.get_pos())
            board.move(state.holding_piece_previews_index, clicked_index)
        state.holding_piece = None
        state.holding_piece_previews_index = None
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            board.RollDices()
        if event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
            board.Undo()

        if event.key == pygame.K_c:
            best_moves, score = board.GetBestMoveForDices()
            print("Best move for dices: ", best_moves , " with score: ", score)
            # make the moves
            for move in best_moves:
                board = board.move(move[0], move[1], commit=True)




        # moves only for latest part of the game
        if event.key == pygame.K_1:
            board.move(23 if board.is_white_turn else 0, 26 if board.is_white_turn else 27)
        if event.key == pygame.K_2:
            board.move(22 if board.is_white_turn else 1, 26 if board.is_white_turn else 27)
        if event.key == pygame.K_3:
            board.move(21 if board.is_white_turn else 2, 26 if board.is_white_turn else 27)
        if event.key == pygame.K_4:
            board.move(20 if board.is_white_turn else 3, 26 if board.is_white_turn else 27)
        if event.key == pygame.K_5:
            board.move(19 if board.is_white_turn else 4, 26 if board.is_white_turn else 27)
        if event.key == pygame.K_6:
            board.move(18 if board.is_white_turn else 5, 26 if board.is_white_turn else 27)