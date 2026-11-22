from tesseract.board_view import BoardView
from tesseract.board_command import BoardCommand

class Puzzle15BoardView(BoardView):
    """
    ASCII-graphical representation of a 4D puzzle15 board
    """

    def read_button_click(self)->BoardCommand:
        line=input(">")
        return BoardCommand.NOP
        
    def draw(self):
        board_model = self._board_controller.get_board_model()
        print(f"BOARD: {board_model}")
