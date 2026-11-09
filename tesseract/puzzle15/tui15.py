import argparse
import sys
from tabulate import tabulate
import tty
import termios
import random

from tesseract.puzzle15.puzzle15_board_model import Puzzle15BoardModel
from tesseract.puzzle15.puzzle15_board_view import Puzzle15BoardView
from tesseract.puzzle15.puzzle15_board_controller import Puzzle15BordController

tabulate.PRESERVE_WHITESPACE = True

DEFAULT_SHUFFLE_MOVES = 5
number_of_shuffle_moves = DEFAULT_SHUFFLE_MOVES
DEFAULT_DIMENSIONS = [4, 4, 4, 4]

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

STATUS_INITIAL = 0
STATUS_MOVED = 1
STATUS_ILLEGAL_MOVE = 2
STATUS_SOLVED = 3
STATUS_SHUFFLED = 4

BOARD_TUI_HEIGHT = 12


# ansi term colors
BG_BLACK = "\033[40m"
BG_GREEN = "\033[42m"
BG_CYAN = "\033[46m"
FG_RED = "\033[31m"
FG_GREEN = "\033[33m"
FG_CYAN = "\033[36m"
FG_WHITE = "\033[37m"
FG_BLACK = "\033[30m"
TERMCOLOR_RESET = "\033[0m"

def number_to_string(array, idx):
    num = array[idx]

    if num == 16:
        return f"{FG_BLACK}--{FG_WHITE}" 

    idx16 = -1
    for i in range(0, 16):
        if array[i] == 16:
            idx16 = i
            break


    coord16 = array_position_to_coordinates(idx16)
    all_neighbours = all_neighbour_coordinates(coord16)
    for neighbour_coord in all_neighbours:
        neighbour_idx = coordinates_to_position(*neighbour_coord)
        if idx == neighbour_idx:
            return f"{FG_GREEN}{num:2}{FG_WHITE}"

    return f"{FG_WHITE}{num:2}"


def draw_empty_board():
    for i in range(0, BOARD_TUI_HEIGHT):
        print()

