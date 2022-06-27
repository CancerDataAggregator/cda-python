class QSQLError(Exception):
    """Just made for readability

    Args:
        Exception (_type_): _description_
    """

    pass


class WRONGDATABASEError(Exception):
    """Just made for readability

    Args:
        Exception (_type_): _description_
    """

    pass


class QSyntaxError(SyntaxError):
    def __init__(self, keyword: str, message: str = "Q Syntax Error") -> None:
        self.message = message
        self.keyword = keyword
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.message} -> {self.keyword} in Q statement is not allowed only uppercase operators"
