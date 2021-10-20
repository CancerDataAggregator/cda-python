from cdapython import Q


def test_and_op():
    q1 = Q("ResearchSubject.Diagnosis.age_at_diagnosis > 50*365")
    q2 = Q('ResearchSubject.associated_project = "TCGA-OV"')

    q = q1.And(q2)
    r = q.run(host="https://cda.cda-dev.broadinstitute.org/")

    # assert isinstance(r.count, int) is True

test_and_op()