import json
import random
import string
from pathlib import Path

DATA_FILE = Path("urls.json")
CODE_LENGTH = 6
ALPHABET = string.ascii_letters + string.digits


def load_urls():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}


def save_urls(urls):
    with open(DATA_FILE, "w") as f:
        json.dump(urls, f, indent=2)


def generate_code(existing_codes):
    while True:
        code = "".join(random.choice(ALPHABET) for _ in range(CODE_LENGTH))
        if code not in existing_codes:
            return code


def shorten_url(urls):
    long_url = input("Enter URL: ").strip()

    if not long_url.startswith(("http://", "https://")):
        print("URL must start with http:// or https://")
        return

    code = generate_code(urls)
    urls[code] = long_url
    save_urls(urls)

    print(f"Short code: {code}")


def resolve_url(urls):
    code = input("Enter short code: ").strip()

    if code in urls:
        print(f"Original URL: {urls[code]}")
    else:
        print("Code not found.")


def main():
    urls = load_urls()

    while True:
        print("\n1. Shorten URL")
        print("2. Resolve URL")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            shorten_url(urls)
        elif choice == "2":
            resolve_url(urls)
        elif choice == "3":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
