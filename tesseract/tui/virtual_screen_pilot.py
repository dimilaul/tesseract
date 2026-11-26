from tesseract.board_model import BoardModel
from tesseract.board_controller import BoardController
from tesseract.board_view import BoardView, VirtualTextualScreen
from tesseract.tui.terminal.terminal_control import TerminalControl
from tesseract.tui.terminal.terminal_screen import TerminalScreen
from tesseract.tui.keyboard_control import KeyboardControl
from tesseract.board_command import BoardCommand
from tesseract.textual_color import TextualColor

class VirtualScreenPilotModel(BoardModel):
    def __init__(self):
        super().__init__(1,1,1,1)
        
class VirtualScreenPilotController(BoardController):
    def __init__(self):
        super().__init__(VirtualScreenPilotModel())
        
    def is_legal(self, board_cmd: BoardCommand)->bool:
        return True
        
    def process_command(self, board_cmd: BoardCommand)->None:
        self._board_model.set_cell(0, 0, 0, 0, board_cmd.value)

class VirtualScreenPilotView(BoardView):
    def __init__(self):
        super().__init__(VirtualScreenPilotController(), VirtualTextualScreen(1, 1), 0, 0, 0, 0)
        
    def draw_on_virtual_screen(self):
        char_value = chr(ord('0') + self._board_controller.get_board_model().get_cell(0,0,0,0))
        self._screen.set_cell(0, 0, char_value, TextualColor.BLACK, TextualColor.WHITE)

def main():
    view = VirtualScreenPilotView()
    
    terminal_screen = TerminalScreen()
    terminal_screen.draw_empty_screen(view.get_screen())
    view.draw_on_virtual_screen()
    terminal_screen.draw_screen(view.get_screen())
    
    keyboard_control = KeyboardControl()
    while True:
        cmd = keyboard_control.get_next_command_from_input()
        if cmd != BoardCommand.NOP:
            view.process_command(cmd)
            view.draw_on_virtual_screen()
            terminal_screen.draw_screen(view.get_screen())
    
if __name__ == "__main__":
    main()
