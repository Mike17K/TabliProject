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

    pygame.display.flip()

pygame.quit()
sys.exit()
