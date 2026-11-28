class TerminalScreen:
    def __init__(self, screen: VirtualTextualScreen):
        self._screen = screen
        self.draw_empty_screen()

    def draw_empty_screen(self)->None:
        screen_height = self._screen.get_height()
        for i in range(screen_height):
            print()
            
    def draw_screen(self)->None:
        for y in range(self._screen.get_height()):
            screen_line = ""
            for x in range(self._screen.get_width()):
                char, background, foreground = self._screen.get_cell(x, y)
                screen_line += char
            print(screen_line)

