"""
cdapython is a library used to interact with the machine generated CDA Python Client and offers some syntactic sugar to make it more pleasant to query the CDA.
"""

from cdapython.Q import Q
from cdapython.utility import unique_terms, columns, query
from cdapython._get_unnest_clause import _get_unnest_clause
from cdapython.constantVariables import VERSION


__name__ = "cdapython"
__version__ = VERSION
__about__ = f"Q {__version__}"


def __repr__() -> str:
    return __version__
