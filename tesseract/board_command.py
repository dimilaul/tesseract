from enum import Enum

class BoardCommand(Enum):
    NOP = 0
    MOVE_UP = 1
    MOVE_DOWN = 2
    MOVE_RIGHT = 3
    MOVE_LEFT = 4
    MOVE_UPSQ = 5
    MOVE_DOWNSQ = 6
    MOVE_LEFTSQ = 7
    MOVE_RIGHTSQ = 8
    MOVE_SHUFFLE = 9
    MOVE_ORDER = 10
    MOVE_TIMER = 11
