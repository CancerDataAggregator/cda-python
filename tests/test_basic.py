from cdapython import Q


def test1():
    q1 = Q('Diagnosis.age_at_diagnosis >= 50')
    print(q1)
    assert q1.query.node_type == ">="

