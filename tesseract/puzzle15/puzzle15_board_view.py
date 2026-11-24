from tesseract.board_controller import BoardController
from tesseract.board_view import BoardView, VirtualTextualScreen
from tesseract.board_command import BoardCommand

class Puzzle15BoardView(BoardView):
    CELL_WIDTH = 2
    CELL_HEIGHT = 1
    CELL_DIAG_LEFT = 1
    CELL_DIAG_RIGHT = 2
    
    def __init__(self,
        board_controller: BoardController,
        virtual_screen: VirtualTextualScreen):
        super().__init__(
            board_controller,
            virtual_screen,
            self.CELL_WIDTH,
            self.CELL_HEIGHT,
            self.CELL_DIAG_LEFT,
            self.CELL_DIAG_RIGHT)
