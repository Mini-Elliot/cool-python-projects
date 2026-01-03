import random
import os
from collections import Counter

MOVES = ["rock", "paper", "scissors"]
WIN_MAP = {
    "rock": "scissors",
    "paper": "rock",
    "scissors": "paper",
}


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def winner(move1, move2):
    if move1 == move2:
        return 0
    return 1 if WIN_MAP[move1] == move2 else -1


# ---------- AI ENGINES ----------

def easy_ai():
    return random.choice(MOVES)


def medium_ai(history):
    if not history:
        return random.choice(MOVES)

    most_common = Counter(history).most_common(1)[0][0]
    return counter_move(most_common)


def hard_ai(history, depth=3):
    if len(history) < depth:
        return medium_ai(history)

    recent = history[-depth:]
    predicted = Counter(recent).most_common(1)[0][0]
    return counter_move(predicted)


def counter_move(move):
    for m, beats in WIN_MAP.items():
        if beats == move:
            return m


# ---------- GAME MODES ----------

def single_player():
    history = []

    level = input("Choose difficulty (easy / medium / hard): ").lower().strip()
    ai = {
        "easy": easy_ai,
        "medium": lambda: medium_ai(history),
        "hard": lambda: hard_ai(history),
    }.get(level)

    if not ai:
        print("Invalid difficulty.")
        return

    while True:
        user = input("Your move (rock/paper/scissors): ").lower().strip()
        if user not in MOVES:
            print("Invalid move.")
            continue

        computer = ai()
        history.append(user)

        result = winner(user, computer)
        print(f"Computer chose: {computer}")

        if result == 1:
            print("You win!")
        elif result == -1:
            print("You lose!")
        else:
            print("Draw.")

        if input("Play again? (y/n): ").lower() != "y":
            break


def two_player():
    while True:
        clear()
        p1 = input("Player 1 move: ").lower().strip()
        clear()
        p2 = input("Player 2 move: ").lower().strip()

        if p1 not in MOVES or p2 not in MOVES:
            print("Invalid move.")
            input("Press Enter...")
            continue

        result = winner(p1, p2)

        if result == 1:
            print("Player 1 wins!")
        elif result == -1:
            print("Player 2 wins!")
        else:
            print("Draw.")

        if input("Play again? (y/n): ").lower() != "y":
            break


# ---------- MAIN ----------

def main():
    while True:
        clear()
        print("Rock Paper Scissors")
        print("1. Single Player (AI)")
        print("2. Two Players")
        print("3. Exit")

        choice = input("Choose option: ").strip()

        if choice == "1":
            single_player()
        elif choice == "2":
            two_player()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")
            input("Press Enter...")


if __name__ == "__main__":
    main()
