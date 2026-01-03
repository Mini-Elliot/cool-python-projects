from random import choice
import os
import string

WORDS = ["apple", "secret", "banana", "tomato", "chicken"]

HANGMAN_STAGES = [
    """
     -----
     |   |
         |
         |
         |
         |
    --------
    """,
    """
     -----
     |   |
     O   |
         |
         |
         |
    --------
    """,
    """
     -----
     |   |
     O   |
     |   |
         |
         |
    --------
    """,
    """
     -----
     |   |
     O   |
    /|   |
         |
         |
    --------
    """,
    """
     -----
     |   |
     O   |
    /|\\  |
         |
         |
    --------
    """,
    """
     -----
     |   |
     O   |
    /|\\  |
    /    |
         |
    --------
    """,
    """
     -----
     |   |
     O   |
    /|\\  |
    / \\  |
         |
    --------
    """
]


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def run_game():
    while True:
        clear_screen()
        word = choice(WORDS).lower()
        guessed_letters = set()
        wrong_guesses = 0
        max_wrong = len(HANGMAN_STAGES) - 1

        name = input("What is your name? >> ").strip()
        clear_screen()
        print(f"Welcome to Hangman, {name}\n")

        while True:
            clear_screen()
            print(HANGMAN_STAGES[wrong_guesses])

            # Display word
            display_word = " ".join(
                char if char in guessed_letters else "_"
                for char in word
            )
            print("Word:", display_word)
            print("\nGuessed letters:", " ".join(sorted(guessed_letters)))

            # Win condition
            if all(char in guessed_letters for char in word):
                print("\nYou won! 🎉")
                break

            # Lose condition
            if wrong_guesses == max_wrong:
                print(f"\nYou lost! The word was: {word}")
                break

            guess = input("\nEnter a letter: ").lower().strip()

            if len(guess) != 1 or guess not in string.ascii_lowercase:
                print("Enter a single alphabetic character.")
                input("Press Enter to continue...")
                continue

            if guess in guessed_letters:
                print("You already guessed that letter.")
                input("Press Enter to continue...")
                continue

            guessed_letters.add(guess)

            if guess not in word:
                wrong_guesses += 1

        choice_again = input("\nPlay again? (y/n): ").lower().strip()
        if choice_again != "y":
            clear_screen()
            print("Thank you for playing.")
            break


if __name__ == "__main__":
    run_game()
