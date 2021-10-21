from cdapython import Q
from time import sleep

def test_and_op():
    sleep(1)
    q1 = Q("ResearchSubject.Diagnosis.age_at_diagnosis > 50*365")
    q2 = Q('ResearchSubject.associated_project = "TCGA-OV"')

    q = q1.And(q2)
    r = q.run()

    assert isinstance(r.count, int) is True
