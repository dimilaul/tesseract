import argparse
import sys
from tabulate import tabulate
import random

from tesseract.puzzle15.puzzle15_board_model import Puzzle15BoardModel
from tesseract.puzzle15.puzzle15_board_model import Puzzle15BoardStatus
from tesseract.puzzle15.puzzle15_simplified_board_view import Puzzle15SimplifiedBoardView
from tesseract.puzzle15.puzzle15_board_controller import Puzzle15BoardController
from tesseract.board_command import BoardCommand
from tesseract.tui.keyboard_control import KeyboardControl
from tesseract.tui.terminal import TerminalControl

tabulate.PRESERVE_WHITESPACE = True

DEFAULT_SHUFFLE_MOVES = 5
number_of_shuffle_moves = DEFAULT_SHUFFLE_MOVES
DEFAULT_DIMENSIONS = [4, 4, 4, 4]


def number_to_string(array, idx):
    num = array[idx]

    if num == 16:
        return f"{TerminalControl.FG_BLACK}--{TerminalControl.FG_WHITE}"

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
            return f"{TerminalControl.FG_GREEN}{num:2}{TerminalControl.FG_WHITE}"

    return f"{TerminalControl.FG_WHITE}{num:2}"


def draw_empty_board():
    for i in range(0, TerminalControl.BOARD_TUI_HEIGHT):
        print()

def draw_board(array, status):
    if_solved = ""
    if status == Puzzle15BoardStatus.STATUS_SOLVED:
        if_solved = TerminalControl.BG_CYAN
    print(f"\033[{TerminalControl.BOARD_TUI_HEIGHT + 1}A{if_solved}\r")
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
    print(TerminalControl.TERMCOLOR_RESET)

def array_position_to_coordinates(idx):
    return (idx // 8, idx % 8 // 4, idx % 4 // 2, idx % 2)

def coordinates_to_position(x, y, z, t):
    return x * 8 + y * 4 + z * 2 + t

def neighbour_coordinates_for_move(array, coord16, cmd):
    if coord16[0] and cmd == BoardCommand.MOVE_DOWNSQ.value   or not coord16[0] and cmd == BoardCommand.MOVE_UPSQ.value:
        return (1 - coord16[0], coord16[1], coord16[2], coord16[3])
    if coord16[1] and cmd == BoardCommand.MOVE_RIGHTSQ.value  or not coord16[1] and cmd == BoardCommand.MOVE_LEFTSQ.value:
        return (coord16[0], 1 - coord16[1], coord16[2], coord16[3])
    if coord16[2] and cmd == BoardCommand.MOVE_DOWN.value     or not coord16[2] and cmd == BoardCommand.MOVE_UP.value:
        return (coord16[0], coord16[1], 1 - coord16[2], coord16[3])
    if coord16[3] and cmd == BoardCommand.MOVE_RIGHT.value    or not coord16[3] and cmd == BoardCommand.MOVE_LEFT.value:
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
        status = Puzzle15BoardStatus.STATUS_MOVED
        if in_order(array):
            status = Puzzle15BoardStatus.STATUS_SOLVED
    else:
        status = Puzzle15BoardStatus.STATUS_ILLEGAL_MOVE
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

    # MVC initialization
    
    model = Puzzle15BoardModel(args.dimensions[0], args.dimensions[1], args.dimensions[2], args.dimensions[3])
    controller = Puzzle15BoardController(model)
    view = Puzzle15SimplifiedBoardView(controller)
    
    # TUI keyboard control
    keyboard_control = KeyboardControl()
    
    # here goes the main gameplay loop

    number_of_shuffle_moves = args.shuffle_moves
    array = init_array()
    print("Press <Enter> or <Space> in order to shuffle, press O to order it back")
    print("Press arrows to move inside the square and WASD to move between the squares")

    draw_empty_board()
    draw_board(array, Puzzle15BoardStatus.STATUS_INITIAL)
    while True:
        cmd = keyboard_control.get_next_command_from_input()
        if cmd != BoardCommand.NOP:
            if cmd == BoardCommand.MOVE_SHUFFLE:
                array = shuffle(array)
                draw_board(array, Puzzle15BoardStatus.STATUS_SHUFFLED)
            elif cmd == BoardCommand.MOVE_ORDER:
                array = init_array()
                draw_board(array, Puzzle15BoardStatus.STATUS_INITIAL)
            else:
                array, status = transform(array, cmd.value, True)
                draw_board(array, status)
