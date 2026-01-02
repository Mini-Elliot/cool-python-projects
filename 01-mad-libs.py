import random

def get_input(prompt):
    while True:
        value = input(f"Enter a {prompt}: ").strip()
        if value:
            return value.lower()
        print("Input cannot be empty.")

def verb_ing(verb):
    if verb.endswith("e") and verb != "be":
        return verb[:-1] + "ing"
    if len(verb) >= 3 and verb[-1] not in "aeiou" and verb[-2] in "aeiou":
        return verb + verb[-1] + "ing"
    return verb + "ing"

def collect_words():
    prompts = {
        "noun1": "noun",
        "noun2": "noun",
        "verb1": "verb",
        "verb2": "verb",
        "adj1": "adjective",
        "adj2": "adjective",
        "adj3": "adjective"
    }

    return {key: get_input(value) for key, value in prompts.items()}

def generate_story(words):
    templates = [
        f"""
One sunny morning, a {words['adj1']} {words['noun1']} woke up with an unstoppable urge to {words['verb1']}.
Without thinking twice, the {words['noun1']} started {verb_ing(words['verb1'])} everywhere—
on the table, on the floor, and in places where it absolutely shouldn’t.

Suddenly, a {words['adj2']} {words['noun2']} appeared.
After a long stare, it shrugged and joined in.
Soon, both of them were {verb_ing(words['verb2'])} like two {words['adj3']} legends.

History would never forget that day.
""",

        f"""
The {words['adj1']} {words['noun1']} was known across the land for one thing: {verb_ing(words['verb1'])}.
No one questioned it—until a {words['adj2']} {words['noun2']} showed up.

Instead of stopping the chaos, the two teamed up and went off {verb_ing(words['verb2'])}.
Some called them foolish. Others called them {words['adj3']}.

They preferred the word “iconic.”
"""
    ]

    return random.choice(templates)

def play():
    while True:
        words = collect_words()
        story_text = generate_story(words)
        print(story_text)

        again = input("Play again? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye.")
            break

if __name__ == "__main__":
    play()
