from UI.state import UIState
import pygame
import sys
from UI.events import handleEvents
from UI.visuals import DrawState

pygame.init()

state = UIState().get_instance()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        handleEvents(event, state)

    DrawState(state)

    if "won" in state.get_board().state:
        print("Game Over: ", state.get_board().state)
        running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
