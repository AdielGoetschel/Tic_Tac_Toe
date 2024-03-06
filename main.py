from tic_tac_toe import Game
from utils import get_user_input_in_range, stream_output


if __name__ == "__main__":
    stream_output("Welcome to Tic-tac-toe! Please choose your mark (1 for X or 0 for O): ")
    human_mark = get_user_input_in_range(0, 1)
    game = Game(human_mark)
    game.play()
