from cdapython import Q


def test_and_op():
    q1 = Q("age_at_diagnosis > 50*365")
    q2 = Q('associated_project = "TCGA-OV"')

    q = q1.AND(q2)
    a = q.to_dict()
    print(a)
    assert a["node_type"] == "AND"


test_and_op()
