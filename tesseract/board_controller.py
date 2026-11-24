from tesseract.board_model import BoardModel
from tesseract.board_command import BoardCommand

class BoardController:
    """
    Manage the 4D TUI with arrows + WASD + shuffle + order
    """

    def __init__(self, board_model: BoardModel):
        self._board_model = board_model
        
    def get_board_model(self)->BoardModel:
        return self._board_model

    def is_legal(self, board_cmd: BoardCommand)->bool:
        if board_cmd == BoardCommand.NOP:
            return True
        return False
        
    def process_command(self, board_cmd: BoardCommand)->None:
        pass
