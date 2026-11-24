from tesseract.board_view import TextualColor

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
    
    def __init__():
        pass
    
    def background_color_to_terminal_command(self, color: TextualColor)->str:
        if color == TextualColor.BLACK:
            return BG_BLACK
        if color == TextualColor.GREEN:
            return BG_GREEN
        if color == TextualColor.BG_CYAN:
            return BG_CYAN
        return ""
        
    def foreground_color_to_terminal_command(color: TextualColor)->str:
        if color == TextualColor.RED:
            return FG_RED
        if color == TextualColor.GREEN:
            return FG_GREEN
        if color == TextualColor.CYAN:
            return FG_CYAN
        if color == TextualColor.BLACK:
            return FG_BLACK

        return ""

    def surround_in_background(self, a_str: str, color: TextualColor)->str:
        if color == TextualColor.BLACK:
            return a_str
        return f"{self.background_color_to_terminal_command(color)}{a_str}{BG_BLACK}"

    def surround_in_foreground(self, a_str: str, color: TextualColor)->str:
        if color == TextualColor.WHITE:
            return a_str
        return f"{self.forreground_color_to_terminal_command(color)}{a_str}{FG_WHITE}"
