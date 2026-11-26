from tesseract.board_model import BoardModel
from tesseract.board_controller import BoardController
from tesseract.board_view import BoardView, VirtualTextualScreen
from tesseract.tui.terminal import TerminalControl, TerminalScreenDraw
from tesseract.tui.keyboard_control import KeyboardControl
from tesseract.board_command import BoardCommand

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
    
    terminal_screen = TerminalScreenDraw()
    terminal_screen.draw_empty_screen(view.get_screen())
    terminal_screen.draw_screen(view.get_screen())
    
    keyboard_control = KeyboardControl()
    while True:
        cmd = keyboard_control.get_next_command_from_input()
        if cmd != BoardCommand.NOP:
            terminal_screen.draw_screen(view.get_screen())

    
    print("OK")

if __name__ == "__main__":
    main()
