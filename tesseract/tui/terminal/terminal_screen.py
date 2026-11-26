class TerminalScreen:
    def __init__(self):
        pass

    def draw_empty_screen(self, screen: VirtualTextualScreen)->None:
        screen_height = screen.get_height()
        for i in range(screen_height):
            print()
            
    def draw_screen(self, screen: VirtualTextualScreen)->None:
        for y in range(screen.get_height()):
            screen_line = ""
            for x in range(screen.get_width()):
                char, background, foreground = screen.get_cell(x, y)
                screen_line += char
            print(screen_line)

