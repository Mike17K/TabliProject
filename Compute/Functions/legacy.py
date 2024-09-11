# # Logic
# def GetAvailableMovesFromDices(self) -> list[list[int, int]]:
#     if self.dice1 == None or self.dice2 == None:
#         return []
#     moves = []
#     if self.dice1 == self.dice2:
#         tmpboard = Board.From(self)
#         for m in self.GetAvailableMovesFromDice(self.dice1, self.is_white_turn):
#             tmpboard1 = tmpboard.move(m[0], m[1], commit=False)
#             for m2 in tmpboard1.GetAvailableMovesFromDice(
#                 self.dice2, self.is_white_turn
#             ):
#                 tmpboard2 = tmpboard1.move(m2[0], m2[1], commit=False)
#                 for m3 in tmpboard2.GetAvailableMovesFromDice(
#                     self.dice2, self.is_white_turn
#                 ):
#                     moves.append([m, m2, m3])
#                     tmpboard3 = tmpboard2.move(m3[0], m3[1], commit=False)
#                     for m4 in tmpboard3.GetAvailableMovesFromDice(
#                         self.dice2, self.is_white_turn
#                     ):
#                         moves.append([m, m2, m3, m4])
#     else:
#         tmpboard = Board.From(self)
#         for m in self.GetAvailableMovesFromDice(self.dice1, self.is_white_turn):
#             tmpboard1 = tmpboard.move(m[0], m[1], commit=False)
#             for m2 in tmpboard1.GetAvailableMovesFromDice(
#                 self.dice2, self.is_white_turn
#             ):
#                 tmpboard2 = tmpboard1.move(m2[0], m2[1], commit=False)
#                 moves.append([m, m2])
#         for m in self.GetAvailableMovesFromDice(self.dice2, self.is_white_turn):
#             tmpboard1 = tmpboard.move(m[0], m[1], commit=False)
#             for m2 in tmpboard1.GetAvailableMovesFromDice(
#                 self.dice1, self.is_white_turn
#             ):
#                 tmpboard2 = tmpboard1.move(m2[0], m2[1], commit=False)
#                 moves.append([m, m2])

#     return moves


# def EvaluateBoard(self, is_white: bool, depth=0) -> float:
#     print("depth=", depth)
#     MAX_DEPTH = 0
#     # Here we can implement a deap search with a depth
#     if depth >= MAX_DEPTH:
#         return self.GetCost()

#     # for each combination of the dises take the sum of the cost of the moves
#     costs = []

#     for dice1, dice2 in [[i, j] for i in range(1, 7) for j in range(1, 7)]:
#         self.SetDices(dice1, dice2)
#         bestMoves, score = self.GetBestMoveForDicesByCost()
#         tmpboard = self
#         for move in bestMoves:
#             tmpboard = tmpboard.move(move[0], move[1], commit=False)
#         costs.append(tmpboard.EvaluateBoard(is_white, depth + 1))

#     return sum(costs) / len(costs) if len(costs) > 0 else 0


# def CanMovePieceFromTo(self, is_white: bool, from_index: int, to_index: int) -> bool:
#     """
#     Check if the piece can be moved from the from_index to the to_index
#     """
#     if (
#         self.board[from_index] == 0
#         or self.board[from_index] * (1 if is_white else -1) < 0
#     ):
#         return False
#     if self.board[to_index] * (-1 if is_white else 1) > 1:
#         return False
#     return True


# def GetBestMoveForDicesByCost(self) -> list[list[list[int, int]], float]:
#     if self.dice1 == None or self.dice2 == None:
#         return []

#     best_move1 = None
#     best_move2 = None
#     best_move3 = None
#     best_move4 = None
#     best_cost = None

