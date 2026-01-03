import random
from collections import Counter
from typing import List


def roll_dice(amount: int, sides: int) -> List[int]:
    if amount <= 0 or sides <= 1:
        raise ValueError("Dice amount must be > 0 and sides must be > 1")

    return [random.randint(1, sides) for _ in range(amount)]


def print_stats(history: List[int]) -> None:
    if not history:
        print("No rolls yet.")
        return

    total = sum(history)
    average = total / len(history)
    frequency = Counter(history)

    print("\n--- Statistics ---")
    print(f"Total rolls: {len(history)}")
    print(f"Sum: {total}")
    print(f"Average: {average:.2f}")
    print("Frequency:")
    for value in sorted(frequency):
        print(f"  {value}: {frequency[value]}")
    print("------------------\n")


def main():
    history: List[int] = []

    print("Dice Simulator")
    print("Commands:")
    print("  roll <dice> <sides>  → roll dice (e.g., roll 2 6)")
    print("  stats               → show statistics")
    print("  exit                → quit\n")

    while True:
        user_input = input("> ").strip().lower()

        if user_input == "exit":
            print("Thank you for playing.")
            break

        if user_input == "stats":
            print_stats(history)
            continue

        if user_input.startswith("roll"):
            try:
                _, dice, sides = user_input.split()
                rolls = roll_dice(int(dice), int(sides))
                history.extend(rolls)
                print("Rolled:", ", ".join(map(str, rolls)))
            except ValueError:
                print("Usage: roll <dice> <sides> (e.g., roll 3 6)")
            except Exception:
                print("Invalid command.")
            continue

        print("Unknown command.")


if __name__ == "__main__":
    main()
