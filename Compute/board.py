import random
from Compute.types import (
    Color,
    Action,
    ActionType,
    MoveAction,
    RemoveAction,
    PlaceAction,
    RollDiceAction,
    GameState,
)


class BoardState:
    def __init__(self) -> None:
        self.board: list[int] = [
            2,
            0,
            0,
            0,
            0,
            -5,
            0,
            -3,
            0,
            0,
            0,
            5,
            -5,
            0,
            0,
            0,
            3,
            0,
            5,
            0,
            0,
            0,
            0,
            -2,
            # -2,-2,-2,-3,-3,-3,0,0,0,0,-1,0,0,0,1,0,0,0,0,2,2,3,3,3,
        ]
        self.cuptured: dict[Color, int] = {Color.WHITE: 0, Color.BLACK: 0}
        self.action_to_get_this_state: Action | None = None
        self.is_white_turn = True
        self.dices = [-1, -1]
        self.translations = []

    def __str__(self) -> str:
        return f"Board({self.board}, {self.cuptured}, {self.is_white_turn}, {self.action_to_get_this_state})"

    def ExecuteAction(self, action: Action) -> None:
        """
        Execute the action on the board
        """
        assert (
            self.action_to_get_this_state == None
        ), "You have already executed an action"
        if action.type == ActionType.ROLL_DICE:
            assert self.dices == [-1, -1], "You have already rolled the dices"
            self.rollDiseAction(action)
            self.action_to_get_this_state = action
            return

        assert self.dices != [-1, -1], "You must roll the dices before making a move"
        assert isinstance(action, Action), "Action must be an instance of Action"
        assert action.Validate()
        if action.type == ActionType.MOVE:
            self.moveAction(action)
        elif action.type == ActionType.REMOVE:
            self.removeAction(action)
        elif action.type == ActionType.PLACE:
            self.placeAction(action)
        # store action
        self.action_to_get_this_state = action

    def moveAction(self, action: MoveAction) -> None:
        """
        Move a piece from one index to another
        """
        from_index = action.from_index
        to_index = action.to_index
        assert 0 <= from_index < len(self.board)
        assert 0 <= to_index < len(self.board)
        assert self.board[from_index] != 0
        assert self.board[from_index] * (1 if self.is_white_turn else -1) > 0
        assert abs(from_index - to_index) in self.translations
        assert (
            self.board[from_index] * (to_index - from_index) > 0
        )  # ensure that this is the correct way
        assert (
            self.board[to_index] * (-1 if self.board[from_index] > 0 else 1) <= 1
        )  # ensure that the to index is empty or has only one piece
        assert (
            self.cuptured[Color.WHITE if self.board[from_index] > 0 else Color.BLACK]
            == 0
        )  # ensure that the player has no captured pieces

        fromIsWhite = self.board[from_index] > 0
        if self.board[to_index] * (-1 if fromIsWhite else 1) == 1:
            self.cuptured[Color.BLACK if fromIsWhite else Color.WHITE] += 1
            self.board[to_index] = 0

        self.board[from_index] -= 1 if fromIsWhite else -1
        self.board[to_index] += 1 if fromIsWhite else -1

        self.translations.remove(abs(from_index - to_index))

    def removeAction(self, action: RemoveAction) -> None:
        """
        Remove a piece from the board, for the final stage of the game
        """
        from_index = action.index_to_remove
        assert 0 <= from_index < len(self.board)
        assert self.board[from_index] != 0
        assert self.board[from_index] * (1 if self.is_white_turn else -1) > 0
        assert from_index < 6 if self.board[from_index] < 0 else from_index > 17
        assert (
            self.cuptured[Color.WHITE if self.board[from_index] > 0 else Color.BLACK]
            == 0
        )  # ensure that the player has no captured pieces
        assert sum([p for p in self.board if p * self.board[from_index] > 0]) == sum(
            self.board[:6] if self.board[from_index] < 0 else self.board[18:]
        )  # ensure that the player has no other pieces on the board

        maxPieceIndex = 0
        for j in range(6):
            i = j if self.board[from_index] < 0 else 23 - j
            if self.board[i] * self.board[from_index] > 0:
                maxPieceIndex = j + 1
        requestedDice = (24 - from_index) if self.is_white_turn else (from_index + 1)
        if (requestedDice) in self.translations:
            self.translations.remove(requestedDice)
        else:
            assert maxPieceIndex == requestedDice
            self.translations.remove(max(self.translations))

        isWhite = self.board[from_index] > 0
        if isWhite:
            self.board[from_index] -= 1
        else:
            self.board[from_index] += 1

    def placeAction(self, action: PlaceAction) -> None:
        """
        Place a cuptured piece on board
        """
        to_index = action.to_index
        color = Color.WHITE if self.is_white_turn else Color.BLACK
        assert 0 <= to_index < len(self.board)
        assert to_index < 6 if color == Color.WHITE else to_index > 17
        assert (
            self.board[to_index] * (-1 if color == Color.WHITE else 1) <= 1
        )  # ensure that the to index is empty or has only one piece
        assert self.cuptured[color] > 0
        assert (
            (to_index + 1) in self.translations
            if color == Color.WHITE
            else (24 - to_index) in self.translations
        )

        if (to_index + 1) in self.translations and color == Color.WHITE:
            self.translations.remove(to_index + 1)
        elif (24 - to_index) in self.translations and color == Color.BLACK:
            self.translations.remove(24 - to_index)

        if self.board[to_index] * (-1 if color == Color.WHITE else 1) == 1:
            self.cuptured[Color.BLACK if color == Color.WHITE else Color.WHITE] += 1
            self.board[to_index] = 0

        self.board[to_index] += 1 if color == Color.WHITE else -1
        self.cuptured[color] -= 1

    def rollDiseAction(self, action: RollDiceAction) -> None:
        assert self.dices == [-1, -1]
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        self.dices = [dice1, dice2]
        if dice1 == dice2:
            self.translations = [dice1] * 4
        else:
            self.translations = [dice1, dice2]


