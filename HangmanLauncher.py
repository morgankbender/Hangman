from Constants import WELCOME_MSG, START_PROMPT, REPLAY_PROMPT, QUIT_MSG, YN_INVALID

from Hangman import Hangman


def launch_prompt(prompt: str) -> None:
    """ Prompt user for y or n (yes or no) answer.

    "Y" will launch a hangman game, "N" will close the application.

    :param prompt: Dialog to prompt user
    :type prompt: str
    :return: None
    """

    # Keep prompting user until they provide valid input
    validated = False
    while not validated:

        # Get user input (and capitalize it for ease of use)
        start_ans = input(prompt).upper()

        # If input is Y or N, they have given a valid answer.
        # Y will launch hangman, N will close application.
        # Invalid answer will reiterate instructions.
        if start_ans == "Y":
            validated = True
            game = Hangman()
            game.play_hangman()
        elif start_ans == "N":
            validated = True
            print(QUIT_MSG)
            quit()
        else:
            print(YN_INVALID)


# LAUNCH GAME ***********************************************
if __name__ == '__main__':
    # Welcome user to game
    print(WELCOME_MSG)

    # Prompt user to start first game
    launch_prompt(START_PROMPT)

    # Prompt user to replay until they close application
    while True:
        launch_prompt(REPLAY_PROMPT)

