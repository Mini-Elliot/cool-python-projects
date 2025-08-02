from random import randint
import subprocess


def guess_the_number():
    try:
        while True:
            least_value, highest_value = 1, 10
            random_number = randint(least_value, highest_value)
            print(
                f"Guess the number in the range of {least_value} to {highest_value}")
            while True:
                try:
                    guess = int(input("Guess: "))
                except ValueError as e:
                    print("Please enter a valid number.")
                    continue
                if guess > random_number:
                    print("Sorry, too high!")
                elif guess < random_number:
                    print("Sorry, too low!")
                elif guess == random_number:
                    print("Hooray! you got it.")
                    break
            choice = input("Do you want to play again? (y/n) ")
            if choice == "y" or choice == "yes":
                subprocess.call("cls", shell=True)
                highest_value = highest_value * 10
                continue
            elif choice == "n" or choice == "no":
                subprocess.call("cls", shell=True)
                print("\rThank you for playing! 😊")
                break
    except KeyboardInterrupt as e:
        print("\rCtrl + C detected. Exiting game.")


if __name__ == "__main__":
    guess_the_number()
