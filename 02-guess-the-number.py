import os
import json
import math
import random
from typing import List, Dict


class Leaderboard:
    def __init__(self, filename: str = "leaderboard.json", limit: int = 10):
        self.filename = filename
        self.limit = limit

    def load(self) -> List[Dict]:
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                return json.load(f)
        return []

    def save(self, data: List[Dict]) -> None:
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def update(self, name: str, level: int) -> None:
        data = self.load()
        data.append({"name": name, "level": level})
        data = sorted(data, key=lambda x: x["level"], reverse=True)[: self.limit]
        self.save(data)

    def display(self) -> None:
        print("\nLEADERBOARD")
        for i, entry in enumerate(self.load(), 1):
            print(f"{i}. {entry['name']} — Level {entry['level']}")


class NumberDomains:
    PI_DIGITS = [int(d) for d in str(math.pi)[2:]]
    E_DIGITS = [int(d) for d in str(math.e)[2:]]

    @staticmethod
    def primes_up_to(n: int) -> List[int]:
        primes = []
        for x in range(2, n + 1):
            if all(x % p != 0 for p in primes):
                primes.append(x)
        return primes

    @staticmethod
    def fibonacci_up_to(n: int) -> List[int]:
        seq = [1, 1]
        while seq[-1] < n:
            seq.append(seq[-1] + seq[-2])
        return seq[:-1]

    @classmethod
    def pick(cls, domain: str, upper: int) -> int:
        if domain == "prime":
            return random.choice(cls.primes_up_to(upper))
        if domain == "fibonacci":
            return random.choice(cls.fibonacci_up_to(upper))
        if domain == "pi":
            return cls.PI_DIGITS[random.randint(0, min(upper, len(cls.PI_DIGITS) - 1))]
        if domain == "e":
            return cls.E_DIGITS[random.randint(0, min(upper, len(cls.E_DIGITS) - 1))]
        return random.randint(1, upper)


class LevelConfig:
    MAX_LEVEL = 50

    @classmethod
    def generate_levels(cls) -> List[Dict]:
        levels = []
        for i in range(cls.MAX_LEVEL):
            levels.append({
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
            })
        return levels


class HardcoreGame:
    def __init__(self):
        self.levels = LevelConfig.generate_levels()
        self.leaderboard = Leaderboard()
        self.total_guesses = 0
        self.player_name = "Anonymous"

    @staticmethod
    def clear():
        os.system("cls" if os.name == "nt" else "clear")

    def start(self):
        self.clear()
        print("HARDCORE MODE — 50 LEVELS — ONE LIFE\n")
        self.player_name = input("Enter your name: ").strip() or "Anonymous"

        for level_number in range(1, LevelConfig.MAX_LEVEL + 1):
            if not self.play_level(level_number):
                return

        print("\nYOU WON.")
        print("All 50 levels completed.")
        self.game_over(LevelConfig.MAX_LEVEL)

    def play_level(self, level_number: int) -> bool:
        config = self.levels[level_number - 1]
        upper = config["upper"]
        attempts = config["attempts"]
        hints_left = config["hints"]
        domain = random.choice(config["domains"])

        secret = NumberDomains.pick(domain, upper)
        low, high = 1, upper

        print(f"\nLEVEL {level_number}/50")
        print(f"Domain: {domain.upper()}")
        print(f"Range: {low}–{high}")
        print(f"Attempts: {attempts}")
        print(f"Hints available: {hints_left}")

        for turn in range(1, attempts + 1):
            try:
                guess = int(input(f"Guess {turn}: "))
            except ValueError:
                print("Invalid input. That counts.")
                self.game_over(level_number)
                return False

            self.total_guesses += 1

            if guess == secret:
                print("Correct.")
                return True

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

        self.game_over(level_number)
        return False

    def game_over(self, level: int):
        print("\nGAME OVER")
        print(f"You reached level {level}")
        self.leaderboard.update(self.player_name, level)
        self.leaderboard.display()


if __name__ == "__main__":
    try:
        HardcoreGame().start()
    except KeyboardInterrupt:
        print("\nExited.")
