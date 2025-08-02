from random import choice
import subprocess

def run_game():
    while True:
        word: str = choice(["apple", "secret", "banana"])

        user_name: str = input("What is your name? >> ")
        print(f"Welcome to hangman, {user_name}")

        #setup
        guessed: str = ''
        tries: int = 3

        #game
        while tries > 0:
            blanks: int = 0

            print("Word: ", end='')
            for char in word:
                if char in guessed:
                    print(char, end="")
                else:
                    print("_", end="")
                    blanks+=1
        
            print("") # This adds a blank line

            if blanks == 0:
                print('You got it')
                break

            guess: str = input("Enter a letter: ")

            if guess in guessed:
                print(f"You already used: {guess}. Please try with another letter.")
                continue

            guessed += guess

            if guess not in guessed:
                tries-=1
                print(f"Sorry, that was wrong... (tries remaining: {tries})")

                if tries == 0:
                    print("No more tries remaining. You lose!")
                    break
                
        user_choice: str = input("Do you want to play again? (y/n) ").strip().lower()
        if user_choice == "y":
            subprocess.call("cls", shell=True)
            continue
        elif user_choice == "n":
            subprocess.call("cls", shell=True)
            print("Thank you for playing! 😊")
            break
        else:
            print('Enter a valid choice.')
            break

if __name__ == "__main__":
    run_game()
