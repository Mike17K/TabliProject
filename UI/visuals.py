import pygame
from UI.constants import screen_height, screen_width, background_image, whitePiece, blackPiece, PIECE_WIDTH

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Simple Pygame Window')

def DrawState(state):
    # Draw the background image
    screen.blit(background_image, (0, 0))

    state.board.draw(state.holding_piece_previews_index)

    # Draw the captured pieces
    captured_black_index = 0
    captured_white_index = 0
    tmp = state.board.captured_pieces[::]
    tmp.remove(state.holding_piece) if state.holding_piece in tmp and state.holding_piece_previews_index in [24,25] else None
    for i in range(len(tmp)):
        if tmp[i] > 0:
            screen.blit(whitePiece, [screen_width/2 - PIECE_WIDTH/2, screen_height /2 + captured_white_index*PIECE_WIDTH + PIECE_WIDTH/2])
            captured_white_index += 1
        else:
            screen.blit(blackPiece, [screen_width/2 - PIECE_WIDTH/2, screen_height /2 - captured_black_index*PIECE_WIDTH - 3*PIECE_WIDTH/2])
            captured_black_index += 1

    # Draw the holding piece
    if state.holding_piece is not None:
        x,y = pygame.mouse.get_pos()
        if state.holding_piece > 0:
            screen.blit(whitePiece, (x - PIECE_WIDTH/2,y - PIECE_WIDTH/2))
        else:
            screen.blit(blackPiece, (x - PIECE_WIDTH/2,y - PIECE_WIDTH/2))

