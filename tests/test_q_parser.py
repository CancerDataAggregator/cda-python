from cdapython import Q, query


def test_parser() -> None:
    qc2 = query(
        'ResearchSubject.Diagnosis.tumor_stage = "Stage IIIC" OR  ResearchSubject.Diagnosis.tumor_stage = "Stage IV"'
    )
    print(qc2.to_json())
    assert isinstance(qc2, Q)
    assert qc2.query.to_dict()["node_type"] == "OR"


test_parser()
