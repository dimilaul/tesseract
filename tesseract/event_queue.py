from collections import deque
from typing import Any, Callable, Optional


class Event:
    """Base class for events dispatched through an EventQueue."""


class ModelChangedEvent(Event):
    """Event emitted when a BoardController changes its BoardModel."""

    def __init__(self, model: Optional[Any] = None):
        self.model = model


class ScreenUpdatedEvent(Event):
    """Event emitted when a VirtualTextualScreen is rendered."""

    def __init__(self, screen: Optional[Any] = None):
        self.screen = screen


class EventQueue:
    """FIFO event queue supporting listener subscriptions and sequential dispatch."""

    def __init__(self, auto_dispatch: bool = True):
        self._queue: deque = deque()
        self._listeners: list[Callable[[Any], None]] = []
        self._auto_dispatch = auto_dispatch
        self._dispatching = False

    def subscribe(self, listener: Callable[[Any], None]) -> None:
        if listener not in self._listeners:
            self._listeners.append(listener)

    def unsubscribe(self, listener: Callable[[Any], None]) -> None:
        if listener in self._listeners:
            self._listeners.remove(listener)

    def emit(self, event: Any) -> None:
        self._queue.append(event)
        if self._auto_dispatch and not self._dispatching:
            self.process_events()

    def process_events(self) -> None:
        if self._dispatching:
            return
        self._dispatching = True
        try:
            while self._queue:
                event = self._queue.popleft()
                for listener in list(self._listeners):
                    listener(event)
        finally:
            self._dispatching = False

    def is_empty(self) -> bool:
        return len(self._queue) == 0

    def __len__(self) -> int:
        return len(self._queue)
