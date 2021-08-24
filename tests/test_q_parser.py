from cdapython.Q import Q
from cdapython.utility import single_operator_parser


def test_parser():
    qc2 = single_operator_parser(
        'ResearchSubject.Diagnosis.tumor_stage = "Stage IIIC" OR  ResearchSubject.Diagnosis.tumor_stage = "Stage IV" '
    )

    assert isinstance(qc2, Q)
    assert qc2.query.to_dict()["node_type"] == "OR"
