import os
import json
import math
import random

LEADERBOARD_FILE = "leaderboard.json"

# ----------- Levels ------------

MAX_LEVEL = 50

LEVELS = [
    {
        "upper": 50 + i * 25,
        "attempts": 5 + (i // 10),
        "hints": 5,
        "domains": (
            ["classic"] if i < 10 else
            ["classic", "prime"] if i < 20 else
            ["classic", "prime", "fibonacci"] if i < 30 else
            ["prime", "fibonacci", "pi"] if i < 40 else
            ["prime", "fibonacci", "pi", "e"]
        )
    }
    for i in range(MAX_LEVEL)
]



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
    print("HARDCORE MODE — 50 LEVELS — ONE LIFE\n")

    name = input("Enter your name: ").strip() or "Anonymous"

    total_guesses = 0

    for level in range(1, MAX_LEVEL + 1):
        config = LEVELS[level - 1]
        upper = config["upper"]
        attempts = config["attempts"]
        hints_left = config["hints"]
        domain = random.choice(config["domains"])

        secret = pick_number(domain, upper)
        low, high = 1, upper

        print(f"\nLEVEL {level}/50")
        print(f"Domain: {domain.upper()}")
        print(f"Range: {low}–{high}")
        print(f"Attempts: {attempts}")
        print(f"Hints available: {hints_left}")

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
                break

            if guess < secret:
                print("Too low.")
                low = max(low, guess + 1)
            else:
                print("Too high.")
                high = min(high, guess - 1)

            if hints_left > 0:
                mid = (low + high) // 2
                print(f"HINT ({hints_left} left): midpoint ≈ {mid}")
                hints_left -= 1

        else:
            return game_over(name, level)

    print("\nYOU WON.")
    print("All 50 levels completed.")
    game_over(name, MAX_LEVEL)



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
