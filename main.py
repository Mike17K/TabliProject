import pygame
import sys
from UI.state import UIState
from UI.events import handleEvents
from UI.visuals import DrawState

pygame.init()

state = UIState().get_instance()

state.board.is_white_turn = (
    True  # TODO make at first the players to roll dices to deside the turn
)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                dice1, dice2 = state.board.RollDices()
                print(
                    state.board.GetBestMoveForDices(
                        dice1=dice1, dice2=dice2, is_white=True
                    )
                )

        handleEvents(event, state)

    DrawState(state)

    pygame.display.flip()

pygame.quit()
sys.exit()
