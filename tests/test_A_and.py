from cdapython import Q
from tests.global_settings import host, table


def test_and_op():
    q1 = Q("ResearchSubject.Diagnosis.age_at_diagnosis > 50*365")
    q2 = Q('ResearchSubject.associated_project = "TCGA-OV"')

    q = q1.AND(q2)
    a = q.to_dict()
    print(a)
    assert a["node_type"] == "AND"


test_and_op()
