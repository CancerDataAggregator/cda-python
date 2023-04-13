from cdapython import Q


def test_q_or_op():
    dq1 = Q('Diagnosis_stage = "Stage IIIC" ')
    dq2 = Q('Diagnosis_stage = "Stage IV" ')
    q2 = dq1.OR(dq2)

    assert isinstance(q2, Q)
    assert q2.query.to_dict()["node_type"] == "OR"
