from cdapython.exceptions.custom_exception import QSyntaxError


def check_keyword(value: str) -> None:
    keywords = ["AND", "OR", "NOT", "FROM", "IN", "LIKE", "IS"]
    check = value.lower() in [str(i).lower() for i in keywords]
    if check:
        raise QSyntaxError(keyword=value)
