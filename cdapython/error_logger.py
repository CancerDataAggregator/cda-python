from rich import print

from cdapython.constant_variables import Constants


def deprecated_values(old: str, new: str) -> None:
    print(
        f" This Value {old} has been deprecated but will be converted it for you in the background please use the new value {new}"
    )
