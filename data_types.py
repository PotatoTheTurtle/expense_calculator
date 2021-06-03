import datetime
from dataclasses import dataclass, field
from constants import TransferType


@dataclass
class Expense:
    name: str
    transfer_type: TransferType
    money: float
    date: datetime.datetime
    fuel: bool

    def __str__(self):
        return f"{{name: {self.name}, type: {self.transfer_type}, money: {self.money}, date: {self.date}, fuel: {self.fuel}}}"


class ExpenseTracking:
    def __init__(self):
        self.__low = list()
        self.__medium = list()
        self.__high = list()
        self.__fuel = list()
        self.__total = 0.0

    def __str__(self):
        low_total = self.__calculate_total(self.__low)
        medium_total = self.__calculate_total(self.__medium)
        high_total = self.__calculate_total(self.__high)
        fuel_total = self.__calculate_total(self.__fuel)

        return f"Low spendings: {self.__low}\n" \
               f"Amount of purchases: {len(self.__low)}\n" \
               f"Total: {low_total}\n" \
               f"\n" \
               f"Medium spending: {self.__medium}\n" \
               f"Amount of purchases: {len(self.__medium)}\n" \
               f"Total: {medium_total}\n" \
               f"\n" \
               f"High spending: {self.__high}\n" \
               f"Amount of purchases: {len(self.__high)}\n" \
               f"Total: {high_total}\n" \
               f"\n" \
               f"Fuel: {self.__fuel}\n" \
               f"Amount of purchases: {len(self.__fuel)}\n" \
               f"Total: {fuel_total}\n" \
               f"\n" \
               f"Total: {self.__total}"

    def __calculate_total(self, expenses: list):
        total = 0
        for expense in expenses:
            total += expense.money
        return total

    @property
    def low(self):
        return self.__low

    @property
    def medium(self):
        return self.__medium

    @property
    def high(self):
        return self.__high

    @property
    def fuel(self):
        return self.__fuel

    @property
    def total(self):
        return self.__total

    def add_low(self, expense: Expense):
        self.__total += expense.money
        self.__low.append(expense)

    def add_medium(self, expense: Expense):
        self.__total += expense.money
        self.__medium.append(expense)

    def add_high(self, expense: Expense):
        self.__total += expense.money
        self.__high.append(expense)

    def add_fuel(self, expense: Expense):
        self.__total += expense.money
        self.__fuel.append(expense)