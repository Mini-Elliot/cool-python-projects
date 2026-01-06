import time
from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum


# -------------------- CONFIG --------------------

USER_CAPACITY = 5
USER_RATE = 1

GLOBAL_CAPACITY = 20
GLOBAL_RATE = 5

BAN_THRESHOLD = 0.6       # reject rate
BAN_DURATION = 10         # seconds
WINDOW_SECONDS = 30


# -------------------- ALGORITHMS --------------------

class Algo(Enum):
    TOKEN = "token"
    LEAKY = "leaky"


class TokenBucket:
    def __init__(self, capacity, rate):
        self.capacity = capacity
        self.tokens = capacity
        self.rate = rate
        self.last = time.time()

    def allow(self):
        now = time.time()
        self.tokens = min(
            self.capacity,
            self.tokens + (now - self.last) * self.rate
        )
        self.last = now

        if self.tokens >= 1:
            self.tokens -= 1
            return True, 0.0
        return False, (1 - self.tokens) / self.rate


class LeakyBucket:
    def __init__(self, capacity, rate):
        self.capacity = capacity
        self.queue = deque()
        self.rate = rate
        self.last = time.time()

    def allow(self):
        now = time.time()
        leaked = int((now - self.last) * self.rate)

        for _ in range(min(leaked, len(self.queue))):
            self.queue.popleft()

        if leaked:
            self.last = now

        if len(self.queue) < self.capacity:
            self.queue.append(now)
            return True, 0.0

        return False, 1 / self.rate


# -------------------- LOGGING --------------------

@dataclass
class Log:
    ts: float
    user: str
    allowed: bool
    reason: str


logs = deque(maxlen=1000)


# -------------------- STATE --------------------

user_buckets = {}
user_bans = {}
user_windows = defaultdict(deque)

global_bucket = TokenBucket(GLOBAL_CAPACITY, GLOBAL_RATE)


# -------------------- HELPERS --------------------

def is_banned(user):
    return user in user_bans and time.time() < user_bans[user]


def sliding_stats(user):
    now = time.time()
    window = user_windows[user]

    while window and now - window[0][0] > WINDOW_SECONDS:
        window.popleft()

    if not window:
        return 0, 0

    allowed = sum(1 for _, ok in window if ok)
    rejected = len(window) - allowed
    return allowed, rejected


def maybe_ban(user):
    allowed, rejected = sliding_stats(user)
    total = allowed + rejected
    if total >= 5 and rejected / total >= BAN_THRESHOLD:
        user_bans[user] = time.time() + BAN_DURATION
        print(f"[BAN] user={user} for {BAN_DURATION}s")


# -------------------- MAIN --------------------

def main():
    print("Advanced Rate Limiter Simulator")
    algo = input("Choose algorithm (token/leaky): ").strip().lower()

    if algo not in {"token", "leaky"}:
        print("Invalid algorithm.")
        return

    algo = Algo(algo)

    while True:
        user = input("> ").strip()
        if user == "exit":
            break

        now = time.time()

        if is_banned(user):
            print(f"[BANNED] user={user}")
            logs.append(Log(now, user, False, "banned"))
            continue

        if not global_bucket.allow()[0]:
            print("[GLOBAL LIMIT]")
            logs.append(Log(now, user, False, "global"))
            continue

        if user not in user_buckets:
            bucket = TokenBucket(USER_CAPACITY, USER_RATE) \
                if algo == Algo.TOKEN else \
                LeakyBucket(USER_CAPACITY, USER_RATE)
            user_buckets[user] = bucket

        allowed, _ = user_buckets[user].allow()
        user_windows[user].append((now, allowed))

        if allowed:
            print(f"[OK] user={user}")
            logs.append(Log(now, user, True, "ok"))
        else:
            print(f"[RATE LIMITED] user={user}")
            logs.append(Log(now, user, False, "user-limit"))
            maybe_ban(user)

    analyze()


# -------------------- ANALYSIS --------------------

def analyze():
    print("\n=== FINAL ANALYSIS ===")

    per_user = defaultdict(lambda: {"ok": 0, "reject": 0})

    for l in logs:
        if l.allowed:
            per_user[l.user]["ok"] += 1
        else:
            per_user[l.user]["reject"] += 1

    for user, s in per_user.items():
        total = s["ok"] + s["reject"]
        rate = s["reject"] / total if total else 0
        print(
            f"user={user} "
            f"ok={s['ok']} "
            f"reject={s['reject']} "
            f"reject_rate={rate:.1%}"
        )

    print("\nKey Observations:")
    print("- Token bucket absorbs bursts.")
    print("- Leaky bucket enforces smooth flow.")
    print("- Sliding windows detect sustained abuse.")
    print("- Temporary bans protect system health.")
    print("- Global limit prevents total collapse.")


if __name__ == "__main__":
    main()
