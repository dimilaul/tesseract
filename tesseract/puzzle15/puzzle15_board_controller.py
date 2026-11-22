from tesseract.board_controller import BoardController

class Puzzle15BoardController(BoardController):
    """
    Manage the Puzzle15 game with arrows + WASD + shuffle + order
    """

    def __init__(self):
        self._board_model = None
        
    def set_board_model(self, board_model: BoardModel)->None:
        self._board_model = board_model
        
    def get_board_model(self)->BoardModel:
        return self._board_model

    def is_legal(self, board_cmd: BoardCommand)->bool:
        if cmd == BoardCommand.NOP:
            return True
        return False
        
    def process_command(self, board_cmd: BoardCommand)->None:
        pass
