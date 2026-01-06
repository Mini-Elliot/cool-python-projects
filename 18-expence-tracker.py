import json
from pathlib import Path
from datetime import date, datetime
from collections import defaultdict

DATA_FILE = Path("expenses.json")
BUDGET_LIMIT = 50000  # monthly budget (change as needed)


# ---------- Utilities ----------

def load_expenses():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)


def parse_date(text):
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        return None


# ---------- Core Features ----------

def add_expense(expenses):
    try:
        amount = float(input("Amount: "))
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("Invalid amount.")
        return

    category = input("Category: ").strip().lower()
    if not category:
        print("Category cannot be empty.")
        return

    raw_date = input("Date (YYYY-MM-DD, blank = today): ").strip()
    expense_date = date.today() if not raw_date else parse_date(raw_date)

    if not expense_date:
        print("Invalid date format.")
        return

    expenses.append({
        "amount": amount,
        "category": category,
        "date": expense_date.isoformat()
    })

    save_expenses(expenses)
    print("Expense added.")


def view_all(expenses):
    if not expenses:
        print("No expenses recorded.")
        return

    print("\nAll expenses:")
    for i, e in enumerate(expenses, 1):
        print(f"{i}. {e['date']} | {e['category']} | {e['amount']:.2f}")


def totals_by_category(expenses):
    totals = defaultdict(float)

    for e in expenses:
        totals[e["category"]] += e["amount"]

    if not totals:
        print("No data.")
        return

    print("\nTotals by category:")
    for cat, total in sorted(totals.items(), key=lambda x: x[1], reverse=True):
        print(f"{cat}: {total:.2f}")


def monthly_summary(expenses):
    month = input("Enter month (YYYY-MM): ").strip()

    try:
        target = datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid format.")
        return

    total = 0
    for e in expenses:
        d = parse_date(e["date"])
        if d and d.year == target.year and d.month == target.month:
            total += e["amount"]

    print(f"\nTotal for {month}: {total:.2f}")

    if total > BUDGET_LIMIT:
        print("⚠ Budget exceeded!")


def date_range_summary(expenses):
    start = parse_date(input("Start date (YYYY-MM-DD): ").strip())
    end = parse_date(input("End date (YYYY-MM-DD): ").strip())

    if not start or not end or start > end:
        print("Invalid date range.")
        return

    total = 0
    for e in expenses:
        d = parse_date(e["date"])
        if d and start <= d <= end:
            total += e["amount"]

    print(f"\nTotal from {start} to {end}: {total:.2f}")


def delete_expense(expenses):
    view_all(expenses)
    if not expenses:
        return

    try:
        idx = int(input("Enter expense number to delete: ")) - 1
        removed = expenses.pop(idx)
        save_expenses(expenses)
        print(f"Removed {removed['category']} expense.")
    except (ValueError, IndexError):
        print("Invalid selection.")


# ---------- Main Loop ----------

def main():
    expenses = load_expenses()

    while True:
        print("""
1. Add expense
2. View all expenses
3. Totals by category
4. Monthly summary
5. Date range summary
6. Delete expense
7. Exit
""")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_all(expenses)
        elif choice == "3":
            totals_by_category(expenses)
        elif choice == "4":
            monthly_summary(expenses)
        elif choice == "5":
            date_range_summary(expenses)
        elif choice == "6":
            delete_expense(expenses)
        elif choice == "7":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
