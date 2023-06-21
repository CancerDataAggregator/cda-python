import json
from typing import List, TypedDict, Union

from cda_client.exceptions import ApiException, ServiceException


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


class HTTP_ERROR_API(ApiException):
    """_summary_
    This is a
    Args:
        ApiException (_type_): _description_
    """

    def __init__(
        self,
        http_error: Union[ServiceException, ApiException],
        message: str = "HTTP ERROR",
    ) -> None:
        self.message = message
        if http_error.body:
            http_dict = json.loads(http_error.body)
            if "error" in http_dict:
                self.error = http_dict["error"]
                self.statusCode = http_dict["status"]
            if "causes" in http_dict:
                self.error = http_dict["message"]
                self.statusCode = http_dict["statusCode"]

        super().__init__(reason=self.message)

    def PRINT_Q_ERROR(self) -> str:
        return f"""
                {self.message}
                Http Status: {self.statusCode}
                Error Message: {self.error}
            """

    def __str__(self) -> str:
        return self.PRINT_Q_ERROR()

    def __repr__(self) -> str:
        return self.PRINT_Q_ERROR()


class HTTP_ERROR_SERVICE(HTTP_ERROR_API):
    def __init__(self, http_error: ServiceException) -> None:
        super().__init__(http_error=http_error)


class CSV_TSV_NO_KEY(Exception):
    """
    This Exception will raise a Error/
    if there is no key
    Args:
        Exception (_type_): _description_
    """

    pass
