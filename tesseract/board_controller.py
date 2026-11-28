from typing import Optional

from tesseract.board_model import BoardModel
from tesseract.board_command import BoardCommand
from tesseract.event_queue import EventQueue, ModelChangedEvent

class BoardController:
    """
    Manage the 4D TUI with arrows + WASD + shuffle + order
    """

    def __init__(self, board_model: BoardModel, event_queue: Optional[EventQueue] = None):
        self._board_model = board_model
        self._event_queue = event_queue if event_queue is not None else EventQueue()
        
    def get_board_model(self)->BoardModel:
        return self._board_model

    def get_event_queue(self)->EventQueue:
        return self._event_queue

    def emit_model_changed(self)->None:
        if self._event_queue is not None:
            self._event_queue.emit(ModelChangedEvent(self._board_model))

    def is_legal(self, board_cmd: BoardCommand)->bool:
        if board_cmd == BoardCommand.NOP:
            return True
        return False

    def _apply_command(self, board_cmd: BoardCommand)->bool:
        return False
        
    def process_command(self, board_cmd: BoardCommand)->None:
        if board_cmd == BoardCommand.NOP:
            return
        if self._apply_command(board_cmd):
            self.emit_model_changed()
