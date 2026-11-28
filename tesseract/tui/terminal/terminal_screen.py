
from typing import Optional

from tesseract.event_queue import EventQueue
from tesseract.virtual_textual_screen import VirtualTextualScreen
from tesseract.tui.terminal.terminal_control import TerminalControl
from tesseract.screen_renderer import ScreenRenderer

class TerminalScreenRenderer(ScreenRenderer):
    def __init__(self, screen: VirtualTextualScreen, event_queue: Optional[EventQueue] = None):
        super().__init__(screen, event_queue)
        self._terminal_control = TerminalControl()
        self.clear()

    def clear(self)->None:
        screen_height = self._screen.get_height()
        for i in range(screen_height):
            print()
            
    def render(self)->None:
        height = self._screen.get_height()
        if height > 0:
            print(self._terminal_control.raise_lines(height), end="\r")
        for y in range(height):
            screen_line = ""
            for x in range(self._screen.get_width()):
                char, background, foreground = self._screen.get_cell(x, y)
                screen_line += self._terminal_control.surround_in_background(self._terminal_control.surround_in_foreground(char, foreground), background)
            print(screen_line, flush=True)

