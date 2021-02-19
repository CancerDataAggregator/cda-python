from cdapython import Q, _get_unnest_clause


def test1():
    q1 = Q('Diagnosis.age_at_diagnosis >= 50')
    assert q1.query.node_type == ">="


def test_unique():
    col_name, unnest = _get_unnest_clause("A")
    assert col_name == "A"
    assert unnest == []

    col_name, unnest = _get_unnest_clause("A.col")
    assert col_name == "_A.col"
    assert unnest == ["UNNEST(A) AS _A"]

    col_name, unnest = _get_unnest_clause("A.B.col")
    assert col_name == "_B.col"
    assert unnest == ["UNNEST(A) AS _A", "UNNEST(_A.B) AS _B"]

    col_name, unnest = _get_unnest_clause("A.B.C.col")
    assert col_name == "_C.col"
    assert unnest == ["UNNEST(A) AS _A", "UNNEST(_A.B) AS _B", "UNNEST(_B.C) AS _C"]
