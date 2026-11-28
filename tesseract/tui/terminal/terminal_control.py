
from tesseract.board_view import TextualColor
from tesseract.board_view import VirtualTextualScreen

class TerminalControl:
    BOARD_TUI_HEIGHT = 12


    # ansi term colors
    BG_BLACK = "\033[40m"
    BG_GREEN = "\033[42m"
    BG_CYAN = "\033[46m"
    FG_RED = "\033[31m"
    FG_GREEN = "\033[33m"
    FG_CYAN = "\033[36m"
    FG_WHITE = "\033[37m"
    FG_BLACK = "\033[30m"
    TERMCOLOR_RESET = "\033[0m"
    
    def __init__(self):
        pass
    
    def background_color_to_terminal_command(self, color: TextualColor)->str:
        if color == TextualColor.BLACK:
            return self.BG_BLACK
        if color == TextualColor.GREEN:
            return self.BG_GREEN
        if color == TextualColor.CYAN:
            return self.BG_CYAN
        return ""
        
    def foreground_color_to_terminal_command(self, color: TextualColor)->str:
        if color == TextualColor.RED:
            return self.FG_RED
        if color == TextualColor.GREEN:
            return self.FG_GREEN
        if color == TextualColor.CYAN:
            return self.FG_CYAN
        if color == TextualColor.BLACK:
            return self.FG_BLACK

        return ""

    def surround_in_background(self, a_str: str, color: TextualColor)->str:
        if color == TextualColor.BLACK:
            return a_str
        return f"{self.background_color_to_terminal_command(color)}{a_str}{self.BG_BLACK}"

    def surround_in_foreground(self, a_str: str, color: TextualColor)->str:
        if color == TextualColor.WHITE:
            return a_str
        return f"{self.foreground_color_to_terminal_command(color)}{a_str}{self.FG_WHITE}"
        
    def get_header_line(self, height: int, background_color: TextualColor)->str:
        header_line = f"\033[{height}A{self.background_color_to_terminal_command(background_color)}\r"
        return header_line

    def get_footer_line(self)->str:
        footer_line = self.TERMCOLOR_RESET
        return footer_line

