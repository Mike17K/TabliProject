from UI.constants import whitePiece, blackPiece, PIECE_WIDTH, OFFSETS
from UI.visuals import screen
from UI.events import encodeMove
import pygame


class Board:
    HISTORY = []

    def __init__(self):
        self.version = ""

        self.captured_pieces = []  # -1 , 1 ,-1..

        self.board = [0 for _ in range(6 * 4)]
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

    def draw(self, holding_index=None):
        for board_index in range(6 * 4):
            if self.board[board_index] == 0:
                continue
            reduce = (
                (1 if self.board[holding_index] > 0 else -1)
                if holding_index == board_index and self.board[holding_index] != 0
                else 0
            )

            x, y = OFFSETS[board_index]
            if self.board[board_index] > 0:
                for white_piece_index in range(self.board[board_index] - reduce):
                    if board_index > 11:
                        screen.blit(
                            pygame.transform.scale(
                                whitePiece, (PIECE_WIDTH, PIECE_WIDTH)
                            ),
                            (x, y - white_piece_index * PIECE_WIDTH),
                        )
                    else:
                        screen.blit(
                            pygame.transform.scale(
                                whitePiece, (PIECE_WIDTH, PIECE_WIDTH)
                            ),
                            (x, y + white_piece_index * PIECE_WIDTH),
                        )
            else:
                for black_piece_index in range(-self.board[board_index] + reduce):
                    if board_index > 11:
                        screen.blit(
                            pygame.transform.scale(
                                blackPiece, (PIECE_WIDTH, PIECE_WIDTH)
                            ),
                            (x, y - black_piece_index * PIECE_WIDTH),
                        )
                    else:
                        screen.blit(
                            pygame.transform.scale(
                                blackPiece, (PIECE_WIDTH, PIECE_WIDTH)
                            ),
                            (x, y + black_piece_index * PIECE_WIDTH),
                        )

    def move(self, from_index, to_index):
        if to_index < 0 or to_index > 23:
            return self  # not correct move the index must be in the board
        # index 24, 25 is the middle section for white and black
        newBoard = Board.From(self)
        newBoard.version = self.version + encodeMove(from_index, to_index)
        newBoard.Commit()
        if from_index == 24 and 1 in self.captured_pieces:
            if self.board[to_index] < -1:
                return self  # not correct move place on 2 or more black pieces

            if newBoard.board[to_index] < 0:
                newBoard.captured_pieces.append(newBoard.board[to_index])

            newBoard.board[to_index] = 1 + (
                newBoard.board[to_index] if newBoard.board[to_index] > 0 else 0
            )
            newBoard.captured_pieces.remove(1)
            return newBoard
        if from_index == 25 and -1 in self.captured_pieces:
            if self.board[to_index] > 1:
                return self  # not correct move place on 2 or more white pieces

            if newBoard.board[to_index] > 0:
                newBoard.captured_pieces.append(newBoard.board[to_index])

            newBoard.board[to_index] = -1 + (
                newBoard.board[to_index] if newBoard.board[to_index] < 0 else 0
            )
            newBoard.captured_pieces.remove(-1)
            return newBoard

        if self.board[from_index] == 0:
            return self

        # normal move from to
        holding_piece = 1 if newBoard.board[from_index] > 0 else -1
        newBoard.board[
            from_index
        ] -= holding_piece  # remove the piece from the from index
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

    def Undo(self):
        if len(self.HISTORY) > 1:
            self.HISTORY.pop()
            self.board = self.HISTORY[-1]
            return True
        return False

    # Logic
    def GetAvailableMovesFromDice(self, dice: int, is_white: bool) -> list[int, int]:
        moves: list[int, int] = []
        for i in range(24 - dice):
            index = i if is_white else (dice + i)
            next_index = index + dice * (1 if is_white else -1)
            if (
                self.board[index] == 0
                or self.board[index] * (1 if is_white else -1) < 0
            ):
                continue
            if (
                self.board[next_index] in [-1, 1, 0]
                or self.board[next_index] * (1 if is_white else -1) > 0
            ):
                moves.append((index, next_index))
        return moves

    def CostOfMove(self, from_index, to_index) -> float:
        newBoard = self.move(from_index, to_index)
        # evaluate the board
        score = 0
        for i in range(24):
            if newBoard.board[i] == 0:
                continue
            # score += newBoard.board[i] * (i-(22 if newBoard.board[i] > 0 else 2))
            if newBoard.board[i] == 1:
                score += -10
            if newBoard.board[i] == -1:
                score += 10
        # the closer to the end the better
        # the more linear distribution on end the better
        # the single pieces where opponent has at least 1 piece before is bad
        # MORE
        return score

    def EvaluateBoard(self, is_white: bool) -> float:
        # for each combination of the dises take the sum of the cost of the moves
        costs = []
        for dice1 in range(1, 7):
            moves1 = self.GetAvailableMovesFromDice(dice1, is_white)
            for m in moves1:
                tmpBoard = self.move(m[0], m[1])
                for dice2 in range(1, 7):
                    moves2 = tmpBoard.GetAvailableMovesFromDice(dice2, is_white)
                    for m2 in moves2:
                        tmpBoard2 = tmpBoard.move(m2[0], m2[1])
                        if dice1 == dice2:
                            moves3 = tmpBoard2.GetAvailableMovesFromDice(
                                dice2, is_white
                            )
                            for m3 in moves3:
                                tmpBoard3 = tmpBoard2.move(m3[0], m3[1])
                                for m4 in tmpBoard3.GetAvailableMovesFromDice(
                                    dice2, is_white
                                ):
                                    tmpBoard4 = tmpBoard3.move(m4[0], m4[1])
                                    costs.append(tmpBoard4.CostOfMove(m4[0], m4[1]))
                        else:
                            costs.append(tmpBoard2.CostOfMove(m2[0], m2[1]))
        return sum(costs) / len(costs) if len(costs) > 0 else 0

    def GetBestMoveForDices(
        self, dice1: int, dice2: int, is_white: bool
    ) -> list[int, int]:
        moves1 = self.GetAvailableMovesFromDice(dice1, is_white)
        moves2 = self.GetAvailableMovesFromDice(dice2, is_white)

        # TODO handle diferently for same value dices

        best_move1 = None
        best_move2 = None
        best_move3 = None
        best_move4 = None
        best_cost = None
        for m1 in moves1:
            tmpBoard = self.move(m1[0], m1[1])
            for m2 in moves2:
                tmpBoard2 = tmpBoard.move(m2[0], m2[1])
                if dice1 == dice2:
                    moves3 = tmpBoard2.GetAvailableMovesFromDice(dice2, is_white)
                    for m3 in moves3:
                        tmpBoard3 = tmpBoard2.move(m3[0], m3[1])
                        for m4 in tmpBoard3.GetAvailableMovesFromDice(dice2, is_white):
                            tmpBoard4 = tmpBoard3.move(m4[0], m4[1])
                            cost = tmpBoard4.EvaluateBoard(not is_white)
                            if best_cost == None or cost * (
                                1 if is_white else -1
                            ) >= best_cost * (1 if is_white else -1):
                                best_cost = cost
                                best_move1 = m1
                                best_move2 = m2
                                best_move3 = m3
                                best_move4 = m4
                                print(best_cost)
                else:
                    cost = tmpBoard2.EvaluateBoard(not is_white)
                    if best_cost == None or cost * (
                        1 if is_white else -1
                    ) >= best_cost * (1 if is_white else -1):
                        best_cost = cost
                        best_move1 = m1
                        best_move2 = m2
                        best_move3 = None
                        best_move4 = None
                        print(best_cost)
        return best_move1, best_move2, best_move3, best_move4


class UIState:
    INSTANCE = None

    def __init__(self):
        self.board = Board()
        self.board.Commit()
        self.holding_piece = None
        self.holding_piece_previews_index = None
        self.running = True
        self.is_white_turn = True

    @staticmethod
    def get_instance():
        if UIState.INSTANCE is None:
            UIState.INSTANCE = UIState()
        return UIState.INSTANCE
