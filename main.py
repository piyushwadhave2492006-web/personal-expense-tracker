
from datetime import date, datetime
from pathlib import Path
import json

DATA_FOLDER = Path("data")
DATA_FILE = DATA_FOLDER / "expenses.json"


def load_expenses():
    if not DATA_FILE.exists():
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read expense data. Starting with an empty list.")
        return []


def save_expenses(expenses):
    DATA_FOLDER.mkdir(parents=True, exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=4)


expenses = load_expenses()


def show_menu():
    print("\n================================")
    print("       PERSONAL EXPENSE TRACKER")
    print("================================")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Search Expenses")
    print("4. Spending Reports")
    print("5. Delete Expense")
    print("6. Exit")


def add_expense():
    print("\n--------- ADD EXPENSE ---------")

    try:
        amount = float(input("Enter amount: ₹"))
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
    except ValueError:
        print("Invalid amount. Enter a number, such as 120 or 45.50.")
        return

    category = input("Enter category: ").strip()
    description = input("Enter description: ").strip()

    if not category or not description:
        print("Category and description cannot be empty.")
        return

    expense_date = input(
        "Enter date (YYYY-MM-DD) [Enter for today]: "
    ).strip()

    if not expense_date:
        expense_date = str(date.today())
    else:
        try:
            datetime.strptime(expense_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD, such as 2026-10-26.")
            return

    expense = {
        "amount": amount,
        "category": category,
        "description": description,
        "date": expense_date
    }

    expenses.append(expense)
    save_expenses(expenses)
    print("Expense added successfully!")


def display_expenses(expense_list):
    if not expense_list:
        print("No expenses found.")
        return

    print("-" * 80)
    print(
        f"{'No.':<5}"
        f"{'Date':<13}"
        f"{'Category':<16}"
        f"{'Description':<26}"
        f"{'Amount':>12}"
    )
    print("-" * 80)

    for index, expense in enumerate(expense_list, start=1):
        print(
            f"{index:<5}"
            f"{expense['date']:<13}"
            f"{expense['category'][:15]:<16}"
            f"{expense['description'][:25]:<26}"
            f"₹{expense['amount']:>10.2f}"
        )

    print("-" * 80)


def view_expenses():
    print("\n--------- ALL EXPENSES ---------")
    display_expenses(expenses)


def search_expenses():
    print("\n--------- SEARCH EXPENSES ---------")
    print("1. Search by Category")
    print("2. Search by Description")
    print("3. Search by Date")

    choice = input("Choose search type: ").strip()

    if choice == "1":
        field = "category"
        term = input("Enter category: ").strip().casefold()
    elif choice == "2":
        field = "description"
        term = input("Enter description: ").strip().casefold()
    elif choice == "3":
        field = "date"
        term = input("Enter date (YYYY-MM-DD): ").strip()
    else:
        print("Invalid search option.")
        return

    if not term:
        print("Search term cannot be empty.")
        return

    if field == "date":
        results = [
            expense for expense in expenses
            if expense["date"] == term
        ]
    else:
        results = [
            expense for expense in expenses
            if term in expense[field].casefold()
        ]

    print("\n--------- SEARCH RESULTS ---------")
    display_expenses(results)


def show_reports():
    print("\n--------- SPENDING REPORT ---------")

    if not expenses:
        print("No expenses available for reports.")
        return

    total_spending = sum(expense["amount"] for expense in expenses)
    expense_count = len(expenses)
    average_spending = total_spending / expense_count

    category_totals = {}

    for expense in expenses:
        category = expense["category"].strip().title()
        category_totals[category] = (
            category_totals.get(category, 0) + expense["amount"]
        )

    print(f"\nTotal spending: ₹{total_spending:.2f}")
    print(f"Number of expenses: {expense_count}")
    print(f"Average per expense: ₹{average_spending:.2f}")

    print("\nCategory-wise spending:")
    for category, amount in sorted(category_totals.items()):
        print(f"{category:<20} ₹{amount:.2f}")

    highest_category = max(category_totals, key=category_totals.get)
    print(
        f"\nHighest spending category: {highest_category} "
        f"(₹{category_totals[highest_category]:.2f})"
    )


def delete_expense():
    print("\n--------- DELETE EXPENSE ---------")

    if not expenses:
        print("There are no expenses to delete.")
        return

    display_expenses(expenses)

    try:
        number = int(input("Enter the expense number to delete (0 to cancel): "))
    except ValueError:
        print("Please enter a valid whole number.")
        return

    if number == 0:
        print("Deletion cancelled.")
        return

    if number < 1 or number > len(expenses):
        print("Invalid expense number.")
        return

    removed = expenses.pop(number - 1)
    save_expenses(expenses)

    print(
        f"Deleted: {removed['category']} - "
        f"{removed['description']} (₹{removed['amount']:.2f})"
    )


def main():
    while True:
        show_menu()
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            search_expenses()
        elif choice == "4":
            show_reports()
        elif choice == "5":
            delete_expense()
        elif choice == "6":
            print("Thank you for using Expense Tracker!")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
