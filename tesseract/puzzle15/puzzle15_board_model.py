from tesseract.board_model import BoardModel

class Puzzle15BoardStatus:
    STATUS_INITIAL = 0
    STATUS_MOVED = 1
    STATUS_ILLEGAL_MOVE = 2
    STATUS_SOLVED = 3
    STATUS_SHUFFLED = 4

class Puzzle15BoardModel(BoardModel):
    """
    Puzzle 15 board represented as flat/linear array
    """
    def _initialize_array(self):
        super()._initialize_array()
        self._array = [i+1 for i in range(0, len(self._array))]

