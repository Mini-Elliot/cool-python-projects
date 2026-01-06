import os
import json
import math
import random
from typing import List, Dict


SAVE_FILE = "savegame.json"
LEADERBOARD_FILE = "leaderboard.json"


# ---------------- LEADERBOARD ----------------
class Leaderboard:
    def __init__(self, filename: str = LEADERBOARD_FILE, limit: int = 10):
        self.filename = filename
        self.limit = limit

    def load(self) -> List[Dict]:
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                return json.load(f)
        return []

    def save(self, data: List[Dict]):
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def update(self, name: str, level: int):
        data = self.load()
        data.append({"name": name, "level": level})
        data = sorted(data, key=lambda x: x["level"], reverse=True)[: self.limit]
        self.save(data)

    def display(self):
        print("\nLEADERBOARD")
        for i, entry in enumerate(self.load(), 1):
            print(f"{i}. {entry['name']} — Level {entry['level']}")


# ---------------- NUMBER DOMAINS ----------------
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


# ---------------- LEVEL CONFIG ----------------
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


# ---------------- HARDCORE GAME ----------------
class HardcoreGame:
    def __init__(self):
        self.levels = LevelConfig.generate_levels()
        self.leaderboard = Leaderboard()
        self.total_guesses = 0
        self.player_name = "Anonymous"
        self.adaptive_factor = 1.0  # ML-inspired difficulty multiplier
        self.current_level = 1

    @staticmethod
    def clear():
        os.system("cls" if os.name == "nt" else "clear")

    # ---------------- SAVE/RESUME ----------------
    def save_game(self):
        data = {
            "name": self.player_name,
            "level": self.current_level,
            "total_guesses": self.total_guesses,
            "adaptive_factor": self.adaptive_factor
        }
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)
        print("Game saved.")

    def load_game(self) -> bool:
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
            self.player_name = data.get("name", "Anonymous")
            self.current_level = data.get("level", 1)
            self.total_guesses = data.get("total_guesses", 0)
            self.adaptive_factor = data.get("adaptive_factor", 1.0)
            print(f"Resuming game for {self.player_name} at level {self.current_level}.")
            return True
        return False

    # ---------------- GAME FLOW ----------------
    def start(self):
        self.clear()
        print("HARDCORE MODE — 50 LEVELS — ONE LIFE\n")
        choice = input("Resume previous game? (y/n): ").strip().lower()
        if choice == "y" and self.load_game():
            pass
        else:
            self.player_name = input("Enter your name: ").strip() or "Anonymous"
            self.current_level = 1
            self.total_guesses = 0
            self.adaptive_factor = 1.0

        while self.current_level <= LevelConfig.MAX_LEVEL:
            result = self.play_level(self.current_level)
            if result:
                self.current_level += 1
            else:
                return

        print("\nYOU WON.")
        print("All 50 levels completed.")
        self.game_over(LevelConfig.MAX_LEVEL)

    def play_level(self, level_number: int) -> bool:
        config = self.levels[level_number - 1]

        # ---------------- ADAPTIVE DIFFICULTY ----------------
        upper = int(config["upper"] * self.adaptive_factor)
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
                print("Invalid input. That counts as a wrong guess.")
                self.update_adaptive(success=False)
                self.save_game()
                self.game_over(level_number)
                return False

            self.total_guesses += 1

            if guess == secret:
                print("Correct!")
                self.update_adaptive(success=True, attempts_used=turn, max_attempts=attempts)
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

        self.update_adaptive(success=False)
        self.save_game()
        self.game_over(level_number)
        return False

    # ---------------- ADAPTIVE DIFFICULTY ----------------
    def update_adaptive(self, success: bool, attempts_used: int = None, max_attempts: int = None):
        """Adjust difficulty based on performance"""
        if success and attempts_used is not None and max_attempts is not None:
            ratio = attempts_used / max_attempts
            if ratio < 0.5:  # solved quickly
                self.adaptive_factor *= 1.1
            elif ratio > 0.8:  # barely solved
                self.adaptive_factor *= 0.95
        elif not success:
            self.adaptive_factor *= 0.9

        # Keep bounds reasonable
        self.adaptive_factor = min(max(self.adaptive_factor, 0.5), 3.0)

    # ---------------- GAME OVER ----------------
    def game_over(self, level: int):
        print("\nGAME OVER")
        print(f"You reached level {level}")
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
        self.leaderboard.update(self.player_name, level)
        self.leaderboard.display()
        exit()


if __name__ == "__main__":
    try:
        HardcoreGame().start()
    except KeyboardInterrupt:
        print("\nExited.")
