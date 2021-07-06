"""
 Cdapython is a library used to interact with the machine generated CDA Python Client and offers some syntactic sugar to make it more pleasant to query the CDA.
"""
from .Q import Q
from .columns import columns
from .unique_terms import unique_terms
from ._get_unnest_clause import _get_unnest_clause
from os import getenv
from dotenv import load_dotenv
load_dotenv()

__name__ = "cdapython"
__version__ = getenv("VERISON")
def __repr__():
    return __version__