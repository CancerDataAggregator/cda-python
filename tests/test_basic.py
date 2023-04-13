from cdapython import Q


def test_basic() -> None:
    q1 = Q("age_at_diagnosis >= 50")
    print(q1)
    assert q1.query.node_type == ">="
