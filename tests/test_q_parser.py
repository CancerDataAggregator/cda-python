from cdapython import Q


def test_parser() -> None:
    qc2 = Q('tumor_stage = "Stage IIIC" OR  Diagnosis_tumor_stage = "Stage IV"')
    print(qc2.to_json())
    assert isinstance(qc2, Q)
    assert qc2.query.to_dict()["node_type"] == "OR"


test_parser()
