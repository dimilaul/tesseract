from tesseract.puzzle15.puzzle15_board_model import Puzzle15BoardModel
from tesseract.puzzle15.puzzle15_board_view import Puzzle15BoardView
from tesseract.puzzle15.puzzle15_board_controller import Puzzle15BoardController

if __name__ == "__main__":
    model = Puzzle15BoardModel(2, 1, 1, 1)
    view = Puzzle15BoardView()
    controller = Puzzle15BoardController()
