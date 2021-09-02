"""
 Cdapython is a library used to interact with the machine generated CDA Python Client and offers some syntactic sugar to make it more pleasant to query the CDA.
"""
from .Q import Q
from .utility import unique_terms, columns, single_operator_parser
from ._get_unnest_clause import _get_unnest_clause
from os import getenv
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

__name__ = "cdapython"
__version__ = getenv("VERSION")
__about__ = f"Q {__version__}"


def __repr__() -> Optional[str]:
    return __version__
