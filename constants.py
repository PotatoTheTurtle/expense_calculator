from enum import Enum


FUEL_STATIONS = ["shell", "teboil", "neste", "ABC"]


class TransferType(Enum):
    MOBILEPAY = "MOBILEPAY"
    CARD = "KORTTIOSTO"
    OWN_TRANSFER = "OMA TILISIIRTO"
    TRANSFER = "TILISIIRTO"