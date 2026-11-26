class TerminalScreen:
    def __init__(self):
        pass

    def draw_empty_screen(self, screen: VirtualTextualScreen)->None:
        screen_height = screen.get_height()
        for i in range(screen_height):
            print()
            
    def draw_screen(self, screen: VirtualTextualScreen)->None:
        for i in range(screen.get_height()):
            print("board_print")

