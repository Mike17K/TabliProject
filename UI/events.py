import pygame
from UI.constants import (
    screen_height,
    PIECE_WIDTH,
    SECTION_TOP_LEFT,
    SECTION_TOP_RIGHT,
    OFFSETS,
)
from UI.state import UIState
from Compute.types import RemoveAction, RollDiceAction, MoveAction, PlaceAction, Color


def get_board_index(x, y) -> int:
    # if the click is on the middle section
    if SECTION_TOP_LEFT[0] + 6 * PIECE_WIDTH < x < SECTION_TOP_RIGHT[0]:
        if y < screen_height / 2:
            return 25  # 25 is the index of the black captured pieces
        if y > screen_height / 2:
            return 24  # 24 is the index of the white captured pieces
    for i in range(6 * 4):
        if OFFSETS[i][0] < x < OFFSETS[i][0] + PIECE_WIDTH:
            if y < screen_height / 2 and i < 12:
                return i
            if y > screen_height / 2 and i >= 12:
                return i
    return None


def handleEvents(event: pygame.event.Event, state: UIState):
    board = state.get_board()
    if event.type == pygame.MOUSEBUTTONDOWN:
        clicked_index = get_board_index(*pygame.mouse.get_pos())
        # if there is not piece on the clicked index do nothing
        if (
            state.holding_piece is None
            and clicked_index in [24, 25]
            and (
                board.cuptured[Color.WHITE] > 0
                if clicked_index == 24
                else board.cuptured[Color.BLACK] > 0
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
            if state.holding_piece_previews_index in [24, 25]:
                try:
                    board.ExecuteAction(PlaceAction(clicked_index))
                    board.Commit()
                except Exception as e:
                    state.holding_piece = None
                    state.holding_piece_previews_index = None
            else:
                try:
                    board.ExecuteAction(
                        MoveAction(
                            from_index=state.holding_piece_previews_index,
                            to_index=clicked_index,
                        )
                    )
                    board.Commit()
                except Exception as e:
                    state.holding_piece = None
                    state.holding_piece_previews_index = None

        state.holding_piece = None
        state.holding_piece_previews_index = None

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            try:
                board.ExecuteAction(RollDiceAction())
                board.Commit()
            except Exception as e:
                pass
        if event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
            board.Undo()

        if event.key == pygame.K_c:
            best_moves = []
            score = 0
            if board.dices != [-1, -1]:
                best_moves, score = board.GetBestMovesForDices(depth=0)

                print("Best moves: ", best_moves, score)
                # make the moves
                for move in best_moves:
                    board.ExecuteAction(move)
                    board = board.Commit()
            else:
                print("No dices rolled yet")

        # moves only for latest part of the game
        if event.key in [
            pygame.K_1,
            pygame.K_2,
            pygame.K_3,
            pygame.K_4,
            pygame.K_5,
            pygame.K_6,
        ]:
            try:
                number = int(event.key) - pygame.K_1 + 1
                board.ExecuteAction(
                    RemoveAction((24 - number) if board.is_white_turn else (number - 1))
                )
                board.Commit()
            except Exception as e:
                pass

        if event.key == pygame.K_e:
            print("Evaluating the board")
            print(board.Evalutate(1))
