import re

COMMON_PASSWORDS = {
    "password", "123456", "12345678", "qwerty",
    "abc123", "password1", "admin", "letmein"
}

SEQUENCES = [
    "1234", "abcd", "qwerty"
]


def check_password(password: str):
    score = 0
    feedback = []

    # Length
    if len(password) >= 12:
        score += 3
    elif len(password) >= 8:
        score += 2
    else:
        feedback.append("Use at least 8 characters.")

    # Character variety
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add lowercase letters.")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letters.")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Add numbers.")

    if re.search(r"[^\w\s]", password):
        score += 1
    else:
        feedback.append("Add special characters.")

    # Common passwords
    if password.lower() in COMMON_PASSWORDS:
        score -= 3
        feedback.append("This password is too common.")

    # Repeated characters
    if re.search(r"(.)\1{2,}", password):
        score -= 1
        feedback.append("Avoid repeated characters.")

    # Sequential patterns
    for seq in SEQUENCES:
        if seq in password.lower():
            score -= 1
            feedback.append("Avoid sequential patterns.")
            break

    score = max(score, 0)
    return score, feedback


def strength_label(score: int):
    if score <= 3:
        return "Weak"
    elif score <= 6:
        return "Moderate"
    elif score <= 8:
        return "Strong"
    else:
        return "Very Strong"


def main():
    password = input("Enter a password: ")

    score, feedback = check_password(password)
    label = strength_label(score)

    print(f"\nStrength: {label} ({score}/10)")

    if feedback:
        print("Suggestions:")
        for item in feedback:
            print(f"- {item}")
    else:
        print("Good password. No obvious weaknesses detected.")


if __name__ == "__main__":
    main()
