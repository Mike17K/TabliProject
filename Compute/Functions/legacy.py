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


# def GetAvailableMovesFromDice(self, dice: int, is_white: bool = None) -> list[int, int]:
#     if is_white == None:
#         is_white = self.is_white_turn

#     moves: list[int, int] = []
#     if len(self.captured_pieces) != 0:
#         if is_white and 1 in self.captured_pieces:  # white has captured pieces
#             if self.board[dice - 1] >= -1:
#                 moves.append((24, dice - 1))
#             return moves
#         if not is_white and -1 in self.captured_pieces:
#             if self.board[24 - dice] <= 1:
#                 moves.append((25, 24 - dice))
#             return moves

#     # check if there is the state for removing pieces
#     piece_count = [0, 0]  # white, black
#     for i in range(24):
#         if self.board[i] > 0:
#             piece_count[0] += self.board[i]
#         if self.board[i] < 0:
#             piece_count[1] += -self.board[i]
#     piece_count[0] += self.captured_pieces.count(1)
#     piece_count[1] += self.captured_pieces.count(-1)

#     if is_white and self.captured_pieces.count(1) == 0:
#         if (
#             piece_count[0]
#             == self.board[23]
#             + self.board[22]
#             + self.board[21]
#             + self.board[20]
#             + self.board[19]
#             + self.board[18]
#         ):
#             # max index
#             min_index = 5
#             for i in range(6):
#                 if self.board[23 - i] > 0:
#                     min_index = i
#                     if dice - 1 == i:
#                         moves.append((23 - i, 26))
#             if dice - 1 >= min_index:
#                 moves.append((min_index, 26))

#     elif not is_white and self.captured_pieces.count(-1) == 0:
#         if (
#             piece_count[1]
#             == -self.board[5]
#             - self.board[4]
#             - self.board[3]
#             - self.board[2]
#             - self.board[1]
#             - self.board[0]
#         ):
#             # state for removing pieces
#             max_index = 18
#             for i in range(6):
#                 if self.board[i] < 0:
#                     max_index = i
#                     if dice - 1 == i:
#                         moves.append((i, 27))
#             if 24 - dice >= max_index:
#                 moves.append((max_index, 27))

#     for i in range(24 - dice):
#         index = i if is_white else (dice + i)
#         next_index = index + dice * (1 if is_white else -1)
#         if self.board[index] == 0 or self.board[index] * (1 if is_white else -1) < 0:
#             continue
#         if (
#             self.board[next_index] in [-1, 1, 0]
#             or self.board[next_index] * (1 if is_white else -1) > 0
#         ):
#             moves.append((index, next_index))

#     # update the available moves
#     self.available_moves = self.available_moves.union(set(moves))
#     return moves


# def GetCost(self):
#     # evaluate the board
#     score = 0
#     white_pieces = 0
#     black_pieces = 0

#     squares_controlled = [0, 0]  # white , black\
#     last_controlled_sq = [-1, -1]

#     last_white_piece_index = -1
#     last_black_piece_index = -1
#     for i in range(24):
#         if self.board[i] > 0 and last_white_piece_index == -1:
#             last_white_piece_index = i
#         if self.board[23 - i] < 0 and last_black_piece_index == -1:
#             last_black_piece_index = 23 - i

#         # when there are more than 2 pieces then the square is controlled

#         if self.board[23 - i] >= 2:
#             last_controlled_sq[0] = i
#         if self.board[23 - i] <= -2:
#             last_controlled_sq[1] = 23 - i

#     for i in range(24):
#         if self.board[i] == 0:
#             continue

#         isWhite = self.board[i] > 0
#         pieces = abs(self.board[i])
#         quarter = (
#             (23 - i) // 6 if isWhite else i // 6
#         )  # 0,1,2,3 the lower the closest to end

#         # the importance of a square baced of the distance from the end
#         important_factor = 1
#         if quarter == 0:
#             important_factor = 0.8
#         elif quarter == 1:
#             important_factor = 2
#         elif quarter == 2:
#             important_factor = 1.5
#         elif quarter == 3:
#             important_factor = 0.2

#         if last_white_piece_index > 6 * 3 - 1:
#             score += 200
#         if last_black_piece_index < 5:
#             score -= 200

#         # modify important factor baced of the first enemy piece position
#         if isWhite:
#             if i < last_black_piece_index:
#                 important_factor *= 1.5
#             else:
#                 # if there are cuptured pieces importance big
#                 if -1 in self.captured_pieces:
#                     important_factor *= 5
#                 else:
#                     important_factor /= 5
#         else:
#             if i > last_white_piece_index:
#                 important_factor *= 1.5
#             else:
#                 if 1 in self.captured_pieces:
#                     important_factor *= 5
#                 else:
#                     important_factor /= 5
#                 important_factor /= 5

#         # solo pieces bad in general and too bad when there are away from the other pieces
#         if pieces == 1:
#             score += (
#                 30
#                 * (-1 if isWhite else 1)
#                 * important_factor
#                 * (
#                     5
#                     if quarter == 0 and ((-1 if isWhite else 1) in self.captured_pieces)
#                     else 1
#                 )
#             )
#             if isWhite:
#                 if i - last_controlled_sq[0] > 12:
#                     score += -10
#             else:
#                 if last_controlled_sq[1] - i > 12:
#                     score += +10

#         # squares controlled
#         if pieces >= 2:
#             squares_controlled[0 if isWhite else 1] += 3 * important_factor

#         # keep track the number of pieces
#         if isWhite:
#             white_pieces += self.board[i] * important_factor
#         else:
#             black_pieces += -self.board[i] * important_factor

#         # the more pieces you have in the start have a small penalty
#         if quarter == 3:
#             score += 2.5 * (1 if isWhite else -1) * pieces

#     # update score based of the number of pieces
#     score += -white_pieces
#     score -= -black_pieces

#     # udpate score based of captured pieces
#     score += -sum(self.captured_pieces) * 20

#     # update based of the controlled squares
#     score += 10 * (squares_controlled[0] - squares_controlled[1])

#     # the closer to the end the better
#     # the more linear distribution on end the better
#     # the single pieces where opponent has at least 1 piece before is bad
#     # MORE
#     return score


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