class Board(BoardState):

    HISTORY: list["Board"] = []

    @staticmethod
    def From(old: "Board") -> "Board":
        newBoard = Board()
        newBoard.board = old.board.copy()
        newBoard.cuptured = old.cuptured.copy()
        newBoard.is_white_turn = old.is_white_turn
        newBoard.dices = old.dices.copy()
        newBoard.translations = old.translations.copy()
        return newBoard

    def __init__(self):
        super().__init__()
        self.state: GameState = GameState.NOT_STARTED

        self.available_moves_calculated = False
        self.available_moves: set[Action] = set()

        if len(Board.HISTORY) == 0:
            Board.HISTORY.append(self)

    def GetAvailableActions(self) -> set[Action]:
        if not self.available_moves_calculated:
            self.available_moves = self.CalculateAvailableActions()
            self.available_moves_calculated = True
        return self.available_moves

    def GetState(self) -> GameState:
        piece_count = [0, 0]  # white, black
        for i in range(24):
            if self.board[i] > 0:
                piece_count[0] += self.board[i]
            if self.board[i] < 0:
                piece_count[1] += -self.board[i]
        if piece_count[0] == 0:
            self.state = GameState.WHITE_WINS
            return self.state
        if piece_count[1] == 0:
            self.state = GameState.BLACK_WINS
            return self.state

        if self.dices == [-1, -1]:
            self.state = (
                GameState.WHITE_ROLLS if self.is_white_turn else GameState.BLACK_ROLLS
            )
            return self.state
        if len(Board.HISTORY) > 0 and Board.HISTORY[-1] != self:
            return self.state
        # if moved pieces are equal to the final results then call it done
        actions: set[Action] = set()
        for i in self.translations:
            actions |= self.getActionsForDice(i)

        if len(self.translations) == 0 or (len(actions) == 0 and self.dices != [-1, -1]):
            self.state = (
                GameState.BLACK_ROLLS if self.is_white_turn else GameState.WHITE_ROLLS
            )
            return self.state

        self.state = (
            GameState.WHITE_MOVES if self.is_white_turn else GameState.BLACK_MOVES
        )
        return self.state

    def Commit(self) -> "Board":
        assert self.action_to_get_this_state != None

        newBoard = Board.From(self)

        if (self.dices != [-1, -1] and self.translations == []) or len(
            self.GetAvailableActions()
        ) == 0:
            newBoard.is_white_turn = not self.is_white_turn
            newBoard.dices = [-1, -1]
            newBoard.translations = []
            newBoard.available_moves_calculated = False
            newBoard.available_moves = set()
        
        # Note: this bellow is important order
        Board.HISTORY.append(newBoard)
        print("New state", newBoard.GetState())

        return newBoard

    @staticmethod
    def Undo():
        if len(Board.HISTORY) > 2:
            Board.HISTORY.pop()
            Board.HISTORY.pop()
            Board.Now().Commit()
            return True
        return False

    @staticmethod
    def Now() -> "Board":
        return Board.HISTORY[-1] if len(Board.HISTORY) > 0 else Board()

    ################ Functions Helper #################

    def CalculateAvailableActions(self) -> set[Action]:
        state = self.GetState()
        if state in [GameState.WHITE_WINS, GameState.BLACK_WINS]:
            return set()
        if state in [GameState.WHITE_ROLLS, GameState.BLACK_ROLLS]:
            return {RollDiceAction()}

        # tmp
        actions: set[Action] = set()
        for i in self.translations:
            actions |= self.getActionsForDice(i)
        return actions

    def getActionsForDice(self, dice: int) -> set[Action]:
        assert 0 < dice < 7, "Dice must be between 1 and 6"
        isWhite = self.is_white_turn

        actions: set[Action] = set()

        # if there are cuptured pieces
        if self.cuptured[Color.WHITE if isWhite else Color.BLACK] != 0:
            index_to = (dice - 1) if isWhite else (24 - dice)
            if self.board[index_to] * (1 if isWhite else -1) >= -1:
                actions.add(PlaceAction(index_to))
            return actions

        # check if there is the state for removing pieces
        piece_count = 0
        for i in range(24):
            piece_count += (
                abs(self.board[i]) if self.board[i] * (1 if isWhite else -1) > 0 else 0
            )
        piece_count += self.cuptured[Color.WHITE if isWhite else Color.BLACK]
        sum_pieces_end_pos = sum(
            [
                abs(i)
                for i in self.board[18 if isWhite else 0 : 24 if isWhite else 6]
                if i * (1 if isWhite else -1) > 0
            ]
        )
        if piece_count == sum_pieces_end_pos:
            # state for removing pieces
            for k in range(0, 6):
                i = 6 - k - 1
                if (
                    self.board[(23 - i) if isWhite else (i)] * (1 if isWhite else -1)
                    > 0
                ):
                    if dice - 1 >= i:
                        actions.add(RemoveAction((23 - i) if isWhite else (i)))
                    break

        # simple moves
        for i in range(24 - dice):
            index = i if isWhite else (dice + i)
            next_to = index + dice * (1 if isWhite else -1)
            if self.board[index] * (1 if isWhite else -1) <= 0:
                continue
            if self.board[next_to] * (1 if isWhite else -1) >= -1:
                actions.add(MoveAction(index, next_to))

        return actions

    ######################## Evaluation ######################
    def GetCost(self):
        # evaluate the board
        score = 0
        white_pieces = 0
        black_pieces = 0

        squares_controlled = [0, 0]  # white , black\
        last_controlled_sq = [-1, -1]

        last_white_piece_index = -1
        last_black_piece_index = -1
        for i in range(24):
            if self.board[i] > 0 and last_white_piece_index == -1:
                last_white_piece_index = i
            if self.board[23 - i] < 0 and last_black_piece_index == -1:
                last_black_piece_index = 23 - i

            # when there are more than 2 pieces then the square is controlled

            if self.board[23 - i] >= 2:
                last_controlled_sq[0] = i
            if self.board[23 - i] <= -2:
                last_controlled_sq[1] = 23 - i

        for i in range(24):
            if self.board[i] == 0:
                continue

            isWhite = self.board[i] > 0
            pieces = abs(self.board[i])
            quarter = (
                (23 - i) // 6 if isWhite else i // 6
            )  # 0,1,2,3 the lower the closest to end

            # the importance of a square baced of the distance from the end
            important_factor = 1
            if quarter == 0:
                important_factor = 0.8
            elif quarter == 1:
                important_factor = 2
            elif quarter == 2:
                important_factor = 1.5
            elif quarter == 3:
                important_factor = 0.2

            if last_white_piece_index > 6 * 3 - 1:
                score += 200
            if last_black_piece_index < 5:
                score -= 200

            # modify important factor baced of the first enemy piece position
            if isWhite:
                if i < last_black_piece_index:
                    important_factor *= 1.5
                else:
                    # if there are cuptured pieces importance big
                    if self.cuptured[Color.BLACK] > 0:
                        important_factor *= 5
                    else:
                        important_factor /= 5
            else:
                if i > last_white_piece_index:
                    important_factor *= 1.5
                else:
                    if self.cuptured[Color.WHITE]:
                        important_factor *= 5
                    else:
                        important_factor /= 5
                    important_factor /= 5

            # solo pieces bad in general and too bad when there are away from the other pieces
            if pieces == 1:
                score += (
                    30
                    * (-1 if isWhite else 1)
                    * important_factor
                    * (
                        5
                        if quarter == 0
                        and (self.cuptured[Color.BLACK if isWhite else Color.WHITE] > 0)
                        else 1
                    )
                )
                if isWhite:
                    if i - last_controlled_sq[0] > 12:
                        score += -10
                else:
                    if last_controlled_sq[1] - i > 12:
                        score += +10

            # squares controlled
            if pieces >= 2:
                squares_controlled[0 if isWhite else 1] += 3 * important_factor

            # keep track the number of pieces
            if isWhite:
                white_pieces += self.board[i] * important_factor
            else:
                black_pieces += -self.board[i] * important_factor

            # the more pieces you have in the start have a small penalty
            if quarter == 3:
                score += 2.5 * (1 if isWhite else -1) * pieces

        # update score based of the number of pieces
        score += -white_pieces
        score -= -black_pieces

        # udpate score based of captured pieces
        score += -(self.cuptured[Color.WHITE] - self.cuptured[Color.BLACK]) * 20

        # update based of the controlled squares
        score += 10 * (squares_controlled[0] - squares_controlled[1])

        # the closer to the end the better
        # the more linear distribution on end the better
        # the single pieces where opponent has at least 1 piece before is bad
        # MORE
        return score

    def Evalutate(self) -> float:
        # TODO later implement with a depth
        return self.GetCost()

    def GetBestMovesForDices(self) -> tuple[list[Action], float]:
        assert self.dices != [-1, -1], "You must roll the dices before making a move"
        # for each move combination that can be done, calculate the Evaluate and return the best one
        best_moves: list[Action] = []
        best_score = -float("inf")

        def UpdateBest(board: "Board", moves: list[Action]):
            nonlocal best_score, best_moves
            score = board.Evalutate()
            if score > best_score:
                best_score = score
                best_moves = moves

        actions1 = self.GetAvailableActions()
        if {RollDiceAction()} not in actions1 and len(self.translations) > 0:
            for a1 in actions1:
                tmpBoard1 = Board.From(self)
                tmpBoard1.ExecuteAction(a1)
                actions2 = tmpBoard1.GetAvailableActions()
                if {RollDiceAction()} not in actions2 and len(tmpBoard1.translations) > 0:
                    for a2 in actions2:
                        tmpBoard2 = Board.From(tmpBoard1)
                        tmpBoard2.ExecuteAction(a2)
                        actions3 = tmpBoard2.GetAvailableActions()

                        if {RollDiceAction()} not in actions3 and len(tmpBoard2.translations) > 0:
                            for a3 in actions3:
                                tmpBoard3 = Board.From(tmpBoard2)
                                tmpBoard3.ExecuteAction(a3)
                                actions4 = tmpBoard3.GetAvailableActions()

                                if {RollDiceAction()} not in actions4 and len(tmpBoard3.translations) > 0:
                                    for a4 in actions4:
                                        tmpBoard4 = Board.From(tmpBoard3)
                                        tmpBoard4.ExecuteAction(a4)

                                        UpdateBest(tmpBoard4, [a1, a2, a3, a4])
                                else:
                                    UpdateBest(tmpBoard3, [a1, a2, a3])
                        else:
                            UpdateBest(tmpBoard2, [a1, a2])
                else:
                    UpdateBest(tmpBoard1, [a1])
        else:
            UpdateBest(self, [])

        return best_moves, best_score
