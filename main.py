import pygame
import sys
pygame.init()

screen_width = 1024
screen_height = 1024
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Simple Pygame Window')

# Load the background image
background_image = pygame.image.load('./tabli.png')

# constants
SECTION_TOP_LEFT = [16,16] # x,y
SECTION_TOP_RIGHT = [534,16] # x,y
SECTION_BOTTOM_LEFT = [16,1008] # x,y
SECTION_BOTTOM_RIGHT = [534,1008] # x,y

PIECE_WIDTH = 78.76

OFFSETS = [[SECTION_TOP_LEFT[0] + PIECE_WIDTH*i,SECTION_TOP_LEFT[1]] for i in range(6)] +\
        [[SECTION_TOP_RIGHT[0] + PIECE_WIDTH*i,SECTION_TOP_RIGHT[1]] for i in range(6)] +\
        [[SECTION_BOTTOM_RIGHT[0] + PIECE_WIDTH*i,SECTION_BOTTOM_RIGHT[1] - PIECE_WIDTH] for i in range(6)][::-1] +\
        [[SECTION_BOTTOM_LEFT[0] + PIECE_WIDTH*i,SECTION_BOTTOM_LEFT[1] - PIECE_WIDTH] for i in range(6)][::-1]

def get_board_index(x,y):
    for i in range(6*4):
        if OFFSETS[i][0] < x < OFFSETS[i][0] + PIECE_WIDTH:
            if y < screen_height/2 and i < 12:
                return i
            if y > screen_height/2 and i >= 12:
                return i
    return None

class Board: 
    def __init__(self):
        self.captured_pieces = [] # -1 , 1 ,-1..

        self.board = [0 for _ in range(6*4)]
        # black pieces -1 -> ..
        # white pieces 1 -> ..

        # setup start board
        self.board[0] = 2
        self.board[11] = 5
        self.board[16] = 3
        self.board[18] = 5
        
        self.board[23] = -2
        self.board[5] = -5
        self.board[7] = -3
        self.board[12] = -5    

    def draw(self):
        for board_index in range(6*4):
            if self.board[board_index] == 0:
                continue
            x,y = OFFSETS[board_index]
            if self.board[board_index] > 0:
                for white_piece_index in range(self.board[board_index]):
                    if board_index > 11:
                        screen.blit(whitePiece, (x,y - white_piece_index*PIECE_WIDTH))
                    else:
                        screen.blit(whitePiece, (x,y + white_piece_index*PIECE_WIDTH))
            else:
                for black_piece_index in range(-self.board[board_index]):
                    if board_index > 11:
                        screen.blit(blackPiece, (x,y - black_piece_index*PIECE_WIDTH))
                    else:
                        screen.blit(blackPiece, (x,y + black_piece_index*PIECE_WIDTH))

board = Board()    

whitePiece = pygame.image.load('./white.png')
blackPiece = pygame.image.load('./black.png')

holding_piece_previews_index = None
holding_piece = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked_index = get_board_index(*pygame.mouse.get_pos())
            # if there is not piece on the clicked index do nothing
            if clicked_index is not None and board.board[clicked_index] != 0:
                holding_piece = 1 if board.board[clicked_index] > 0 else -1
                board.board[clicked_index] -= holding_piece
                holding_piece_previews_index = clicked_index
        if event.type == pygame.MOUSEBUTTONUP:
            if holding_piece is not None:
                clicked_index = get_board_index(*pygame.mouse.get_pos())
                if clicked_index is not None:
                    if board.board[clicked_index] * holding_piece >= 0:
                        board.board[clicked_index] += holding_piece
                    else:
                        # here is a posible capture or not correct move
                        if abs(board.board[clicked_index]) == 1:
                            board.captured_pieces.append(board.board[clicked_index])
                            board.board[clicked_index] = holding_piece
                        else:
                            board.board[holding_piece_previews_index] += holding_piece
                else:
                    board.board[holding_piece_previews_index] += holding_piece
                holding_piece = None
        
    # Draw the background image
    screen.blit(background_image, (0, 0))

    board.draw()

    # Draw the captured pieces
    captured_black_index = 0
    captured_white_index = 0
    for i in range(len(board.captured_pieces)):
        if board.captured_pieces[i] > 0:
            screen.blit(whitePiece, [screen_width/2 - PIECE_WIDTH/2, screen_height /2 + captured_white_index*PIECE_WIDTH + PIECE_WIDTH/2])
            captured_white_index += 1
        else:
            screen.blit(blackPiece, [screen_width/2 - PIECE_WIDTH/2, screen_height /2 - captured_black_index*PIECE_WIDTH - 3*PIECE_WIDTH/2])
            captured_black_index += 1

    # Draw the holding piece
    if holding_piece is not None:
        x,y = pygame.mouse.get_pos()
        if holding_piece > 0:
            screen.blit(whitePiece, (x - PIECE_WIDTH/2,y - PIECE_WIDTH/2))
        else:
            screen.blit(blackPiece, (x - PIECE_WIDTH/2,y - PIECE_WIDTH/2))

    

    pygame.display.flip()

pygame.quit()
sys.exit()
