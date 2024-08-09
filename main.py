import pygame
import sys
from UI.state import UIState
from UI.events import handleEvents
from UI.visuals import DrawState

pygame.init()

state = UIState().get_instance()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print(state.board.GetBestMoveForDices(dice1=6, dice2=6, is_white=True))

        handleEvents(event, state)

    DrawState(state)

    pygame.display.flip()

pygame.quit()
sys.exit()
