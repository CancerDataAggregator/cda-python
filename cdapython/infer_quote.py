from cdapython.functions import Quoted, Unquoted
from typing import Union
from cda_client.model.query import Query
from Q import *

def infer_quote(val: Union[int, float, str, "Q", Query]) -> Query:
    if isinstance(val, (Q, Query)):
        return val
    elif isinstance(val, str) and val.startswith('"') and val.endswith('"'):
        return Quoted(val[1:-1])
    else:
        return Unquoted(val)