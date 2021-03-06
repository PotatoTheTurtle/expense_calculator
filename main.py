import csv
import sys
import datetime
from pathlib import Path

from expense_tracking import ExpenseTracking, Expense
from constants import TransferType, FUEL_STATIONS


def construct_report(path: Path):
    with path.open() as opened_csv:
        csv_reader = csv.reader(opened_csv, delimiter=";")

        expenses = []

        for row in csv_reader:
            try:
                money = row[2]
                transfer_type = row[3]
                name = row[5]
            except IndexError:
                print(f"Warning! Corrupted csv file please check, failed row: {row} (index out of bounds)")
                continue

            money = money.replace("+", "")
            if not money.replace(",", "", 1).replace("-", "", 1).isdigit():
                continue

            money = float(money.replace(",", "."))

            date = [int(number) for number in reversed(row[1].split("."))]
            date = datetime.datetime(*date)

            # This could of been done dynamically with something like "for name, age in mydict.items():",
            # but it will be slower
            if transfer_type == "KORTTIOSTO":
                transfer_type = TransferType.CARD
            elif transfer_type == "MOBILEPAY":
                transfer_type = TransferType.MOBILEPAY
            elif transfer_type == "OMA TILISIIRTO":
                transfer_type = TransferType.OWN_TRANSFER
            elif transfer_type == "TILISIIRTO":
                transfer_type = TransferType.TRANSFER
            else:
                transfer_type = None

            expense = Expense(name, transfer_type, money, date, False)

            for fuel_station in FUEL_STATIONS:
                if fuel_station.lower() in expense.name.lower():
                    expense.fuel = True

            expenses.append(expense)

        opened_csv.close()

    return expenses


def sort_expenses(expenses: [], expense_tracking: ExpenseTracking):
    for expense in expenses:

        if expense.transfer_type != TransferType.CARD and expense.transfer_type != TransferType.MOBILEPAY:
            continue

        if expense.fuel:
            expense_tracking.add_fuel(expense)
        elif expense.money >= -20:
            expense_tracking.add_low(expense)
        elif expense.money >= -40:
            expense_tracking.add_medium(expense)
        else:
            expense_tracking.add_high(expense)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("must provide path argument")
        exit(0)

    csv_file = Path(sys.argv[1])
    if not csv_file.exists():
        print("CSV file does not exist. Check path.")
        exit(1)

    transactions = construct_report(csv_file)
    expense_tracking = ExpenseTracking()
    sort_expenses(transactions, expense_tracking)

    print(expense_tracking.get_details(expense_tracking.low))
