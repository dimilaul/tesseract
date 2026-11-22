from tesseract.puzzle15.puzzle15_board_model import Puzzle15BoardModel
from tesseract.puzzle15.puzzle15_board_view import Puzzle15BoardView
from tesseract.puzzle15.puzzle15_board_controller import Puzzle15BoardController

if __name__ == "__main__":
    model = Puzzle15BoardModel(2, 1, 1, 1)
    view = Puzzle15BoardView()
    controller = Puzzle15BoardController()
    
    controller.set_board_model(model)
    view.set_board_controller(controller)
    
    view.draw()
    while True:
        command = view.read_button_click()
        if view.is_legal(command):
            view.process_command(command)
            view.draw()
        else:
            view.report_illegal_command(command)
        
        
