from cdapython import Q
from cdapython.exceptions.custom_exception import QSyntaxError
import pytest


def testing_syntax() -> None:
    with pytest.raises(QSyntaxError):
        Q("'has and leg' from")
