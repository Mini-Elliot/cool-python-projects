import json
import os
import random
import re
from difflib import SequenceMatcher

BRAIN_FILE = "chatbot_brain.json"

STOPWORDS = {
    "what", "is", "are", "you", "me", "tell", "about",
    "the", "a", "an", "do", "does", "can", "please"
}

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text.strip()

def keywords(text: str) -> set:
    return {w for w in normalize(text).split() if w not in STOPWORDS}

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

def load_brain():
    if os.path.exists(BRAIN_FILE):
        with open(BRAIN_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_brain(brain):
    with open(BRAIN_FILE, "w", encoding="utf-8") as f:
        json.dump(brain, f, indent=4)

def find_best_match(user_input: str, brain: dict):
    user_keys = keywords(user_input)
    best_score = 0
    best_entry = None

    for main_q, data in brain.items():
        all_phrases = [main_q] + data.get("aliases", [])
        for phrase in all_phrases:
            phrase_keys = keywords(phrase)
            overlap = len(user_keys & phrase_keys)

            score = overlap + similarity(user_input, phrase)

            if score > best_score:
                best_score = score
                best_entry = data

    return best_entry if best_score >= 1.2 else None

def chatbot():
    brain = load_brain()
    print("Chatbot ready. Type 'exit' to quit.\n")

    try:
        while True:
            user_input = input("You: ").strip()
            if not user_input:
                continue

            if user_input.lower() in {"exit", "quit", "bye"}:
                print("Bot: Goodbye 👋")
                break

            entry = find_best_match(user_input, brain)

            if entry:
                print("Bot:", random.choice(entry["responses"]))
            else:
                print("Bot: I don't know that yet.")

                teach = input("Teach me? (y/n): ").lower()
                if teach.startswith("y"):
                    answer = input("What should I reply?: ").strip()
                    key = normalize(user_input)

                    brain[key] = {
                        "aliases": [],
                        "responses": [answer],
                        "tags": []
                    }

                    save_brain(brain)
                    print("Bot: Learned 👍")

    except KeyboardInterrupt:
        print("\nBot: Bye 👋")
        save_brain(brain)

if __name__ == "__main__":
    chatbot()
