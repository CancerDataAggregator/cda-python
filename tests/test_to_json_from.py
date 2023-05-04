from cdapython import Q


def test_check_from_to_json() -> None:
    """_summary_
    This test checks Q to json function it is looking for a SUBQUERY value because From is just alias for SUBQUERY
    """

    q1 = Q('primary_diagnosis_condition = "Ovarian Serous Cystadenocarcinoma"')
    q2 = Q('system = "PDC"')
    q3 = Q('system = "GDC"')

    q = q3.FROM(q1.AND(q2))

    assert q.to_json().find("SUBQUERY") != -1
