import pygame
import base64
import sys
pygame.init()

screen_width = 1024
screen_height = 1024
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Simple Pygame Window')

# Load images
background_image = pygame.image.load('images/tabli.png')
whitePiece = pygame.image.load('images/white.png')
blackPiece = pygame.image.load('images/black.png')

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

def get_board_index(x,y) -> int:
    # if the click is on the middle section
    if SECTION_TOP_LEFT[0] + 6*PIECE_WIDTH < x < SECTION_TOP_RIGHT[0]:
        if y < screen_height/2:
            return 25
        if y > screen_height/2:
            return 24
    for i in range(6*4):
        if OFFSETS[i][0] < x < OFFSETS[i][0] + PIECE_WIDTH:
            if y < screen_height/2 and i < 12:
                return i
            if y > screen_height/2 and i >= 12:
                return i
    return None

def encodeMove(from_index,to_index):
    # 0 -> 25 + 0 -> 23  = 2 letters 
    return chr(from_index + 65) + chr(to_index + 65)

class Board: 
    HISTORY = []
    def __init__(self):
        self.version = ""

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

    @staticmethod
    def From(board):
        newBoard = Board()
        newBoard.board = board.board[::]
        newBoard.captured_pieces = board.captured_pieces[::]
        return newBoard

    def draw(self, holding_index = None):
        for board_index in range(6*4):
            if self.board[board_index] == 0:
                continue
            reduce = ( 1 if self.board[holding_index] > 0 else -1 ) if holding_index == board_index and self.board[holding_index] != 0 else 0

            x,y = OFFSETS[board_index]
            if self.board[board_index] > 0:
                for white_piece_index in range(self.board[board_index] - reduce):
                    if board_index > 11:
                        screen.blit(whitePiece, (x,y - white_piece_index*PIECE_WIDTH))
                    else:
                        screen.blit(whitePiece, (x,y + white_piece_index*PIECE_WIDTH))
            else:
                for black_piece_index in range(-self.board[board_index] + reduce):
                    if board_index > 11:
                        screen.blit(blackPiece, (x,y - black_piece_index*PIECE_WIDTH))
                    else:
                        screen.blit(blackPiece, (x,y + black_piece_index*PIECE_WIDTH))
    
    def move(self,from_index,to_index):
        if to_index < 0 or to_index > 23: return self # not correct move the index must be in the board
        # index 24, 25 is the middle section for white and black
        newBoard = Board.From(self)
        newBoard.version = self.version + encodeMove(from_index,to_index)
        newBoard.Commit()
        if from_index == 24 and 1 in self.captured_pieces:
            if self.board[to_index] < -1: return self # not correct move place on 2 or more black pieces
            
            if newBoard.board[to_index]<0: newBoard.captured_pieces.append(newBoard.board[to_index])

            newBoard.board[to_index] = 1 + (newBoard.board[to_index] if newBoard.board[to_index]>0 else 0)
            newBoard.captured_pieces.remove(1)
            return newBoard
        if from_index == 25 and -1 in self.captured_pieces:
            if self.board[to_index] > 1: return self # not correct move place on 2 or more white pieces

            if newBoard.board[to_index]>0: newBoard.captured_pieces.append(newBoard.board[to_index])

            newBoard.board[to_index] = -1 + (newBoard.board[to_index] if newBoard.board[to_index]<0 else 0)
            newBoard.captured_pieces.remove(-1)
            return newBoard
        
        if self.board[from_index] == 0: return self

        # normal move from to
        holding_piece = 1 if newBoard.board[from_index] > 0 else -1
        newBoard.board[from_index] -= holding_piece # remove the piece from the from index
        if newBoard.board[to_index] * holding_piece >= 0:
            newBoard.board[to_index] += holding_piece
        else:
            # here is a posible capture or not correct move
            if abs(newBoard.board[to_index]) == 1:
                newBoard.captured_pieces.append(newBoard.board[to_index])
                newBoard.board[to_index] = holding_piece
            else:
                newBoard.board[from_index] += holding_piece
        return newBoard
    
    def Commit(self):
        self.HISTORY.append(self.board)

board = Board()    
board.Commit()

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
            if holding_piece is None and clicked_index in [24,25] and (1 in board.captured_pieces if clicked_index == 24 else -1 in board.captured_pieces):
                holding_piece = 1 if clicked_index == 24 else -1
                holding_piece_previews_index = clicked_index
            if clicked_index is not None and 0<= clicked_index <24 and board.board[clicked_index] != 0:
                holding_piece = 1 if board.board[clicked_index] > 0 else -1
                holding_piece_previews_index = clicked_index
        if event.type == pygame.MOUSEBUTTONUP:
            if holding_piece is not None:
                clicked_index = get_board_index(*pygame.mouse.get_pos())
                board = board.move(holding_piece_previews_index,clicked_index)
            holding_piece = None
            holding_piece_previews_index = None
        
    # Draw the background image
    screen.blit(background_image, (0, 0))

    board.draw(holding_piece_previews_index)

    # Draw the captured pieces
    captured_black_index = 0
    captured_white_index = 0
    tmp = board.captured_pieces[::]
    tmp.remove(holding_piece) if holding_piece in tmp and holding_piece_previews_index in [24,25] else None
    for i in range(len(tmp)):
        if tmp[i] > 0:
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
