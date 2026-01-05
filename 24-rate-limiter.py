import time
from collections import defaultdict, deque
from dataclasses import dataclass


# -------------------- RATE LIMITERS --------------------

class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refill = time.time()

    def refill(self):
        now = time.time()
        elapsed = now - self.last_refill
        added = elapsed * self.refill_rate
        if added > 0:
            self.tokens = min(self.capacity, self.tokens + added)
            self.last_refill = now

    def allow(self):
        self.refill()
        if self.tokens >= 1:
            self.tokens -= 1
            return True, 0.0
        retry_after = (1 - self.tokens) / self.refill_rate
        return False, max(retry_after, 0.0)


class LeakyBucket:
    def __init__(self, capacity, leak_rate):
        self.capacity = capacity
        self.queue = deque()
        self.leak_rate = leak_rate
        self.last_leak = time.time()

    def leak(self):
        now = time.time()
        elapsed = now - self.last_leak
        leaked = int(elapsed * self.leak_rate)

        for _ in range(min(leaked, len(self.queue))):
            self.queue.popleft()

        if leaked > 0:
            self.last_leak = now

    def allow(self):
        self.leak()
        if len(self.queue) < self.capacity:
            self.queue.append(time.time())
            return True, 0.0

        retry_after = 1 / self.leak_rate
        return False, retry_after


# -------------------- LOGGING --------------------

@dataclass
class LogEntry:
    timestamp: float
    user: str
    allowed: bool
    retry_after: float


logs = []


# -------------------- MAIN APP --------------------

def main():
    print("Rate Limiter Simulator (Real Version)")
    print("Type: user_id to make request, or 'exit'")

    algorithm = input("Choose algorithm (token/leaky): ").strip().lower()
    if algorithm not in {"token", "leaky"}:
        print("Invalid algorithm.")
        return

    buckets = {}

    while True:
        user_input = input("> ").strip()
        if user_input == "exit":
            break

        user_id = user_input

        if user_id not in buckets:
            if algorithm == "token":
                buckets[user_id] = TokenBucket(capacity=5, refill_rate=1)
            else:
                buckets[user_id] = LeakyBucket(capacity=5, leak_rate=1)

        bucket = buckets[user_id]
        allowed, retry_after = bucket.allow()

        logs.append(
            LogEntry(time.time(), user_id, allowed, retry_after)
        )

        if allowed:
            print(f"[ALLOWED] user={user_id}")
        else:
            print(f"[REJECTED] user={user_id} retry_after={retry_after:.2f}s")

    analyze_logs()


# -------------------- ANALYSIS --------------------

def analyze_logs():
    print("\n=== Request Analysis ===")

    per_user = defaultdict(lambda: {"allowed": 0, "rejected": 0})

    for entry in logs:
        if entry.allowed:
            per_user[entry.user]["allowed"] += 1
        else:
            per_user[entry.user]["rejected"] += 1

    for user, stats in per_user.items():
        total = stats["allowed"] + stats["rejected"]
        reject_rate = stats["rejected"] / total if total else 0
        print(
            f"user={user} "
            f"allowed={stats['allowed']} "
            f"rejected={stats['rejected']} "
            f"reject_rate={reject_rate:.2%}"
        )

    print("\nInterpretation:")
    print("- Token bucket allows bursts, then recovers.")
    print("- Leaky bucket smooths traffic, rejects bursts.")
    print("- Per-user isolation prevents noisy neighbors.")


if __name__ == "__main__":
    main()
