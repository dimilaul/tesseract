from tesseract.board_view import BoardView
from tesseract.board_command import BoardCommand

class Puzzle15BoardView(BoardView):
    CELL_WIDTH = 2
    CELL_HEIGHT = 1
    CELL_DIAG_LEFT = 1
    CELL_DIAG_RIGHT = 2
    
    def __init__(self,
        board_controller: BoardController,
        virtual_screen: VirtualTextualScreen,
        super.__init__(
            board_controller,
            virtual_screen,
            CELL_WIDTH,
            CELL_HEIGHT,
            CELL_DIAG_LEFT,
            CELL_DIAG_RIGHT)
