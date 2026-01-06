import json
import os
import random
import re
from difflib import SequenceMatcher
from collections import defaultdict

BRAIN_FILE = "chatbot_brain.json"

STOPWORDS = {
    "what", "is", "are", "you", "me", "tell", "about",
    "the", "a", "an", "do", "does", "can", "please"
}

# ---------------- NLP Utilities ----------------

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text.strip()

def tokenize(text: str) -> list:
    return [w for w in normalize(text).split() if w not in STOPWORDS]

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

# ---------------- Brain Handling ----------------

def migrate_brain(raw: dict) -> dict:
    """Convert old flat brain format into structured intents"""
    new_brain = {}

    for k, v in raw.items():
        intent = normalize(k)

        if isinstance(v, dict):
            new_brain[intent] = v
        else:
            new_brain[intent] = {
                "patterns": [intent],
                "responses": v if isinstance(v, list) else [v],
                "tags": [],
                "confidence": 1.0
            }

    return new_brain

def load_brain():
    if not os.path.exists(BRAIN_FILE):
        return {}

    with open(BRAIN_FILE, "r", encoding="utf-8") as f:
        raw = json.load(f)

    return migrate_brain(raw)

def save_brain(brain):
    with open(BRAIN_FILE, "w", encoding="utf-8") as f:
        json.dump(brain, f, indent=4)

# ---------------- Intelligence Core ----------------

class Context:
    def __init__(self):
        self.last_intent = None

context = Context()

def intent_score(user_tokens, pattern_tokens, user_text, pattern_text):
    overlap = len(set(user_tokens) & set(pattern_tokens))
    seq_sim = similarity(user_text, pattern_text)
    return overlap * 1.2 + seq_sim

def find_intent(user_input, brain):
    user_tokens = tokenize(user_input)
    best_score = 0
    best_intent = None

    for intent, data in brain.items():
        for pattern in data["patterns"]:
            score = intent_score(
                user_tokens,
                tokenize(pattern),
                user_input,
                pattern
            )

            if intent == context.last_intent:
                score *= 1.1  # context bias

            if score > best_score:
                best_score = score
                best_intent = intent

    return best_intent if best_score >= 1.5 else None

def generate_response(intent, brain):
    responses = brain[intent]["responses"]
    response = random.choice(responses)

    context.last_intent = intent
    return response

# ---------------- Learning ----------------

def learn(user_input, brain):
    normalized = normalize(user_input)

    intent = normalized.replace(" ", "_")

    response = input("What should I reply?: ").strip()
    if not response:
        return

    brain[intent] = {
        "patterns": [normalized],
        "responses": [response],
        "tags": [],
        "confidence": 0.5
    }

    save_brain(brain)
    print("Bot: Learned new intent.")

# ---------------- Chat Loop ----------------

def chatbot():
    brain = load_brain()
    print("AI Chatbot ready. Type 'exit' to quit.\n")

    try:
        while True:
            user_input = input("You: ").strip()
            if not user_input:
                continue

            if user_input.lower() in {"exit", "quit", "bye"}:
                print("Bot: Goodbye 👋")
                break

            intent = find_intent(user_input, brain)

            if intent:
                print("Bot:", generate_response(intent, brain))
            else:
                print("Bot: I’m not sure what you mean.")

                teach = input("Teach me? (y/n): ").lower()
                if teach.startswith("y"):
                    learn(user_input, brain)

    except KeyboardInterrupt:
        print("\nBot: Bye 👋")
        save_brain(brain)

if __name__ == "__main__":
    chatbot()
