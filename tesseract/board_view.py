from tesseract.board_model import BoardModel

class BoardView:
    """
    Generic ASCII-graphical representation of a 4D board
    """
    def __init__(self, width=80, height=40, cell_width=1, cell_height = 1, cell_left_diag_span = 1, cell_right_diag_span = 2):
        self._height = height
        self._width = width
        self._view = []
        self.clear_view()
        self._cell_height = cell_height
        self._cell_width = cell_width
        self._cell_left_diag_span = cell_left_diag_span
        self._cell_right_diag_span = cell_right_diag_span
        
    def clear_view(self)->None:
        self._view = []
        for i in range(0, self._height):
            line = ''
            for i in range(0, self._width):
                line += ' '
            self._view.append(line)
            
    def draw_board(self, board_model: BoardModel)->None:
        self._view[0, 0] = str(board_model._array[0])
        self._view[0, 1] = str(board_model._array[1])
        pass
        
    
        
