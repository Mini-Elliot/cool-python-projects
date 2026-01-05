import json
from pathlib import Path
from datetime import date

DATA_FILE = Path("expenses.json")


def load_expenses():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)


def add_expense(expenses):
    try:
        amount = float(input("Amount: "))
    except ValueError:
        print("Invalid amount.")
        return

    category = input("Category: ").strip().lower()
    expense_date = input("Date (YYYY-MM-DD, blank = today): ").strip()

    if not expense_date:
        expense_date = date.today().isoformat()

    expenses.append({
        "amount": amount,
        "category": category,
        "date": expense_date
    })

    save_expenses(expenses)
    print("Expense added.")


def view_totals_by_category(expenses):
    totals = {}

    for expense in expenses:
        category = expense["category"]
        totals[category] = totals.get(category, 0) + expense["amount"]

    if not totals:
        print("No expenses recorded.")
        return

    print("\nTotals by category:")
    for category, total in totals.items():
        print(f"{category}: {total:.2f}")


def main():
    expenses = load_expenses()

    while True:
        print("\n1. Add expense")
        print("2. View totals by category")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_totals_by_category(expenses)
        elif choice == "3":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
