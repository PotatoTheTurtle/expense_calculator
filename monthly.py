import csv
import sys
import datetime
from pathlib import Path

from data_types import ExpenseTracking, Expense
from constants import TransferType, FUEL_STATIONS


def construct_report(path: Path):
    with path.open() as opened_csv:
        csv_reader = csv.reader(opened_csv, delimiter=";")

        expenses = []

        for row in csv_reader:
            money = row[2]
            money = money.replace("+", "")
            if not money.replace(",", "", 1).replace("-", "", 1).isdigit():
                continue

            money = float(money.replace(",", "."))

            date = [int(number) for number in reversed(row[1].split("."))]
            date = datetime.datetime(*date)

            transfer_type = row[3]

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

            name = row[5]

            expense = Expense(name, transfer_type, money, date, False)

            for fuel_station in FUEL_STATIONS:
                if fuel_station.lower() in expense.name.lower():
                    expense.fuel = True

            expenses.append(expense)

        opened_csv.close()

    return expenses


def read_monthly(expenses: [], expense_tracking: ExpenseTracking):
    total = 0
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

    print(total + 1487)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("must provide path argument")
        exit()

    csv_file = Path(sys.argv[1])

    transactions = construct_report(csv_file)
    monthly_expenses = ExpenseTracking()

    read_monthly(transactions, monthly_expenses)
    print(monthly_expenses)
