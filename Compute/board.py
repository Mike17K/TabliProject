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
            # 2,0,0,0,0,-5,0,-3,0,0,0,5,-5,0,0,0,3,0,5,0,0,0,0,-2,
            -2,
            -2,
            -2,
            -3,
            -3,
            -3,
            0,
            0,
            0,
            0,
            -1,
            0,
            0,
            0,
            1,
            0,
            0,
            0,
            0,
            2,
            2,
            3,
            3,
            3,
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
        print(self, action, self.action_to_get_this_state, len(Board.HISTORY))
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
            print("calculating available moves")
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
        if len(self.translations) == 0 or (
            self.available_moves_calculated and len(self.available_moves) == 0
        ):
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
            print(
                "other plays, data: ",
                self.dices,
                self.translations,
                self.GetAvailableActions(),
            )
            newBoard.is_white_turn = not self.is_white_turn
            newBoard.dices = [-1, -1]
            newBoard.translations = []
            newBoard.available_moves_calculated = False
            newBoard.available_moves = set()
        print("New state", newBoard.GetState())

        Board.HISTORY.append(newBoard)

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
        print("getActionsForDice", dice)
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
            print("state for removing pieces")
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

    def GetBestMovesForDices(self) -> tuple[Action, float]:
        pass  # TODO
