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

    def parse_input(self, inp)->BoardCommand:
        cmd = BoardCommand.NOP
        if inp == 65:
            cmd = BoardCommand.MOVE_UP
        elif inp == 66:
            cmd = BoardCommand.MOVE_DOWN
        elif inp == 67:
            cmd = BoardCommand.MOVE_RIGHT
        elif inp == 68:
            cmd = BoardCommand.MOVE_LEFT
        elif inp == ord('w'):
            cmd = BoardCommand.MOVE_UPSQ
        elif inp == ord('s'):
            cmd = BoardCommand.MOVE_DOWNSQ
        elif inp == ord('d'):
            cmd = BoardCommand.MOVE_RIGHTSQ
        elif inp == ord('a'):
            cmd = BoardCommand.MOVE_LEFTSQ
        elif inp == 10 or inp == ord(' '):
            cmd = BoardCommand.MOVE_SHUFFLE
        elif inp == ord('o'):
            cmd = BoardCommand.MOVE_ORDER
        return cmd

        
    def get_next_command_from_input(self)->BoardCommand:
        while True:
            c = self.getch()
            if ord(c) == 91 or ord(c) == 27:
                continue
            cmd = self.parse_input(ord(c))
            return cmd

