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

    def PRINT_Q_ERROR(self) -> str:
        return f'{self.message} -> Q operator "{self.keyword}" is not uppercase. Please use "{self.keyword.upper()}" instead'

    def __str__(self) -> str:
        return self.PRINT_Q_ERROR()

    def __repr__(self) -> str:
        return self.PRINT_Q_ERROR()
