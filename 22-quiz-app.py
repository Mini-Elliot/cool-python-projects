import random

QUESTIONS = [
    {
        "question": "What is 2 + 2?",
        "options": ["3", "4", "5", "6"],
        "answer": "4",
        "difficulty": 1
    },
    {
        "question": "Which keyword defines a function in Python?",
        "options": ["func", "define", "def", "lambda"],
        "answer": "def",
        "difficulty": 1
    },
    {
        "question": "What does HTTP stand for?",
        "options": [
            "HyperText Transfer Protocol",
            "High Transfer Text Process",
            "Host Text Transmission Program",
            "Hyperlink Transfer Tool"
        ],
        "answer": "HyperText Transfer Protocol",
        "difficulty": 2
    },
    {
        "question": "Which data structure has O(1) average lookup?",
        "options": ["List", "Tuple", "Set", "Stack"],
        "answer": "Set",
        "difficulty": 2
    },
    {
        "question": "What is a closure in Python?",
        "options": [
            "A loop inside a function",
            "A function remembering its outer scope",
            "A sealed class",
            "A private variable"
        ],
        "answer": "A function remembering its outer scope",
        "difficulty": 3
    },
    {
        "question": "Which sorting algorithm has O(n log n) worst-case time?",
        "options": ["Bubble Sort", "Insertion Sort", "Merge Sort", "Selection Sort"],
        "answer": "Merge Sort",
        "difficulty": 3
    }
]


def get_questions_by_difficulty(difficulty):
    return [q for q in QUESTIONS if q["difficulty"] == difficulty]


def ask_question(question):
    print("\n" + question["question"])
    for idx, option in enumerate(question["options"], start=1):
        print(f"{idx}. {option}")

    choice = input("Your answer (number): ").strip()

    if not choice.isdigit():
        return False

    index = int(choice) - 1
    if index < 0 or index >= len(question["options"]):
        return False

    return question["options"][index] == question["answer"]


def main():
    difficulty = 2
    score = 0
    rounds = 0

    print("Adaptive Quiz (type Ctrl+C to quit)")

    try:
        while True:
            available = get_questions_by_difficulty(difficulty)

            if not available:
                print("No questions at this difficulty.")
                break

            question = random.choice(available)
            correct = ask_question(question)

            rounds += 1

            if correct:
                print("Correct.")
                score += 1
                difficulty = min(3, difficulty + 1)
            else:
                print(f"Wrong. Correct answer: {question['answer']}")
                difficulty = max(1, difficulty - 1)

            print(f"Current difficulty: {difficulty}")

    except KeyboardInterrupt:
        print("\n\nQuiz ended.")

    print(f"\nFinal score: {score}/{rounds}")


if __name__ == "__main__":
    main()
