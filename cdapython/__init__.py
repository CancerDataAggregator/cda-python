"""
 Cdapython is a library used to interact with the machine generated CDA Python Client and offers some syntactic sugar to make it more pleasant to query the CDA.
"""
from .Q import Q
from .utility import unique_terms,columns
from ._get_unnest_clause import _get_unnest_clause
from os import getenv
from dotenv import load_dotenv
load_dotenv()

__name__ = "cdapython"
__version__ = getenv("VERISON")
__about__ ="Q {version}"
def __repr__():
    return __version__