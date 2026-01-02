import json, os, sys, random, math, hashlib

SAVE_FILE = "save.json"
LEADERBOARD_FILE = "leaderboard.json"


def clear():
    os.system("cls" if os.name == "nt" else "clear")


# ===================== LEADERBOARD =====================

class Leaderboard:
    def __init__(self, file=LEADERBOARD_FILE):
        self.file = file
        self.entries = self.load()

    def load(self):
        if os.path.exists(self.file):
            with open(self.file) as f:
                return json.load(f)
        return []

    def add(self, name, level):
        self.entries.append({"name": name, "level": level})
        self.entries = sorted(self.entries, key=lambda x: x["level"], reverse=True)[:10]
        with open(self.file, "w") as f:
            json.dump(self.entries, f, indent=4)

    def show(self):
        print("\n=== LEADERBOARD ===")
        for i, e in enumerate(self.entries, 1):
            print(f"{i}. {e['name']} — Level {e['level']}")


# ===================== SKILLS =====================

class SkillTree:
    def __init__(self):
        self.hacking = 0
        self.combat = 0
        self.stealth = 0

    def upgrade(self, skill):
        if hasattr(self, skill):
            setattr(self, skill, getattr(self, skill) + 1)


# ===================== PLAYER =====================

class Player:
    def __init__(self, name):
        self.name = name
        self.max_hp = 100
        self.hp = self.max_hp
        self.lives = 3
        self.level = 1
        self.score = 0
        self.credits = 0
        self.detection = 0
        self.skills = SkillTree()

    def alive(self):
        return self.hp > 0

    def lose_life(self):
        self.lives -= 1
        self.reset_after_death()

    def reset_after_death(self):
        self.hp = self.max_hp
        self.detection = 0


# ===================== ENEMY =====================

class Enemy:
    def __init__(self, level):
        self.is_boss = level % 5 == 0
        base = 30 + level * 8
        self.hp = base * (2 if self.is_boss else 1)
        self.damage = 8 + level * 2


# ===================== HACKING =====================

class HackPuzzle:
    @staticmethod
    def domain():
        return random.choice(["prime", "fibonacci", "pi", "e"])

    @staticmethod
    def generate(domain):
        if domain == "prime":
            return random.choice(
                [x for x in range(2, 200) if all(x % p for p in range(2, int(x**0.5)+1))]
            )
        if domain == "fibonacci":
            seq = [1, 1]
            while seq[-1] < 200:
                seq.append(seq[-1] + seq[-2])
            return random.choice(seq)
        if domain == "pi":
            return int(str(math.pi)[2:6])
        if domain == "e":
            return int(str(math.e)[2:6])

    @staticmethod
    def play(player):
        domain = HackPuzzle.domain()
        secret = HackPuzzle.generate(domain)
        low, high = 1, 200
        attempts = max(3, 6 - player.skills.hacking)

        print(f"\nHACK MODE — {domain.upper()}")
        print("Binary search recommended.")

        for _ in range(attempts):
            try:
                guess = int(input(f"[{low}-{high}] Guess: "))
            except:
                player.detection += 10
                continue

            if guess == secret:
                print("Hack successful.")
                return True

            player.detection += 5
            if guess < secret:
                low = guess + 1
                print("Too low.")
            else:
                high = guess - 1
                print("Too high.")

            print(f"Hint: midpoint ≈ {(low + high) // 2}")

        print("Hack failed.")
        return False


# ===================== COMBAT =====================

class CombatSystem:
    @staticmethod
    def engage(player):
        enemy = Enemy(player.level)

        print("\n⚠ ENCOUNTER ⚠")
        if enemy.is_boss:
            print("BOSS DETECTED.")

        while enemy.hp > 0 and player.alive():
            print(f"\nHP: {player.hp} | Lives: {player.lives} | Detection: {player.detection}")
            action = input("[attack / hack / flee]: ").lower()

            if action == "attack":
                dmg = random.randint(10, 18) + player.skills.combat * 2
                enemy.hp -= dmg
                print(f"You dealt {dmg} damage.")

            elif action == "hack":
                if HackPuzzle.play(player):
                    enemy.hp = 0
                else:
                    player.detection += 10

            elif action == "flee":
                player.hp -= 20
                print("You escaped, but lost HP.")
                return

            enemy_hit = enemy.damage + random.randint(0, 6)
            player.hp -= enemy_hit
            print(f"Enemy hit for {enemy_hit}.")

            if player.detection >= 100:
                print("TRACE COMPLETE.")
                player.hp = 0

        if player.alive():
            print("Enemy defeated.")
            player.score += 50
            player.credits += 20
            player.level += 1


# ===================== GAME =====================

class Game:
    def __init__(self):
        clear()
        self.player = Player(input("Enter your alias: ") or "Anonymous")
        self.leaderboard = Leaderboard()

    def run(self):
        while self.player.lives > 0:
            CombatSystem.engage(self.player)

            if not self.player.alive():
                self.player.lose_life()
                if self.player.lives == 0:
                    break
                print(f"\nYou lost a life. Lives remaining: {self.player.lives}")
                input("Press ENTER to continue...")
                clear()
                continue

            print("\nUpgrade skill?")
            print("1. Hacking  2. Combat  3. Stealth  0. Skip")
            choice = input("> ")

            if choice == "1":
                self.player.skills.upgrade("hacking")
            elif choice == "2":
                self.player.skills.upgrade("combat")
            elif choice == "3":
                self.player.skills.upgrade("stealth")

        self.game_over()

    def game_over(self):
        clear()
        print("PERMADEATH.")
        print(f"Alias: {self.player.name}")
        print(f"Level reached: {self.player.level}")
        self.leaderboard.add(self.player.name, self.player.level)
        self.leaderboard.show()
        sys.exit()


# ===================== ENTRY =====================

if __name__ == "__main__":
    try:
        Game().run()
    except KeyboardInterrupt:
        print("\nDisconnected.")