def draw_board(array, status):
    if_solved = ""
    if status == STATUS_SOLVED:
        if_solved = BG_CYAN
    print(f"\033[{BOARD_TUI_HEIGHT + 1}A{if_solved}\r")
    sub1 = [[number_to_string(array,  0), number_to_string(array,  1)], [number_to_string(array,  2), number_to_string(array,  3)]]
    sub2 = [[number_to_string(array,  4), number_to_string(array,  5)], [number_to_string(array,  6), number_to_string(array,  7)]]
    sub3 = [[number_to_string(array,  8), number_to_string(array,  9)], [number_to_string(array, 10), number_to_string(array, 11)]]
    sub4 = [[number_to_string(array, 12), number_to_string(array, 13)], [number_to_string(array, 14), number_to_string(array, 15)]]

    fmt = "rounded_grid"
    lines1 = tabulate(sub1, tablefmt=fmt).splitlines()
    lines2 = tabulate(sub2, tablefmt=fmt).splitlines()
    lines3 = tabulate(sub3, tablefmt=fmt).splitlines()
    lines4 = tabulate(sub4, tablefmt=fmt).splitlines()

    # 3. Combine tables side-by-side for the top row (sub1 and sub2)
    top_row = [l1 + "    " + l2 for l1, l2 in zip(lines1, lines2)]

    # 4. Combine tables side-by-side for the bottom row (sub3 and sub4)
    bottom_row = [l3 + "    " + l4 for l3, l4 in zip(lines3, lines4)]

    # 5. Print the complete grid
    for line in top_row:
        print(line)
    # Optional: add a blank line or spacing between rows if desired
    print("                          ")
    for line in bottom_row:
        print(line)
    print(TERMCOLOR_RESET)


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
    # Use cbreak mode to keep Ctrl+C signal handling active
        tty.setcbreak(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def move_to_string(move):
    if move == MOVE_UP:
        return "up"
    elif move == MOVE_DOWN:
        return "down"
    elif move == MOVE_RIGHT:
        return "right"
    elif move == MOVE_LEFT:
        return "left"
    elif move == MOVE_UPSQ:
        return "up square"
    elif move == MOVE_DOWNSQ:
        return "down square"
    elif move == MOVE_LEFTSQ:
        return "left square"
    elif move == MOVE_RIGHTSQ:
        return "right square"
    elif move == MOVE_SHUFFLE:
        return "shuffle"
    elif move == MOVE_ORDER:
        return "order"
    else:
        return " !!! UNRECOGNIZED MOVE !!! "


def parse_input(inp):
    move = 0
    if inp == 65:
        move = MOVE_UP
    elif inp == 66:
        move = MOVE_DOWN
    elif inp == 67:
        move = MOVE_RIGHT
    elif inp == 68:
        move = MOVE_LEFT
    elif inp == ord('w'):
        move = MOVE_UPSQ
    elif inp == ord('s'):
        move = MOVE_DOWNSQ
    elif inp == ord('d'):
        move = MOVE_RIGHTSQ
    elif inp == ord('a'):
        move = MOVE_LEFTSQ
    elif inp == 10 or inp == ord(' '):
        move = MOVE_SHUFFLE
    elif inp == ord('o'):
        move = MOVE_ORDER
#    if move:
#        print(move_to_string(move))
    return move

def array_position_to_coordinates(idx):
    return (idx // 8, idx % 8 // 4, idx % 4 // 2, idx % 2)

def coordinates_to_position(x, y, z, t):
    return x * 8 + y * 4 + z * 2 + t

def neighbour_coordinates_for_move(array, coord16, cmd):
    if coord16[0] and cmd == MOVE_DOWNSQ   or not coord16[0] and cmd == MOVE_UPSQ:
        return (1 - coord16[0], coord16[1], coord16[2], coord16[3])
    if coord16[1] and cmd == MOVE_RIGHTSQ  or not coord16[1] and cmd == MOVE_LEFTSQ:
        return (coord16[0], 1 - coord16[1], coord16[2], coord16[3])
    if coord16[2] and cmd == MOVE_DOWN     or not coord16[2] and cmd == MOVE_UP:
        return (coord16[0], coord16[1], 1 - coord16[2], coord16[3])
    if coord16[3] and cmd == MOVE_RIGHT    or not coord16[3] and cmd == MOVE_LEFT:
        return (coord16[0], coord16[1], coord16[2], 1 - coord16[3])

    return None

def all_neighbour_coordinates(coord16):
    return [(1 - coord16[0], coord16[1], coord16[2], coord16[3]),
            (coord16[0], 1 - coord16[1], coord16[2], coord16[3]),
            (coord16[0], coord16[1], 1 - coord16[2], coord16[3]), 
            (coord16[0], coord16[1], coord16[2], 1 - coord16[3])]

def transform(array, cmd, loud):
    idx16 = -1
    for i in range(0, 16):
        if array[i] == 16:
            idx16 = i
            break
    coord16 = array_position_to_coordinates(idx16)
    neighbour_coord = neighbour_coordinates_for_move(array, coord16, cmd)
    if neighbour_coord:
        neighbour_idx = coordinates_to_position(*neighbour_coord)
        array[idx16] = array[neighbour_idx]
        array[neighbour_idx] = 16
        status = STATUS_MOVED
        if in_order(array):
            status = STATUS_SOLVED
    else:
        status = STATUS_ILLEGAL_MOVE
    return array, status

def in_order(array):
    for i in range(0, 16):
        if array[i] != i + 1:
            return False
    return True

def revert_move(move):
    binary_move = move - 1
    reverse_binary_move = 2 * (binary_move // 2) + 1 - binary_move % 2
    return reverse_binary_move + 1

def shuffle(array):
    for move in range(number_of_shuffle_moves):
        cmd = random.sample(range(1, 9), 1)[0]
#        print(f"shuffling with cmd {move_to_string(cmd)}, in order to revert apply {move_to_string(revert_move(cmd))}")
        array, _ = transform(array, cmd, False)
    return array

def init_array():
    return [i for i in range(1, 17)]

def dimension_type(value):
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value!r} is not an integer")
    if not (1 <= ivalue <= 16):
        raise argparse.ArgumentTypeError(f"dimension must be an integer from 1 to 16, got {ivalue}")
    return ivalue

class DimensionsAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if len(values) > 4:
            parser.error(f"argument {option_string or '-d/--dimensions'}: allowed up to 4 values, got {len(values)}")
        if len(values) < 4:
            values = values + [1] * (4 - len(values))
        setattr(namespace, self.dest, values)

def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--shuffle-moves",
        type=int,
        default=DEFAULT_SHUFFLE_MOVES,
        help="number of shuffle moves",
    )
    parser.add_argument(
        "-d",
        "--dimensions",
        nargs="*",
        type=dimension_type,
        default=DEFAULT_DIMENSIONS,
        action=DimensionsAction,
        help="board dimensions (up to 4 integers from 1 to 16, default: 4 4 4 4)",
    )
    return parser

if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    number_of_shuffle_moves = args.shuffle_moves
    array = init_array()
    print("Press <Enter> or <Space> in order to shuffle, press O to order it back")
    print("Press arrows to move inside the square and WASD to move between the squares")

    draw_empty_board()
    draw_board(array, STATUS_INITIAL)
    while True:
        c = getch()
        if ord(c) == 91 or ord(c) == 27:
            continue
#        print(f"\n{ord(c)}")
        cmd = parse_input(ord(c))
        if cmd:
            if cmd == MOVE_SHUFFLE:
                array = shuffle(array)
                draw_board(array, STATUS_SHUFFLED)
            elif cmd == MOVE_ORDER:
                array = init_array()
                draw_board(array, STATUS_INITIAL)
            else:
                array, status = transform(array, cmd, True)
                draw_board(array, status)
