from typing import Optional

from tesseract.board_model import BoardModel
from tesseract.board_controller import BoardController
from tesseract.board_view import BoardView, VirtualTextualScreen
from tesseract.tui.terminal.terminal_control import TerminalControl
from tesseract.tui.terminal.terminal_screen import TerminalScreenRenderer
from tesseract.tui.keyboard_control import KeyboardControl
from tesseract.board_command import BoardCommand
from tesseract.textual_color import TextualColor

class VirtualScreenPilotModel(BoardModel):
    def __init__(self):
        super().__init__(3,3,1,1)
        self._head = (0, 0, 0, 0)

    def can_move_up(self)->bool:
        return self._head[1] > 0

    def can_move_down(self)->bool:
        return self._head[1] < 2

    def can_move_left(self)->bool:
        return self._head[0] > 0 

    def can_move_right(self)->bool:
        return self._head[0] < 2    

    def  move_up(self)->None:
        if self.can_move_up():
            self._head = (self._head[0], self._head[1]-1, self._head[2], self._head[3])

    def move_down(self)->None:
        if self.can_move_down():
            self._head = (self._head[0], self._head[1]+1, self._head[2], self._head[3])

    def move_left(self)->None:
        if self.can_move_left():
            self._head = (self._head[0]-1, self._head[1], self._head[2], self._head[3]) 

    def move_right(self)->None:
        if self.can_move_right():
            self._head = (self._head[0]+1, self._head[1], self._head[2], self._head[3]) 

        
class VirtualScreenPilotController(BoardController):
    def __init__(self):
        super().__init__(VirtualScreenPilotModel())
        
    def is_legal(self, board_cmd: BoardCommand)->bool:
        if board_cmd == BoardCommand.NOP:
            return True
        if board_cmd == BoardCommand.MOVE_DOWN:
            return self.get_board_model().can_move_down()
        elif board_cmd == BoardCommand.MOVE_UP:
            return self.get_board_model().can_move_up()
        elif board_cmd == BoardCommand.MOVE_LEFT:
            return self.get_board_model().can_move_left()
        elif board_cmd == BoardCommand.MOVE_RIGHT:
            return self.get_board_model().can_move_right()
        else:
            return False
        
    def _apply_command(self, board_cmd: BoardCommand)->bool:
        if board_cmd == BoardCommand.MOVE_DOWN:
            if self._board_model.can_move_down():
                self._board_model.move_down()
                return True
            return False
        elif board_cmd == BoardCommand.MOVE_UP:
            if self._board_model.can_move_up():
                self._board_model.move_up()
                return True
            return False
        elif board_cmd == BoardCommand.MOVE_LEFT:
            if self._board_model.can_move_left():
                self._board_model.move_left()
                return True
            return False
        elif board_cmd == BoardCommand.MOVE_RIGHT:
            if self._board_model.can_move_right():
                self._board_model.move_right()
                return True
            return False
        else:
            self._board_model.set_cell(0, 0, 0, 0, board_cmd.value)
            return True

class VirtualScreenPilotView(BoardView):
    def __init__(
        self,
        board_controller: Optional[BoardController] = None,
        virtual_screen: Optional[VirtualTextualScreen] = None,
    ):
        controller = board_controller if board_controller is not None else VirtualScreenPilotController()
        screen = virtual_screen if virtual_screen is not None else VirtualTextualScreen(3, 3)
        super().__init__(controller, screen, 0, 0, 0, 0)
        
    def _render_board(self):
        char_value = chr(ord('0') + self._board_controller.get_board_model().get_cell(0,0,0,0))
        for y in range(0, 3):
            for x in range(0, 3):
                if (x, y) == self._board_controller.get_board_model()._head[0:2]:
                    self._screen.set_cell(x, y, char_value, TextualColor.WHITE, TextualColor.BLACK)
                else:
                    self._screen.set_cell(x, y, ' ', TextualColor.BLACK, TextualColor.WHITE)

def main():
    controller = VirtualScreenPilotController()
    screen = VirtualTextualScreen(3, 3)
    terminal_renderer = TerminalScreenRenderer(screen)
    view = VirtualScreenPilotView(controller, screen)
    view.render()
    
    keyboard_control = KeyboardControl()
    while True:
        cmd = keyboard_control.get_next_command_from_input()
        if cmd != BoardCommand.NOP:
            controller.process_command(cmd)
    
if __name__ == "__main__":
    main()
