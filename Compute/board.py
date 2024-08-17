import random


def encodeMove(from_index, to_index):
    # 0 -> 25 + 0 -> 23  = 2 letters
    return chr(from_index + 65) + chr(to_index + 65)

class Board:
    HISTORY = []

    def __init__(self):
        self.is_white_turn = True
        self.board = [2,0,0,0,0,-5 ,0,-3,0,0,0,5, -5,0,0,0,3,0 ,5,0,0,0,0,-2]

        self.captured_pieces = []  # -1 , 1 ,-1..

        self.dice1 = None
        self.dice2 = None
        self.translations = []
        
        self.state = "rolling-the-dices"
        
        # Helper variables for the UI
        self.available_moves = set()

    def RollDices(self):
        self.dice1 = random.randint(1, 6)
        self.dice2 = random.randint(1, 6)
        self.state = "waiting-for-move"
        self.translations = [self.dice1,self.dice2] if self.dice1 != self.dice2 else [self.dice1,self.dice1,self.dice1,self.dice1]
        self.available_moves = set(self.GetAvailableMovesFromDice(dice=self.dice2, is_white=self.is_white_turn)).union(set(self.GetAvailableMovesFromDice(dice=self.dice1, is_white=self.is_white_turn)))
        return self.dice1, self.dice2

    def GetState(self) -> str:
        if self.dice1 == None or self.dice2 == None:
            return "rolling-the-dices"
        if Board.HISTORY[-1] != self: return self.state
        # if moved pieces are equal to the final results then call it done
        if len(self.translations) == 0:
            return "done"
        # else if there are not more available moves then call it done
        newAvailableMoves = set()
        for i in self.translations:
            newAvailableMoves = newAvailableMoves.union(set(self.GetAvailableMovesFromDice(dice=i)))
        self.available_moves = newAvailableMoves
        if len(self.available_moves) == 0:
            return "done"

        # else call it waiting-for-move       
        return "waiting-for-move"

    @staticmethod
    def From(board) -> "Board":
        newBoard = Board()
        newBoard.board = board.board[::]
        newBoard.captured_pieces = board.captured_pieces[::]
            
        newBoard.dice1 = board.dice1
        newBoard.dice2 = board.dice2
        newBoard.is_white_turn = board.is_white_turn
        newBoard.translations = board.translations[::]
        newBoard.available_moves = board.available_moves.copy()

        return newBoard

    def move(self, from_index, to_index, commit=True) -> "Board":
        if (from_index, to_index) not in self.available_moves:
            return self
        if abs(to_index - from_index) not in [self.dice1, self.dice2]:
            return self
        if to_index < 0 or to_index > 23:
            return self  # not correct move the index must be in the board
        # index 24, 25 is the middle section for white and black
        if self.dice1 == None or self.dice2 == None:
            return self
        newBoard = Board.From(self)
        newBoard.translations.remove(abs(to_index - from_index))
        
        if from_index == 24 and 1 in self.captured_pieces:
            if self.board[to_index] < -1:
                return self  # not correct move place on 2 or more black pieces

            if newBoard.board[to_index] < 0:
                newBoard.captured_pieces.append(newBoard.board[to_index])

            newBoard.board[to_index] = 1 + (
                newBoard.board[to_index] if newBoard.board[to_index] > 0 else 0
            )
            newBoard.captured_pieces.remove(1)
            if commit:
                newAvailableMoves = set()
                for i in newBoard.translations:
                    newAvailableMoves = newAvailableMoves.union(set(newBoard.GetAvailableMovesFromDice(dice=i)))
                newBoard.available_moves = newAvailableMoves
                return newBoard.Commit()
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
            if commit:
                newAvailableMoves = set()
                for i in newBoard.translations:
                    newAvailableMoves = newAvailableMoves.union(set(newBoard.GetAvailableMovesFromDice(dice=i)))
                newBoard.available_moves = newAvailableMoves
                return newBoard.Commit()
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
        if commit:
            newAvailableMoves = set()
            for i in newBoard.translations:
                newAvailableMoves = newAvailableMoves.union(set(newBoard.GetAvailableMovesFromDice(dice=i)))
            newBoard.available_moves = newAvailableMoves

            return newBoard.Commit()
        return newBoard

    def Commit(self) -> "Board":
        if len(self.HISTORY)!=0 : 
            if self.HISTORY[-1] != self:
                self.HISTORY.append(self)
        else:
            self.HISTORY.append(self)
        self.state = self.GetState()
        print("commited : " + self.state)
        if self.state == "done": 
            newBoard = Board.From(self)
            newBoard.is_white_turn = not self.is_white_turn
            newBoard.dice1 = None
            newBoard.dice2 = None
            newBoard.translations = []
            newBoard.available_moves = set()

            self.HISTORY.append(newBoard)
            return newBoard
        return self

    @staticmethod
    def Undo():
        if len(Board.HISTORY) > 1:
            Board.HISTORY.pop()
            return True
        return False

    # Logic
    def GetAvailableMovesFromDices(self) -> list[list[int, int]]:
        if self.dice1 == None or self.dice2 == None:
            return []
        moves = [] 
        for m in self.GetAvailableMovesFromDice(self.dice1, self.is_white_turn):
            tmpboard = self.move(m[0], m[1], commit=False)
            for m2 in tmpboard.GetAvailableMovesFromDice(self.dice2, self.is_white_turn):
                if self.dice1 != self.dice2:
                    moves.append([m, m2])
                    continue
                tmpboard2 = tmpboard.move(m2[0], m2[1], commit=False)
                for m3 in tmpboard2.GetAvailableMovesFromDice(self.dice2, self.is_white_turn):
                    moves.append([m, m2, m3])
                    tmpboard3 = tmpboard2.move(m3[0], m3[1], commit=False)
                    for m4 in tmpboard3.GetAvailableMovesFromDice(self.dice2, self.is_white_turn):
                        moves.append([m, m2, m3, m4])
        return moves
        
    def GetAvailableMovesFromDice(self, dice: int, is_white: bool=None) -> list[int, int]:
        if is_white == None:
            is_white = self.is_white_turn

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
    
    def CanMovePieceFromTo(self, is_white: bool, from_index: int, to_index: int) -> bool:
        """
        Check if the piece can be moved from the from_index to the to_index
        """
        if self.board[from_index] == 0 or self.board[from_index] * (1 if is_white else -1) < 0:
            return False
        if self.board[to_index] * (-1 if is_white else 1) > 1:
            return False
        return True

    def GetBestMoveForDices(
        self, dice1: int, dice2: int, is_white: bool
    ) -> list[int, int]:
        moves1 = self.GetAvailableMovesFromDice(dice1, is_white)
        moves2 = self.GetAvailableMovesFromDice(dice2, is_white)
        moves = set(moves1).intersection(moves2)
        if len(moves) == 0: return []

        best_moves = [list(moves)[0]] if len(moves) > 0 else []
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
        return best_moves
