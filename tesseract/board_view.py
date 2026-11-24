from tesseract.board_model import BoardModel
from enum import Enum
from tesseract.board_controller import BoardController

class TextualColor(Enum):
    """
    Basic colors that are supported in Linux terminal emulator
    """
    BLACK = 0
    GREEN = 1
    CYAN = 2
    RED = 3
    WHITE = 4

class VirtualTextualScreen:
    """
    Textual representation of the screen
    """

    def init(self, height, weight):
        self._height = height
        self._width = width
        self._screen_matrix : list[list[tuple[char, color, color]]] = []
        self.clear()
        
    def clear(self):
        self._screen_matrix = [[(' ', TextualColor.BLACK, TextualColor.BLACK) for i in range(0, self._width)] for j in range(0, self._height)]

    def set_cell(x: int, y: int, c: char, bg_color: TextualColor, fg_color: TextualColor)->None:
        if x not in range(0, self._width):
            raise Exception(f"cannot set x out of range: {x}")
        if y not in range(0, self.height):
            raise Exception(f"cannot set y out of range: {y}")
        self._screen_matrix[y][x] = (c, bg_color, fg_color)
        
    def get_cell(x: int, y: int)->tuple[char, TextualColor, TextualColor]:
        return self._screen_matrix[y][x]

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
        
        self._screen = screen
        self._cell_height = cell_height
        self._cell_width = cell_width
        self._cell_left_diag_span = cell_left_diag_span
        self._cell_right_diag_span = cell_right_diag_span
        self._board_controller = board_controller
        
    def clear_view(self)->None:
        self._view = []
        for i in range(0, self._height):
            line = ''
            for i in range(0, self._width):
                line += ' '
            self._view.append(line)
            
    def draw_board_on_virtual_screen(self)->None:
        pass
        
    def draw_virtual_screen(self)->None:
        pass

    def is_legal(self, board_cmd: BoardCommand)->bool:
        return self._board_controller.is_legal
        
    def process_command(self, board_cmd: BoardCommand)->None:
        self._board_controller.process_command(board_cmd)
        
    def report_illegal_command(self, board_cmd: BoardCommand)->None:
        pass