#     if self.dice1 == self.dice2:
#         for m1 in self.GetAvailableMovesFromDice(self.dice1, self.is_white_turn):
#             tmpBoard = self.move(m1[0], m1[1], commit=False)
#             moves2 = tmpBoard.GetAvailableMovesFromDice(self.dice2, self.is_white_turn)
#             if len(moves2) == 0:
#                 cost = tmpBoard.GetCost()
#                 if best_cost == None or cost * (
#                     1 if self.is_white_turn else -1
#                 ) >= best_cost * (1 if self.is_white_turn else -1):
#                     best_cost = cost
#                     best_move1 = m1
#                     best_move2 = None
#                     best_move3 = None
#                     best_move4 = None
#                     best_moves = [best_move1]
#                 continue
#             for m2 in moves2:
#                 tmpBoard2 = tmpBoard.move(m2[0], m2[1], commit=False)
#                 moves3 = tmpBoard2.GetAvailableMovesFromDice(
#                     self.dice2, self.is_white_turn
#                 )
#                 if len(moves3) == 0:
#                     cost = tmpBoard2.GetCost()
#                     if best_cost == None or cost * (
#                         1 if self.is_white_turn else -1
#                     ) >= best_cost * (1 if self.is_white_turn else -1):
#                         best_cost = cost
#                         best_move1 = m1
#                         best_move2 = m2
#                         best_move3 = None
#                         best_move4 = None
#                         best_moves = [best_move1, best_move2]
#                     continue
#                 for m3 in moves3:
#                     tmpBoard3 = tmpBoard2.move(m3[0], m3[1], commit=False)
#                     moves4 = tmpBoard3.GetAvailableMovesFromDice(
#                         self.dice2, self.is_white_turn
#                     )
#                     if len(moves4) == 0:
#                         cost = tmpBoard3.GetCost()
#                         if best_cost == None or cost * (
#                             1 if self.is_white_turn else -1
#                         ) >= best_cost * (1 if self.is_white_turn else -1):
#                             best_cost = cost
#                             best_move1 = m1
#                             best_move2 = m2
#                             best_move3 = m3
#                             best_move4 = None
#                             best_moves = [best_move1, best_move2, best_move3]
#                             print(best_cost, best_move1, best_move2, best_move3)
#                         continue
#                     for m4 in moves4:
#                         tmpBoard4 = tmpBoard3.move(m4[0], m4[1], commit=False)
#                         cost = tmpBoard4.GetCost()
#                         if best_cost == None or cost * (
#                             1 if self.is_white_turn else -1
#                         ) >= best_cost * (1 if self.is_white_turn else -1):
#                             best_cost = cost
#                             best_move1 = m1
#                             best_move2 = m2
#                             best_move3 = m3
#                             best_move4 = m4
#                             best_moves = [
#                                 best_move1,
#                                 best_move2,
#                                 best_move3,
#                                 best_move4,
#                             ]
#     else:
#         for m1 in self.GetAvailableMovesFromDice(self.dice1, self.is_white_turn):
#             tmpBoard = self.move(m1[0], m1[1], commit=False)
#             moves1 = tmpBoard.GetAvailableMovesFromDice(self.dice2, self.is_white_turn)
#             if len(moves1) == 0:
#                 cost = tmpBoard.GetCost()
#                 if best_cost == None or cost * (
#                     1 if self.is_white_turn else -1
#                 ) >= best_cost * (1 if self.is_white_turn else -1):
#                     best_cost = cost
#                     best_move1 = m1
#                     best_move2 = None
#                     best_move3 = None
#                     best_move4 = None
#                     best_moves = [best_move1]
#                 continue
#             for m2 in moves1:
#                 tmpBoard2 = tmpBoard.move(m2[0], m2[1], commit=False)
#                 cost = tmpBoard2.GetCost()
#                 if best_cost == None or cost * (
#                     1 if self.is_white_turn else -1
#                 ) >= best_cost * (1 if self.is_white_turn else -1):
#                     best_cost = cost
#                     best_move1 = m1
#                     best_move2 = m2
#                     best_move3 = None
#                     best_move4 = None
#                     best_moves = [best_move1, best_move2]

#         for m1 in self.GetAvailableMovesFromDice(self.dice2, self.is_white_turn):
#             tmpBoard = self.move(m1[0], m1[1], commit=False)
#             moves1 = tmpBoard.GetAvailableMovesFromDice(self.dice1, self.is_white_turn)
#             if len(moves1) == 0:
#                 cost = tmpBoard.GetCost()
#                 if best_cost == None or cost * (
#                     1 if self.is_white_turn else -1
#                 ) >= best_cost * (1 if self.is_white_turn else -1):
#                     best_cost = cost
#                     best_move1 = m1
#                     best_move2 = None
#                     best_move3 = None
#                     best_move4 = None
#                     best_moves = [best_move1]
#                 continue
#             for m2 in moves1:
#                 tmpBoard2 = tmpBoard.move(m2[0], m2[1], commit=False)
#                 cost = tmpBoard2.GetCost()
#                 if best_cost == None or cost * (
#                     1 if self.is_white_turn else -1
#                 ) >= best_cost * (1 if self.is_white_turn else -1):
#                     best_cost = cost
#                     best_move1 = m1
#                     best_move2 = m2
#                     best_move3 = None
#                     best_move4 = None
#                     best_moves = [best_move1, best_move2]

#     return best_moves, best_cost


# def GetBestMoveForDices(self) -> list[list[list[int, int]], float]:
#     if self.dice1 == None or self.dice2 == None:
#         return [], 0

#     best_move1 = None
#     best_move2 = None
#     best_move3 = None
#     best_move4 = None
#     best_cost = None

