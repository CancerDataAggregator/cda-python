from rich import print


def deprecated_values(old: str, new: str) -> None:
    print("ran error_logger.py deprecated_values")
    print(
        f" This Value {old} has been deprecated but will be converted it for you in the background please use the new value {new}"
    )
