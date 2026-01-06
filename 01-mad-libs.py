import random
import time

# ---------------- CONFIG ----------------
DEFAULT_SEED = None          # set to an int for reproducible stories
PRINT_DELAY = 0.015          # seconds per character
OPTIONAL_FILL_PROB = 0.3     # chance to auto-fill optional words


# ---------------- LINGUISTICS ----------------
IRREGULAR_ING = {
    "die": "dying",
    "lie": "lying",
    "tie": "tying",
    "fix": "fixing",
    "run": "running",
    "swim": "swimming",
}


def verb_ing(verb: str) -> str:
    if verb in IRREGULAR_ING:
        return IRREGULAR_ING[verb]

    if verb.endswith("e") and verb != "be":
        return verb[:-1] + "ing"

    if (
        len(verb) >= 3 and
        verb[-1] not in "aeiou" and
        verb[-2] in "aeiou" and
        verb[-3] not in "aeiou"
    ):
        return verb + verb[-1] + "ing"

    return verb + "ing"


# ---------------- INPUT ----------------
def get_input(prompt: str, example: str | None = None) -> str:
    while True:
        msg = f"Enter a {prompt}"
        if example:
            msg += f" (e.g. {example})"
        value = input(msg + ": ").strip().lower()

        if value and value.isalpha():
            return value

        print("Please enter alphabetic text only.")


def collect_words(prompts: list[tuple[str, str, str | None]]) -> dict:
    random.shuffle(prompts)
    words = {}

    for key, kind, example in prompts:
        words[key] = get_input(kind, example)

    # optional auto-fill for extra flavor
    if random.random() < OPTIONAL_FILL_PROB:
        words.setdefault("adj3", "absolutely unhinged")

    return words


# ---------------- TEMPLATES ----------------
TEMPLATES = [
    {
        "required": {"noun1", "noun2", "verb1", "verb2", "adj1", "adj2", "adj3"},
        "text": """
One sunny morning, a {adj1} {noun1} woke up with an unstoppable urge to {verb1}.
Without thinking twice, the {noun1} started {verb1_ing} everywhere—
on the table, on the floor, and in places where it absolutely shouldn’t.

Suddenly, a {adj2} {noun2} appeared.
After a long stare, it shrugged and joined in.
Soon, both of them were {verb2_ing} like two {adj3} legends.

History would never forget that day.
"""
    },
    {
        "required": {"noun1", "noun2", "verb1", "verb2", "adj1", "adj2", "adj3"},
        "text": """
The {adj1} {noun1} was known across the land for one thing: {verb1_ing}.
No one questioned it—until a {adj2} {noun2} showed up.

Instead of stopping the chaos, the two teamed up and went off {verb2_ing}.
Some called them foolish. Others called them {adj3}.

They preferred the word “iconic.”
"""
    }
]


def generate_story(words: dict) -> str:
    enriched = dict(words)
    enriched["verb1_ing"] = verb_ing(words["verb1"])
    enriched["verb2_ing"] = verb_ing(words["verb2"])

    valid_templates = [
        t for t in TEMPLATES
        if t["required"].issubset(enriched.keys())
    ]

    template = random.choice(valid_templates)
    return template["text"].format(**enriched)


# ---------------- OUTPUT ----------------
def slow_print(text: str, delay: float = PRINT_DELAY):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


# ---------------- GAME LOOP ----------------
def play(seed: int | None = DEFAULT_SEED):
    if seed is not None:
        random.seed(seed)

    prompts = [
        ("noun1", "noun", "cat"),
        ("noun2", "noun", "robot"),
        ("verb1", "verb", "dance"),
        ("verb2", "verb", "escape"),
        ("adj1", "adjective", "sleepy"),
        ("adj2", "adjective", "suspicious"),
        ("adj3", "adjective", "legendary"),
    ]

    while True:
        words = collect_words(prompts)
        story = generate_story(words)

        print("\n--- Your Story ---\n")
        slow_print(story)

        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye.")
            break


# ---------------- ENTRY ----------------
if __name__ == "__main__":
    play()
