from typing import Optional

from tesseract.board_model import BoardModel
from enum import Enum
from tesseract.board_controller import BoardController
from tesseract.board_command import BoardCommand
from tesseract.event_queue import EventQueue, ModelChangedEvent
from tesseract.virtual_textual_screen import VirtualTextualScreen
from tesseract.textual_color import TextualColor

class BoardView:
    """
    Generic ASCII-graphical representation of a 4D board
    """
    def __init__(self,
        board_controller: BoardController,
        virtual_screen: VirtualTextualScreen,
        cell_width: int = 2,
        cell_height:int = 1,
        cell_left_diag_span: int = 1,
        cell_right_diag_span: int = 2,
        event_queue: Optional[EventQueue] = None):
        
        self._screen = virtual_screen
        self._cell_height = cell_height
        self._cell_width = cell_width
        self._cell_left_diag_span = cell_left_diag_span
        self._cell_right_diag_span = cell_right_diag_span
        self._board_controller = board_controller
        self._event_queue = event_queue if event_queue is not None else (
            board_controller.get_event_queue() if board_controller is not None else None
        )
        if self._event_queue is not None:
            self._event_queue.subscribe(self._on_model_changed)

    def _on_model_changed(self, event: ModelChangedEvent)->None:
        if not isinstance(event, ModelChangedEvent):
            return
        if event.model is not None and event.model is not self._board_controller.get_board_model():
            return
        self.render()

    def _render_board(self)->None:
        pass
        
    def clear_view(self)->None:
        self._screen.clear()
        
    def render(self)->None:
        self._render_board()
        self._screen.render()

    def is_legal(self, board_cmd: BoardCommand)->bool:
        return self._board_controller.is_legal(board_cmd)
        
    def process_command(self, board_cmd: BoardCommand)->None:
        self._board_controller.process_command(board_cmd)
        
    def report_illegal_command(self, board_cmd: BoardCommand)->None:
        pass
        
    def get_screen(self)->VirtualTextualScreen:
        return self._screen

    def get_event_queue(self)->Optional[EventQueue]:
        return self._event_queue


