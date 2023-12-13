from typing import List

from cdapython.exceptions.custom_exception import QSyntaxError


def check_keyword(value: str) -> None:
    print("ran check_case.py check_keyword")
    keywords: List[str] = ["AND", "OR", "NOT", "FROM", "IN", "LIKE", "IS"]
    check: bool = value.lower() in [str(i).lower() for i in keywords]
    if check:
        raise QSyntaxError(keyword=value)
