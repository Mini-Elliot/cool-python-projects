import random
import time
from typing import Optional


class Linguistics:
    IRREGULAR_ING = {
        "die": "dying",
        "lie": "lying",
        "tie": "tying",
        "fix": "fixing",
        "run": "running",
        "swim": "swimming",
    }

    @classmethod
    def verb_ing(cls, verb: str) -> str:
        if verb in cls.IRREGULAR_ING:
            return cls.IRREGULAR_ING[verb]

        if verb.endswith("e") and verb != "be":
            return verb[:-1] + "ing"

        if (
            len(verb) >= 3
            and verb[-1] not in "aeiou"
            and verb[-2] in "aeiou"
            and verb[-3] not in "aeiou"
        ):
            return verb + verb[-1] + "ing"

        return verb + "ing"


class StoryEngine:
    def __init__(self):
        self.templates = [
            {
                "required": {
                    "noun1", "noun2", "verb1", "verb2",
                    "adj1", "adj2", "adj3"
                },
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
                "required": {
                    "noun1", "noun2", "verb1", "verb2",
                    "adj1", "adj2", "adj3"
                },
                "text": """
The {adj1} {noun1} was known across the land for one thing: {verb1_ing}.
No one questioned it—until a {adj2} {noun2} showed up.

Instead of stopping the chaos, the two teamed up and went off {verb2_ing}.
Some called them foolish. Others called them {adj3}.

They preferred the word “iconic.”
"""
            }
        ]

    def generate(self, words: dict) -> str:
        enriched = dict(words)
        enriched["verb1_ing"] = Linguistics.verb_ing(words["verb1"])
        enriched["verb2_ing"] = Linguistics.verb_ing(words["verb2"])

        valid = [
            t for t in self.templates
            if t["required"].issubset(enriched.keys())
        ]

        template = random.choice(valid)
        return template["text"].format(**enriched)


class ConsoleUI:
    def __init__(self, print_delay: float = 0.015):
        self.print_delay = print_delay

    def slow_print(self, text: str):
        for char in text:
            print(char, end="", flush=True)
            time.sleep(self.print_delay)
        print()

    def get_input(self, kind: str, example: Optional[str] = None) -> str:
        while True:
            msg = f"Enter a {kind}"
            if example:
                msg += f" (e.g. {example})"
            value = input(msg + ": ").strip().lower()

            if value and value.isalpha():
                return value

            print("Please enter alphabetic text only.")


class MadLibsGame:
    def __init__(
        self,
        seed: Optional[int] = None,
        optional_fill_prob: float = 0.3,
        print_delay: float = 0.015
    ):
        self.optional_fill_prob = optional_fill_prob
        self.ui = ConsoleUI(print_delay)
        self.engine = StoryEngine()

        if seed is not None:
            random.seed(seed)

        self.prompts = [
            ("noun1", "noun", "cat"),
            ("noun2", "noun", "robot"),
            ("verb1", "verb", "dance"),
            ("verb2", "verb", "escape"),
            ("adj1", "adjective", "sleepy"),
            ("adj2", "adjective", "suspicious"),
            ("adj3", "adjective", "legendary"),
        ]

    def collect_words(self) -> dict:
        random.shuffle(self.prompts)
        words = {}

        for key, kind, example in self.prompts:
            words[key] = self.ui.get_input(kind, example)

        if random.random() < self.optional_fill_prob:
            words.setdefault("adj3", "absolutely unhinged")

        return words

    def run(self):
        while True:
            words = self.collect_words()
            story = self.engine.generate(words)

            print("\n--- Your Story ---\n")
            self.ui.slow_print(story)

            again = input("\nPlay again? (y/n): ").strip().lower()
            if again != "y":
                print("Goodbye.")
                break
