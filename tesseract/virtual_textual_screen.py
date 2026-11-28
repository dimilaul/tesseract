from typing import Optional

from tesseract.event_queue import EventQueue, ScreenUpdatedEvent
from tesseract.textual_color import TextualColor

class VirtualTextualScreen:
    """
    Textual representation of the screen
    """

    def __init__(self, height: int, width: int, event_queue: Optional[EventQueue] = None):
        self._height = height
        self._width = width
        self._screen_matrix: list[list[tuple[str, TextualColor, TextualColor]]] = []
        self._event_queue = event_queue if event_queue is not None else EventQueue()
        self.clear()

    def get_event_queue(self)->EventQueue:
        return self._event_queue
        
    def clear(self):
        self._screen_matrix = [[(' ', TextualColor.BLACK, TextualColor.BLACK) for i in range(0, self._width)] for j in range(0, self._height)]

    def render(self)->None:
        if self._event_queue is not None:
            self._event_queue.emit(ScreenUpdatedEvent(self))

    def set_cell(self, x: int, y: int, c: str, bg_color: TextualColor, fg_color: TextualColor)->None:
        if x not in range(0, self._width):
            raise Exception(f"cannot set x out of range: {x}")
        if y not in range(0, self._height):
            raise Exception(f"cannot set y out of range: {y}")
        self._screen_matrix[y][x] = (c, bg_color, fg_color)
        
    def get_cell(self, x: int, y: int)->tuple[str, TextualColor, TextualColor]:
        return self._screen_matrix[y][x]
        
    def get_height(self)->int:
        return self._height
        
    def get_width(self)->int:
        return self._width
        

