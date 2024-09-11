from UI.state import UIState
import pygame
import sys
from UI.events import handleEvents
from UI.visuals import DrawState
from Compute.types import GameState

pygame.init()

state = UIState().get_instance()
state.get_board().GetState()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        handleEvents(event, state)

    DrawState(state)

    if state.get_board().state in [GameState.WHITE_WINS, GameState.BLACK_WINS]:
        print("Game Over: ", state.get_board().state)
        running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
