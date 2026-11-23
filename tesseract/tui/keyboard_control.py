import sys
import termios
import tty

from tesseract.board_command import BoardCommand

class KeyboardControl:
    def __init__(self):
        pass
        

    def getch(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
        # Use cbreak mode to keep Ctrl+C signal handling active
            tty.setcbreak(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def parse_input(self, inp):
        move = 0
        if inp == 65:
            move = BoardCommand.MOVE_UP.value
        elif inp == 66:
            move = BoardCommand.MOVE_DOWN.value
        elif inp == 67:
            move = BoardCommand.MOVE_RIGHT.value
        elif inp == 68:
            move = BoardCommand.MOVE_LEFT.value
        elif inp == ord('w'):
            move = BoardCommand.MOVE_UPSQ.value
        elif inp == ord('s'):
            move = BoardCommand.MOVE_DOWNSQ.value
        elif inp == ord('d'):
            move = BoardCommand.MOVE_RIGHTSQ.value
        elif inp == ord('a'):
            move = BoardCommand.MOVE_LEFTSQ.value
        elif inp == 10 or inp == ord(' '):
            move = BoardCommand.MOVE_SHUFFLE.value
        elif inp == ord('o'):
            move = BoardCommand.MOVE_ORDER.value
        return move

        
    def get_next_command_from_input(self)->BoardCommand:
        while True:
            c = self.getch()
            if ord(c) == 91 or ord(c) == 27:
                continue
            cmd = self.parse_input(ord(c))
            return cmd

