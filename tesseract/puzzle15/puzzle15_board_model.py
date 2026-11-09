from tesseract.board_model import BoardModel

class Puzzle15BoardModel(BoardModel):
    """
    Puzzle 15 board represented as flat/linear array
    """
    def _initial_array(self):
        super._initial_array()
        self._array = [i+1 for i in range(0, len(self._array))]

    def __init__():
        super.__init__(4, 4, 4, 4)
