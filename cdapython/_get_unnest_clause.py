# column ->
# SELECT DISTINCT(column)

# D.column ->
# SELECT DISTINCT(_D.column) FROM TABLE, UNNEST(D) AS _D

# A.B.C.D.column ->
# SELECT DISTINCT(_D.column) FROM TABLE, UNNEST(A) AS _A, UNNEST(_A.B) AS _B, UNNEST(_B.C) AS _C, UNNEST(_C.D) AS _D

from typing import List, Tuple, Union


def _get_unnest_clause(col_name: str) -> Tuple[str, List[str]]:
    _new_col, _unnest = col_name, []
    c = col_name.split(".")
    if len(c) > 1:
        _new_col = f"_{c[-2]}.{c[-1]}"
        _unnest = [f"UNNEST({c[0]}) AS _{c[0]}"]
        for n in range(1, len(c) - 1):
            _unnest += [f"UNNEST(_{c[n - 1]}.{c[n]}) AS _{c[n]}"]

    return _new_col, _unnest
