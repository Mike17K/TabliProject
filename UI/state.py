from Compute.board import Board

class UIState:
    INSTANCE = None

    def __init__(self):
        # reset the board
        Board.HISTORY = []
        board = Board()
        board.Commit()

        self.holding_piece = None
        self.holding_piece_previews_index = None
        self.running = True
        self.is_white_turn = True

    @staticmethod
    def get_instance():
        if UIState.INSTANCE is None:
            UIState.INSTANCE = UIState()
        return UIState.INSTANCE

    def get_board(self) -> Board:
        # get the current board
        return Board.HISTORY[-1]