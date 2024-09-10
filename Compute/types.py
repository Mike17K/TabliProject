from enum import Enum


class GameState(Enum):
    NOT_STARTED = 0
    WHITE_MOVES = 1
    WHITE_ROLLS = 2
    BLACK_MOVES = 3
    BLACK_ROLLS = 4
    WHITE_WINS = 5
    BLACK_WINS = 6


class Color(Enum):
    WHITE = 0
    BLACK = 1


class ActionType(Enum):
    MOVE = 0
    REMOVE = 1
    PLACE = 2
    ROLL_DICE = 3


class Action:
    def __init__(self) -> None:
        super().__init__()
        self.type: ActionType | None = None

    def Validate(self) -> bool:
        return NotImplemented

    def __hash__(self):
        return NotImplemented

    def __eq__(self, other):
        return NotImplemented


class MoveAction(Action):
    def __init__(self, from_index: int, to_index: int):
        self.type: ActionType = ActionType.MOVE
        self.from_index = from_index
        self.to_index = to_index

    def Validate(self) -> bool:
        return 0 <= self.from_index < 24 and 0 <= self.to_index < 24

    def __hash__(self):
        return hash((self.type, self.from_index, self.to_index))

    def __eq__(self, other):
        if other is None:
            return False
        assert isinstance(other, MoveAction)
        return (
            self.type == other.type
            and self.from_index == other.from_index
            and self.to_index == other.to_index
        )


class RemoveAction(Action):
    def __init__(self, index_to_remove: int):
        self.type: ActionType = ActionType.REMOVE
        self.index_to_remove = index_to_remove

    def Validate(self) -> bool:
        return 0 <= self.index_to_remove < 24

    def __hash__(self):
        return hash((self.type, self.index_to_remove))

    def __eq__(self, other):
        if other is None:
            return False
        assert isinstance(other, RemoveAction)
        return self.type == other.type and self.index_to_remove == other.index_to_remove


class PlaceAction(Action):
    def __init__(self, to_index: int):
        self.type: ActionType = ActionType.PLACE
        self.to_index = to_index

    def Validate(self) -> bool:
        return 0 <= self.to_index < 24

    def __hash__(self):
        return hash((self.type, self.to_index))

    def __eq__(self, other):
        if other is None:
            return False
        assert isinstance(other, PlaceAction)
        return self.type == other.type and self.to_index == other.to_index


class RollDiceAction(Action):
    def __init__(self):
        self.type: ActionType = ActionType.ROLL_DICE

    def Validate(self) -> bool:
        return True

    def __hash__(self):
        return hash(self.type)

    def __eq__(self, other):
        if other is None:
            return False
        assert isinstance(
            other, RollDiceAction
        ), "RollDiceAction can only be compared with RollDiceAction"
        return self.type == other.type
