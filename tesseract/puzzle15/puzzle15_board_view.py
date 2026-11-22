from tesseract.board_view import BoardView
from tesseract.board_command import BoardCommand

class Puzzle15BoardView(BoardView):
    """
    ASCII-graphical representation of a 4D puzzle15 board
    """
    
    def __init__(self):
        self._board_controller = None
    
    def set_board_controller(self, board_controller: BoardController)->None:
        self._board_controller = board_controller
        
    def read_button_click(self)->BoardCommand:
        line=input(">")
        return BoardCommand.NOP
    
    def is_legal(self, board_cmd: BoardCommand)->bool:
        return self._board_controller.is_legal
        
    def process_command(self, board_cmd: BoardCommand)->None:
        self._board_controller.process_command(board_cmd)
        
    def report_illegal_command(self, board_cmd: BoardCommand)->None:
        pass
    
    def draw(self):
        board_model = self._board_controller.get_board_model()
        print(f"BOARD: {board_model}")
