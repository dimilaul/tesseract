from tesseract.board_view import BoardView

class Puzzle15SimplifiedBoardView(BoardView):
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
