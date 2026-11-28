from typing import Optional

from tesseract.event_queue import EventQueue, ScreenUpdatedEvent
from tesseract.virtual_textual_screen import VirtualTextualScreen


class ScreenRenderer:
    """Base renderer listening to ScreenUpdatedEvent on a screen event queue."""

    def __init__(self, screen: VirtualTextualScreen):
        self._screen = screen
        self._event_queue = screen.get_event_queue()
        if self._event_queue is not None:
            self._event_queue.subscribe(self._on_screen_updated)

    def _on_screen_updated(self, event: ScreenUpdatedEvent) -> None:
        if not isinstance(event, ScreenUpdatedEvent):
            return
        if event.screen is not None and event.screen is not self._screen:
            return
        self.render()

    def get_screen(self) -> VirtualTextualScreen:
        return self._screen

    def get_event_queue(self) -> Optional[EventQueue]:
        return self._event_queue

    def clear(self):
        raise NotImplementedError("Subclasses must implement the clear method.")

    def render(self):
        raise NotImplementedError("Subclasses must implement the render method.")