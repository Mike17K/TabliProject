from enum import Enum

class Color(Enum):
    WHITE = 0
    BLACK = 1

class Action(Enum):
    MOVE = 0
    REMOVE = 1
    PLACE = 2
    def __init__(self) -> None:
        super().__init__()
        self.type: Action = None
    def Validate(self) -> bool:
        return False

class MoveAction(Action):
    def __init__(self, from_index: int, to_index: int):
        self.type: Action = Action.MOVE
        self.from_index = from_index
        self.to_index = to_index
    
    def Validate(self) -> bool:
        return 0<=self.from_index<24 and 0<=self.to_index<24
    
class RemoveAction(Action):
    def __init__(self, index: int):
        self.type: Action = Action.REMOVE
        self.index = index
    
    def Validate(self) -> bool:
        return 0<=self.index<24
    
class PlaceAction(Action):
    def __init__(self, to_index: int):
        self.type: Action = Action.PLACE
        self.to_index = to_index
    
    def Validate(self) -> bool:
        return 0<=self.index<24