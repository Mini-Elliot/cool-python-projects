import json
import os
from difflib import get_close_matches

BRAIN_FILE = 'chatbot_brain.json'

def load_brain():
    """Load Chatbot memory from JSON file"""
    if os.path.exists(BRAIN_FILE):
        with open(BRAIN_FILE, 'r', encoding="utf-8") as file:
            return json.load(file)
    return {}

def save_brain(knowledge):
    """Save chatbot memory to JSON file"""
    with open(BRAIN_FILE, 'w', encoding="utf-8") as file:
        json.dump(knowledge, file, indent=4)

def get_best_match_by_words(user_input: str, knowledge: dict) -> str | None:
    """Find the best match based on common words"""
    user_words = set(user_input.lower().split())
    best_match = None
    max_score = 0

    for question in knowledge.keys():
        questions_words = set(question.lower().split())
        score = len(user_words & questions_words)
        
        if score > max_score:
            max_score = score
            best_match = question
        
    return best_match if max_score > 0 else None

def get_suggestions(user_input: str, knowledge: dict, limit=3):
    """Suggest similar question if no match found."""
    return get_close_matches(user_input, list(knowledge.keys()), n=limit, cutoff=0.4)

def chatbot():
    knowledge = load_brain()
    print("Chatbot is ready ! (Press Ctrl + C to exit)")
    try:
        while True:
            user_input: str = input("You: ").strip().lower()

            if user_input in  ["exit", "bye", "quit"]:
                print("Bot: See you later. Bye 👋")
                break

            # Try word-based matching first then fall back to close match
            best_match = get_best_match_by_words(user_input, knowledge)
            
            if best_match:
                print(f"Bot: {knowledge[best_match]}")
            else:
                print("Bot: I don't know that. 🤔")

            # show suggestions
            if not best_match:
                suggestions = get_suggestions(user_input, knowledge)
                if suggestions:
                    print("Did you mean: ")
                    for i, s in enumerate(suggestions, 1):
                        print(f"{i}. {s}")

                teach = input("Do you want to teach me? (yes/no): ").strip().lower()
                if teach.startswith("y"):
                    new_answer = input("What should I reply?: ").strip()
                    knowledge[user_input] = new_answer
                    save_brain(knowledge)
                    print("Got it. I'll remember that.")
                else:
                    print("Bot: Okay may be next time.")
                
    except KeyboardInterrupt:
        print("\nBot: See you later. Bye 👋")
        save_brain(knowledge)

if __name__ == "__main__":
    default_brain: dict ={
        "hello" : "Hey there!",
        "how are you" : "I fine, thanks.",
        "what time is it": "I don't know. I don't care",
        "bye" : "See you later."
    }

    if not os.path.exists(BRAIN_FILE):
        save_brain(default_brain)

    chatbot()