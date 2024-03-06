def get_user_input_in_range(lower_bound: int, upper_bound: int) -> int:
    """
    capture input from the user until a valid int in the given range is passed
    """
    user_input = input()
    while not user_input.isdigit() or int(user_input) not in range(lower_bound, upper_bound+1):
        print(f"Invalid input. Please enter a number between {lower_bound} and {upper_bound}:")
        user_input = input()
    return int(user_input)


def stream_output(msg: str):
    print(msg)
