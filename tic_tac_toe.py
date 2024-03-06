import numpy as np
import random
from typing import Tuple, Optional

from utils import get_user_input_in_range, stream_output

EMPTY_CELL = -1
CENTER_CELL = 4
MARKS_MAPPING = {0: 'O', 1: 'X', EMPTY_CELL: ' '}  # mapping from numbers to the marks of the players
TIE_MESSAGE = "No one won"

BOARD_NUMBERING = """0 | 1 | 2
3 | 4 | 5
6 | 7 | 8
"""


class Board:
    def __init__(self):
        """Initialize the game board, -1 indicates an empty cell"""
        self.board = np.full((3, 3), EMPTY_CELL, dtype=int)

    def print_board(self) -> None:
        """Print the current game board"""
        for row in self.board:
            mapped_row = [MARKS_MAPPING[cell] for cell in row]
            stream_output(' | '.join(mapped_row))

    @staticmethod
    def display_board_numbering() -> None:
        """Display the numbering of cells."""
        stream_output(BOARD_NUMBERING)

    @staticmethod
    def convert_cell_numbering_to_indexes(cell: int) -> Tuple[int, int]:
        """Convert cell numbering to row and column indexes"""
        row = cell // 3
        column = cell % 3
        return row, column

    def is_cell_occupied(self, cell_number: int) -> bool:
        """Check if a cell is already occupied"""
        row, column = self.convert_cell_numbering_to_indexes(cell_number)
        return self.board[row][column] != EMPTY_CELL

    def update_cell(self, cell_number: int, mark: int) -> None:
        """Update a cell with a mark"""
        row, column = self.convert_cell_numbering_to_indexes(cell_number)
        self.board[row][column] = mark


class Player:
    def __init__(self, mark: int) -> None:
        """Initialize a player with a mark"""
        self.mark = mark


class Game:
    def __init__(self, mark: int) -> None:
        """Initialize the game with a players and board."""
        self.board = Board()
        self.human_player = Player(mark)
        self.computer_player = Player((mark + 1) % 2)

    @staticmethod
    def check_if_winner(player: Player, board: np.ndarray) -> bool:
        """Check if the given player wins on the given board"""
        mark = player.mark
        # Check rows, columns, and diagonals
        if (np.any(np.all(board == mark, axis=1)) or  # Check rows
                np.any(np.all(board == mark, axis=0)) or  # Check columns
                np.all(np.diag(board) == mark) or  # Check main diagonal
                np.all(np.diag(np.fliplr(board)) == mark)):  # Check other diagonal
            return True
        return False

    def check_potential_win(self, player: Player) -> Optional[int]:
        """Check if the given player can win in his next move"""
        mark = player.mark
        for i in range(9):
            row, column = self.board.convert_cell_numbering_to_indexes(i)
            if self.board.board[row][column] == EMPTY_CELL:  # if the cell is empty
                optional_board = self.board.board.copy()
                optional_board[row][column] = mark  # try placing the mark in the empty cell
                if self.check_if_winner(player, optional_board):
                    return i
        return None

    def human_move(self) -> int:
        """Take a move input from the human player"""
        self.board.display_board_numbering()
        stream_output("Current Board:")
        self.board.print_board()

        while True:
            stream_output("Please enter your move (0-8): ")
            cell = get_user_input_in_range(0, 8)
            if self.board.is_cell_occupied(cell):
                stream_output("That cell is already occupied. Choose another one.")
            else:
                return cell

    def computer_move(self) -> int:
        """Generate a move for the computer player"""
        # Check if the computer can win in the next move
        computer_winning_move = self.check_potential_win(self.computer_player)
        if computer_winning_move is not None:
            cell = computer_winning_move
            return cell

        # Check if the human player can win in the next move and block him
        human_winning_move = self.check_potential_win(self.human_player)
        if human_winning_move is not None:
            cell = human_winning_move
            return cell

        # take the center if it is available
        if not self.board.is_cell_occupied(CENTER_CELL):
            return CENTER_CELL

        # choose a random available cell
        cells_attempted = set()
        while True:
            cell_number = random.randint(0, 8)
            if cell_number not in cells_attempted and not self.board.is_cell_occupied(cell_number):
                return cell_number
            else:
                cells_attempted.add(cell_number)

    def play(self) -> None:
        """Start the game, moves between the human player and the computer player until either player wins
        or the game ends in a draw after 9 moves"""
        number_of_moves_played = 0
        current_player = self.human_player
        while number_of_moves_played < 9:
            if current_player == self.human_player:
                cell = self.human_move()
            else:
                cell = self.computer_move()
            self.board.update_cell(cell, current_player.mark)
            number_of_moves_played += 1
            if self.check_if_winner(current_player, self.board.board):
                stream_output(f"{MARKS_MAPPING[current_player.mark]} wins!")
                self.board.print_board()
                return
            if current_player == self.human_player:
                current_player = self.computer_player
            else:
                current_player = self.human_player
        stream_output(TIE_MESSAGE)
