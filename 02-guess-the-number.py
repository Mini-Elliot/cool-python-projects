import os
import json
import math
import random

LEADERBOARD_FILE = "leaderboard.json"


# ---------- Utilities ----------

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    return []


def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ---------- Number Generators ----------

def primes_up_to(n):
    primes = []
    for x in range(2, n + 1):
        if all(x % p != 0 for p in primes):
            primes.append(x)
    return primes


def fibonacci_up_to(n):
    seq = [1, 1]
    while seq[-1] < n:
        seq.append(seq[-1] + seq[-2])
    return seq[:-1]


PI_DIGITS = [int(d) for d in str(math.pi)[2:]]
E_DIGITS = [int(d) for d in str(math.e)[2:]]


def pick_number(domain, upper):
    if domain == "prime":
        return random.choice(primes_up_to(upper))
    if domain == "fibonacci":
        return random.choice(fibonacci_up_to(upper))
    if domain == "pi":
        return PI_DIGITS[random.randint(0, min(upper, len(PI_DIGITS) - 1))]
    if domain == "e":
        return E_DIGITS[random.randint(0, min(upper, len(E_DIGITS) - 1))]
    return random.randint(1, upper)


# ---------- Game ----------

def hardcore_game():
    clear()
    print("HARDCORE MODE — ONE LIFE\n")

    name = input("Enter your name: ").strip() or "Anonymous"

    level = 1
    upper = 50
    attempts = 7
    total_guesses = 0

    domains = ["prime", "fibonacci", "pi", "e", "classic"]

    while True:
        domain = random.choice(domains)
        secret = pick_number(domain, upper)
        low, high = 1, upper

        print(f"\nLEVEL {level}")
        print(f"Domain: {domain.upper()}")
        print(f"Range: {low}–{high}")
        print(f"Attempts: {attempts}")
        print("Hint: Optimal play uses binary search.")

        used = []

        for turn in range(1, attempts + 1):
            try:
                guess = int(input(f"Guess {turn}: "))
            except ValueError:
                print("Invalid input. That counts.")
                return game_over(name, level)

            total_guesses += 1
            used.append(guess)

            if guess == secret:
                print("Correct.")

                # efficiency check
                ideal = math.ceil(math.log2(high - low + 1))
                if len(used) > ideal:
                    print("You solved it, but inefficiently.")
                else:
                    print("Efficient solution.")

                # adaptive difficulty
                efficiency = ideal / len(used)
                upper += int(upper * (0.3 + efficiency))
                attempts = max(3, attempts - 1)

                level += 1
                break

            if guess < secret:
                print("Too low.")
                low = max(low, guess + 1)
            else:
                print("Too high.")
                high = min(high, guess - 1)

            if len(used) >= 3:
                mid = (low + high) // 2
                print(f"Binary hint: midpoint ≈ {mid}")

        else:
            return game_over(name, level)


def game_over(name, level):
    print("\nGAME OVER")
    print(f"You reached level {level}")

    leaderboard = load_leaderboard()
    leaderboard.append({"name": name, "level": level})
    leaderboard = sorted(leaderboard, key=lambda x: x["level"], reverse=True)[:10]
    save_leaderboard(leaderboard)

    print("\nLEADERBOARD")
    for i, entry in enumerate(leaderboard, 1):
        print(f"{i}. {entry['name']} — Level {entry['level']}")


if __name__ == "__main__":
    try:
        hardcore_game()
    except KeyboardInterrupt:
        print("\nExited.")
