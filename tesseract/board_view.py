from tesseract.board_model import BoardModel
from enum import Enum
from tesseract.board_controller import BoardController
from tesseract.board_command import BoardCommand
from tesseract.virtual_textual_screen import VirtualTextualScreen
from tesseract.textual_color import TextualColor

class BoardView:
    """
    Generic ASCII-graphical representation of a 4D board
    """
    def __init__(self,
        board_controller: BoardController,
        virtual_screen: VirtualTextualScreen,
        cell_width: int = 2,
        cell_height:int = 1,
        cell_left_diag_span: int = 1,
        cell_right_diag_span: int = 2):
        
        self._screen = virtual_screen
        self._cell_height = cell_height
        self._cell_width = cell_width
        self._cell_left_diag_span = cell_left_diag_span
        self._cell_right_diag_span = cell_right_diag_span
        self._board_controller = board_controller
        
    def clear_view(self)->None:
        self._screen.clear()
            
    def draw_board_on_virtual_screen(self)->None:
        pass
        
    def draw_virtual_screen(self)->None:
        pass

    def is_legal(self, board_cmd: BoardCommand)->bool:
        return self._board_controller.is_legal(board_cmd)
        
    def process_command(self, board_cmd: BoardCommand)->None:
        self._board_controller.process_command(board_cmd)
        
    def report_illegal_command(self, board_cmd: BoardCommand)->None:
        pass
        
    def get_screen(self)->VirtualTextualScreen:
        return self._screen


