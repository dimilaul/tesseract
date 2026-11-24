from tesseract.board_model import BoardModel
from tesseract.board_controller import BoardController
from tesseract.board_view import BoardView, VirtualTextualScreen

class VirtualScreenPilotModel(BoardModel):
    def __init__(self):
        super().__init__(1,1,1,1)
        
class VirtualScreenPilotController(BoardController):
    def __init__(self):
        super().__init__(VirtualScreenPilotModel())
    
class VirtualScreenPilotView(BoardView):
    def __init__(self):
        super().__init__(VirtualScreenPilotController(), VirtualTextualScreen(1, 1), 0, 0, 0, 0)

def main():
    view = VirtualScreenPilotView()
    print("OK")

if __name__ == "__main__":
    main()
