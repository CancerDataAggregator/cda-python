from cdapython.Q import Q
from cdapython.utility import query


def test_parser() -> None:
    qc2 = query(
        'ResearchSubject.Diagnosis.tumor_stage = "Stage IIIC" OR  ResearchSubject.Diagnosis.tumor_stage = "Stage IV" '
    )

    assert isinstance(qc2, Q)
    assert qc2.query.to_dict()["node_type"] == "OR"
