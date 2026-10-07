"""
Expense Tracker
---------------
A command-line app to record, view, and summarize daily expenses.
Data is stored in a CSV file (expenses.csv) in the same folder.

Run:  python expense_tracker.py
"""

import csv
import os
from collections import defaultdict
from datetime import datetime

FILE_NAME = "expenses.csv"
FIELDS = ["date", "category", "description", "amount"]


def init_file():
    """Create the CSV file with a header row if it doesn't exist."""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(FIELDS)


def read_expenses():
    """Return all expenses as a list of dictionaries."""
    with open(FILE_NAME, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        row["amount"] = float(row["amount"])
    return rows


def add_expense():
    category = input("Category (food/travel/bills/other): ").strip().lower() or "other"
    description = input("Description: ").strip()

    try:
        amount = float(input("Amount: "))
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("Invalid amount. Enter a positive number.\n")
        return

    date_text = input("Date (YYYY-MM-DD, press Enter for today): ").strip()
    if not date_text:
        date_text = datetime.now().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date_text, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.\n")
            return

    with open(FILE_NAME, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([date_text, category, description, f"{amount:.2f}"])
    print("Expense added.\n")


def view_expenses():
    expenses = read_expenses()
    if not expenses:
        print("No expenses recorded yet.\n")
        return

    print(f"\n{'Date':<12}{'Category':<12}{'Description':<22}{'Amount':>10}")
    print("-" * 56)
    for e in expenses:
        print(f"{e['date']:<12}{e['category']:<12}{e['description'][:20]:<22}{e['amount']:>10.2f}")
    print("-" * 56)
    print(f"{'Total':<46}{sum(e['amount'] for e in expenses):>10.2f}\n")


def category_summary():
    expenses = read_expenses()
    if not expenses:
        print("No expenses recorded yet.\n")
        return

    totals = defaultdict(float)
    for e in expenses:
        totals[e["category"]] += e["amount"]

    grand_total = sum(totals.values())
    print("\nSpending by category")
    print("-" * 36)
    for category, total in sorted(totals.items(), key=lambda x: x[1], reverse=True):
        percent = total / grand_total * 100
        print(f"{category:<14}{total:>10.2f}   ({percent:.1f}%)")
    print("-" * 36)
    print(f"{'Total':<14}{grand_total:>10.2f}\n")


def monthly_report():
    month = input("Enter month (YYYY-MM): ").strip()
    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month format. Use YYYY-MM.\n")
        return

    expenses = [e for e in read_expenses() if e["date"].startswith(month)]
    if not expenses:
        print(f"No expenses found for {month}.\n")
        return

    total = sum(e["amount"] for e in expenses)
    print(f"\nReport for {month}")
    print(f"Number of expenses: {len(expenses)}")
    print(f"Total spent: {total:.2f}")
    print(f"Average per expense: {total / len(expenses):.2f}")
    biggest = max(expenses, key=lambda e: e["amount"])
    print(f"Biggest expense: {biggest['description']} ({biggest['amount']:.2f})\n")


def main():
    init_file()
    menu = {
        "1": ("Add expense", add_expense),
        "2": ("View all expenses", view_expenses),
        "3": ("Summary by category", category_summary),
        "4": ("Monthly report", monthly_report),
    }

    while True:
        print("=== Expense Tracker ===")
        for key, (label, _) in menu.items():
            print(f"{key}. {label}")
        print("5. Exit")

        choice = input("Choose an option: ").strip()
        if choice == "5":
            print("Goodbye!")
            break
        elif choice in menu:
            menu[choice][1]()
        else:
            print("Invalid choice. Try again.\n")


if __name__ == "__main__":
    main()
