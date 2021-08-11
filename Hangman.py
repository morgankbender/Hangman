# imports
import json
import random
from Constants import WORD_LIST_PATH, WORD_LIST_KEY, HANGMAN_PICS, WIN_MSG, LOSE_MSG, GUESS_PROMPT, GUESS_INVALID


class Hangman:

    def __init__(self: "Hangman") -> None:
        """ Hangman instance constructor

        :return: None
        """
        self.HIDDEN_WORD = get_hidden_word()
        self.game_won = False
        self.game_lost = False
        self.missed_guesses = []
        self.all_guesses = []
        self.found_letters = [False] * len(self.HIDDEN_WORD)
        self.curr_guess = ""

    # CORE GAME FUNCTIONALITY ***********************************
    def check_guess(self: "Hangman") -> None:
        """ Iterate through word as substrings to find all indexes of the guessed letter

        :return: None
        """
        # Init vars
        index = 0

        # Each time an index is found, create a substring beginning one past the previous
        # index and search again. Stop when end of string is reached or break if no index is found
        while index != len(self.HIDDEN_WORD):
            substring = self.HIDDEN_WORD[index:]
            sub_index = substring.find(self.curr_guess)

            if sub_index != -1:
                index += sub_index
                self.found_letters[index] = True
                index += 1
            else:
                if index == 0:
                    self.missed_guesses.append(self.curr_guess)
                break

    def display_game_data(self: "Hangman") -> None:
        """ Display information about game to the CLI

        :return: None
        """
        # Put a large space to differentiate from old data. Then display hangman image.
        print(f"\n\n{HANGMAN_PICS[len(self.missed_guesses)]}")

        # Show word preview with found letters in their proper place and
        # underscores for the rest of the letters
        word_preview = ""
        for i in range(len(self.HIDDEN_WORD)):
            if self.found_letters[i]:
                word_preview += f" {self.HIDDEN_WORD[i]} "
            else:
                word_preview += f" _ "
        print(f"\n{word_preview}")

        # Show all characters the user has guessed that were wrong
        # (or indicate they have not made any wrong guesses)
        if len(self.missed_guesses) != 0:
            print(f"\nWrong guesses:")
            print(*self.missed_guesses, sep=",")

        if self.game_won:
            print(WIN_MSG)
        elif self.game_lost:
            print(LOSE_MSG)
            print(f"The word was: {self.HIDDEN_WORD}")

    def check_game_over(self: "Hangman") -> None:
        """ Check win and lose conditions

        :return: None
        """
        if self.found_letters.count(False) == 0:
            self.game_won = True
        elif len(self.missed_guesses) == len(HANGMAN_PICS) - 1:
            self.game_lost = True

    def validate_guess(self: "Hangman") -> bool:
        """ Check if guess is valid (one letter)

        :return: Validity of guess
        :rtype: Boolean
        """
        if self.curr_guess.isalpha() and len(self.curr_guess) == 1:
            if self.all_guesses.count(self.curr_guess) > 0:
                print(f"You have already guessed {self.curr_guess}")
                return False
            else:
                self.all_guesses.append(self.curr_guess)
                return True
        else:
            print(GUESS_INVALID)
            return False

    def play_hangman(self: "Hangman") -> None:
        """ Launch game. Responsible for main game logic.

        :return: None
        """
        # Start by displaying game data
        print(f"For development only!! Word is: {self.HIDDEN_WORD}")
        self.display_game_data()

        # We will keep giving the user another turn until they have won or lost the game
        while not self.game_won and not self.game_lost:

            # Continuously prompt the user until they provide a valid guess
            valid_guess = False
            while not valid_guess:
                self.curr_guess = input(GUESS_PROMPT).upper()
                valid_guess = self.validate_guess()

            # Update where the guessed letter appears in the hidden word
            self.check_guess()

            # Check win conditions
            self.check_game_over()

            # Display game data (this is at the end so that if the game is won
            # or lost, the data is displayed one last time)
            self.display_game_data()


def get_hidden_word() -> str:
    """ Get random word from JSON file

    Using a json file from the internet for possible words.
    This function opens the json file and chooses a random
    word. If the word contains non-letter characters or is
    less than three characters, a new word will be selected.

    :return: random word from word_list.json that has at least three letters (and only letters)
    :rtype: str
    """
    # get list of words from word_list.json
    with open(WORD_LIST_PATH) as json_words:
        word_list = json.load(json_words)[WORD_LIST_KEY]

    # Get a random word from the list, until we find a word that is
    # all letters and at least 3 characters
    word = ""
    while len(word) < 3 and not word.isalpha():
        word = random.choice(word_list)

    # Return the randomly selected word in uppercase
    return word.upper()
