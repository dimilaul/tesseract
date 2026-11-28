
from tesseract.board_view import TextualColor
from tesseract.board_view import VirtualTextualScreen

class TerminalControl:
    BOARD_TUI_HEIGHT = 12


    # ansi term colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    BG_DEFAULT = "\033[49m"
    FG_RED = "\033[31m"
    FG_GREEN = "\033[33m"
    FG_CYAN = "\033[36m"
    FG_WHITE = "\033[37m"
    FG_BLACK = "\033[30m"
    FG_DEFAULT = "\033[39m"
    TERMCOLOR_RESET = "\033[0m"

    _BG_COLOR_COMMANDS = {
        TextualColor.BLACK: BG_BLACK,
        TextualColor.GREEN: BG_GREEN,
        TextualColor.CYAN: BG_CYAN,
        TextualColor.RED: BG_RED,
        TextualColor.WHITE: BG_WHITE,
    }

    _FG_COLOR_COMMANDS = {
        TextualColor.BLACK: FG_BLACK,
        TextualColor.GREEN: FG_GREEN,
        TextualColor.CYAN: FG_CYAN,
        TextualColor.RED: FG_RED,
        TextualColor.WHITE: FG_WHITE,
    }
    
    def __init__(self):
        pass
    
    def background_color_to_terminal_command(self, color: TextualColor)->str:
        return self._BG_COLOR_COMMANDS.get(color, "")
        
    def foreground_color_to_terminal_command(self, color: TextualColor)->str:
        return self._FG_COLOR_COMMANDS.get(color, "")

    def surround_in_background(self, a_str: str, color: TextualColor)->str:
        cmd = self.background_color_to_terminal_command(color)
        if not cmd:
            return a_str
        return f"{cmd}{a_str}{self.BG_DEFAULT}"

    def surround_in_foreground(self, a_str: str, color: TextualColor)->str:
        cmd = self.foreground_color_to_terminal_command(color)
        if not cmd:
            return a_str
        return f"{cmd}{a_str}{self.FG_DEFAULT}"

    def raise_lines(self, num_lines: int)->str:
        if num_lines <= 0:
            return ""
        return f"\033[{num_lines}A"
        
    def get_header_line(self, height: int, background_color: TextualColor)->str:
        header_line = f"{self.raise_lines(height)}{self.background_color_to_terminal_command(background_color)}\r"
        return header_line

    def get_footer_line(self)->str:
        footer_line = self.TERMCOLOR_RESET
        return footer_line