#     if self.dice1 == self.dice2:
#         for m1 in self.GetAvailableMovesFromDice(self.dice1, self.is_white_turn):
#             tmpBoard = self.move(m1[0], m1[1], commit=False)
#             moves2 = tmpBoard.GetAvailableMovesFromDice(self.dice2, self.is_white_turn)
#             if len(moves2) == 0:
#                 cost = tmpBoard.EvaluateBoard(self.is_white_turn)
#                 if best_cost == None or cost * (
#                     1 if self.is_white_turn else -1
#                 ) >= best_cost * (1 if self.is_white_turn else -1):
#                     best_cost = cost
#                     best_move1 = m1
#                     best_move2 = None
#                     best_move3 = None
#                     best_move4 = None
#                     best_moves = [best_move1]
#                 continue
#             for m2 in moves2:
#                 tmpBoard2 = tmpBoard.move(m2[0], m2[1], commit=False)
#                 moves3 = tmpBoard2.GetAvailableMovesFromDice(
#                     self.dice2, self.is_white_turn
#                 )
#                 if len(moves3) == 0:
#                     cost = tmpBoard2.EvaluateBoard(self.is_white_turn)
#                     if best_cost == None or cost * (
#                         1 if self.is_white_turn else -1
#                     ) >= best_cost * (1 if self.is_white_turn else -1):
#                         best_cost = cost
#                         best_move1 = m1
#                         best_move2 = m2
#                         best_move3 = None
#                         best_move4 = None
#                         best_moves = [best_move1, best_move2]
#                     continue
#                 for m3 in moves3:
#                     tmpBoard3 = tmpBoard2.move(m3[0], m3[1], commit=False)
#                     moves4 = tmpBoard3.GetAvailableMovesFromDice(
#                         self.dice2, self.is_white_turn
#                     )
#                     if len(moves4) == 0:
#                         cost = tmpBoard3.EvaluateBoard(self.is_white_turn)
#                         if best_cost == None or cost * (
#                             1 if self.is_white_turn else -1
#                         ) >= best_cost * (1 if self.is_white_turn else -1):
#                             best_cost = cost
#                             best_move1 = m1
#                             best_move2 = m2
#                             best_move3 = m3
#                             best_move4 = None
#                             best_moves = [best_move1, best_move2, best_move3]
#                             print(best_cost, best_move1, best_move2, best_move3)
#                         continue
#                     for m4 in moves4:
#                         tmpBoard4 = tmpBoard3.move(m4[0], m4[1], commit=False)
#                         cost = tmpBoard4.EvaluateBoard(self.is_white_turn)
#                         if best_cost == None or cost * (
#                             1 if self.is_white_turn else -1
#                         ) >= best_cost * (1 if self.is_white_turn else -1):
#                             best_cost = cost
#                             best_move1 = m1
#                             best_move2 = m2
#                             best_move3 = m3
#                             best_move4 = m4
#                             best_moves = [
#                                 best_move1,
#                                 best_move2,
#                                 best_move3,
#                                 best_move4,
#                             ]
#     else:
#         board1 = Board.From(self)
#         for m1 in self.GetAvailableMovesFromDice(self.dice1, self.is_white_turn):
#             tmpBoard = board1.move(m1[0], m1[1], commit=False)
#             moves1 = tmpBoard.GetAvailableMovesFromDice(self.dice2, self.is_white_turn)
#             if len(moves1) == 0:
#                 cost = tmpBoard.EvaluateBoard(self.is_white_turn)
#                 if best_cost == None or cost * (
#                     1 if self.is_white_turn else -1
#                 ) >= best_cost * (1 if self.is_white_turn else -1):
#                     best_cost = cost
#                     best_move1 = m1
#                     best_move2 = None
#                     best_move3 = None
#                     best_move4 = None
#                     best_moves = [best_move1]
#                 continue
#             for m2 in moves1:
#                 tmpBoard2 = tmpBoard.move(m2[0], m2[1], commit=False)
#                 cost = tmpBoard2.EvaluateBoard(self.is_white_turn)
#                 if best_cost == None or cost * (
#                     1 if self.is_white_turn else -1
#                 ) >= best_cost * (1 if self.is_white_turn else -1):
#                     best_cost = cost
#                     best_move1 = m1
#                     best_move2 = m2
#                     best_move3 = None
#                     best_move4 = None
#                     best_moves = [best_move1, best_move2]

#         board1 = Board.From(self)
#         for m1 in self.GetAvailableMovesFromDice(self.dice2, self.is_white_turn):
#             tmpBoard = board1.move(m1[0], m1[1], commit=False)
#             moves1 = tmpBoard.GetAvailableMovesFromDice(self.dice1, self.is_white_turn)
#             if len(moves1) == 0:
#                 cost = tmpBoard.EvaluateBoard(self.is_white_turn)
#                 if best_cost == None or cost * (
#                     1 if self.is_white_turn else -1
#                 ) >= best_cost * (1 if self.is_white_turn else -1):
#                     best_cost = cost
#                     best_move1 = m1
#                     best_move2 = None
#                     best_move3 = None
#                     best_move4 = None
#                     best_moves = [best_move1]
#                 continue
#             for m2 in moves1:
#                 tmpBoard2 = tmpBoard.move(m2[0], m2[1], commit=False)
#                 cost = tmpBoard2.EvaluateBoard(self.is_white_turn)
#                 if best_cost == None or cost * (
#                     1 if self.is_white_turn else -1
#                 ) >= best_cost * (1 if self.is_white_turn else -1):
#                     best_cost = cost
#                     best_move1 = m1
#                     best_move2 = m2
#                     best_move3 = None
#                     best_move4 = None
#                     best_moves = [best_move1, best_move2]

#     return best_moves, best_cost
