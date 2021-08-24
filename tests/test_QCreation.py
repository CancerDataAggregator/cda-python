from cdapython import Q


def test():
    dq1 = Q('ResearchSubject.Diagnosis.tumor_stage = "Stage IIIC" ')
    dq2 = Q('ResearchSubject.Diagnosis.tumor_stage = "Stage IV" ')
    q2 = dq1.Or(dq2)

    assert isinstance(q2, Q)
    assert q2.query.to_dict()["node_type"] == "OR"
