import random
import subprocess

def rock_paper_scissors():
    moves = ["rock", "paper", "scissors"]
    try:
        while True:
            computer_move = random.choice(moves)
            while True:
                user_move = input(
                    "Please enter your move (rock, paper, scissors) >> ").strip().lower()
                if user_move in moves:
                    if (user_move == "rock" and computer_move == "paper") or (user_move == "paper" and computer_move == "scissors") or (user_move == "scissors" and computer_move == "rock"):
                        print(f"Sorry, you lost. Computer move: {computer_move}")
                        break
                    elif user_move == computer_move:
                        print(f"It is a draw. Computer move: {computer_move}")
                        break
                    else:
                        print(f"Hurray! You win. Computer move: {computer_move}")
                        break
                else:
                    print("Please enter a moves form the list.")
            choice = input("Do you want to play again? (y/n) ")
            if choice == "y" or choice == "yes":
                subprocess.call("cls", shell=True)
                continue
            elif choice == "n" or choice == "no":
                subprocess.call("cls", shell=True)
                print("\rThank you for playing! 😊")
                break
    except KeyboardInterrupt:
        subprocess.call("cls", shell=True)
        print("\rCtrl + C detected. Exiting game.")

if __name__ == "__main__":
    rock_paper_scissors()