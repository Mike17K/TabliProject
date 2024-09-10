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
        ]
        self.cuptured: dict[Color, int] = {Color.WHITE: 0, Color.BLACK: 0}
        self.action_to_get_this_state: Action | None = None
        self.is_white_turn = True
        self.dices = [-1, -1]

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
        assert abs(from_index - to_index) in self.dices
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

        self.dices.remove(abs(from_index - to_index))

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
        if (requestedDice) in self.dices:
            self.dices.remove(requestedDice)
        else:
            assert maxPieceIndex == requestedDice
            self.dices.remove(max(self.dices))

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
            (24 - to_index) in self.dices
            if color == Color.WHITE
            else (to_index + 1) in self.dices
        )

        if (24 - to_index) in self.dices and color == Color.WHITE:
            self.dices.remove(24 - to_index)
        elif (to_index + 1) in self.dices and color == Color.BLACK:
            self.dices.remove(to_index + 1)

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
            self.dices += [dice1, dice1]


class Board(BoardState):

    HISTORY: list["Board"] = []

    @staticmethod
    def From(old: "Board") -> "Board":
        newBoard = Board()
        newBoard.board = old.board.copy()
        newBoard.cuptured = old.cuptured.copy()
        newBoard.is_white_turn = old.is_white_turn
        newBoard.dices = old.dices.copy()
        return newBoard

    def __init__(self):
        super().__init__()
        self.state: GameState = GameState.NOT_STARTED

        self.available_moves_calculated = False
        self.available_moves: set[Action] = set()

    def GetAvailableMoves(self) -> set[Action]:
        if not self.available_moves_calculated:
            self.available_moves = self.CalculateAvailableActions()
        return self.available_moves

    def GetState(self) -> GameState:
        piece_count = [0, 0]  # white, black
        for i in range(24):
            if self.board[i] > 0:
                piece_count[0] += 1
            if self.board[i] < 0:
                piece_count[1] += 1
        if piece_count[0] == 0:
            return GameState.WHITE_WINS
        if piece_count[1] == 0:
            return GameState.BLACK_WINS

        if self.dices == [-1, -1]:
            return (
                GameState.WHITE_ROLLS if self.is_white_turn else GameState.BLACK_ROLLS
            )
        if Board.HISTORY[-1] != self:
            return self.state
        # if moved pieces are equal to the final results then call it done
        if len(self.dices) == 0 or len(self.GetAvailableMoves()) == 0:
            return (
                GameState.BLACK_ROLLS if self.is_white_turn else GameState.WHITE_ROLLS
            )

        return GameState.WHITE_MOVES if self.is_white_turn else GameState.BLACK_MOVES

    def Commit(self) -> "Board":
        assert self.action_to_get_this_state != None

        newBoard = Board.From(self)
        Board.HISTORY.append(newBoard)

    @staticmethod
    def Undo():
        if len(Board.HISTORY) > 1:
            Board.HISTORY.pop()
            return True
        return False

    @staticmethod
    def Now() -> "Board":
        return Board.HISTORY[-1] if len(Board.HISTORY) > 0 else Board()

    ################ Functions Helper #################

    def GetBestMoveForDices(self) -> tuple[Action, float]:
        pass

    def CalculateAvailableActions(self) -> set[Action]:
        return []
