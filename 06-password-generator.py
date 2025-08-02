import secrets
import string


def contains_upper(password: str) -> bool:
    for char in password:
        if char.isupper():
            return True

    return False


def contain_symbol(password: str) -> bool:
    for char in password:
        if char in string.punctuation:
            return True

    return False


def generate_password(length: int, symbols: bool, uppercase: bool) -> str:
    combination: str = string.ascii_lowercase + string.digits

    if symbols:
        combination += string.punctuation

    if uppercase:
        combination += string.ascii_uppercase

    combination_length = len(combination)
    new_password: str = ''

    for _ in range(length):
        new_password += combination[secrets.randbelow(combination_length)]

    return new_password


def main():
    uppercase = False
    symbols = False
    try:
        # Welcome message
        print("Welcome to password generator.")

        while True:
            # Queries
            pass_length: int = int(input("\rEnter a number for length of password > "))
            for_uppercase: str = input("\rDo you want uppercase letters in your password (y/n) > ").strip().lower()
            for_symbols: str = input("\rDo you want symbols in your passwords (y/n) > ").strip().lower()

            # To check uppercase condition
            if for_uppercase == "y":
                uppercase = True
            elif for_uppercase == "n":
                uppercase = False
            else:
                print("Please, enter a correct choice.")

            # To check symbols condition
            if for_symbols == "y":
                symbols = True
            elif for_symbols == "n":
                symbols = False
            else:
                print("Please, enter a correct choice.")

            for i in range(1, 6):
                new_pass: str = generate_password(pass_length, uppercase, symbols)
                specs: str = f'Contains Uppercase: {contains_upper(new_pass)}, Contains Symbols: {contain_symbol(new_pass)}'
                print(f"{i} -> {new_pass} ({specs})")
            choice: str = input("Do you want to generate more passwords? (y/n) > ").strip().lower()
            if choice == "y":
                continue
            elif choice == "n":
                break
            else:
                print("Please, enter a valid choice.")
    except KeyboardInterrupt:
        print("Ctrl + C detected. Exiting program.")


if __name__ == "__main__":
    main()
