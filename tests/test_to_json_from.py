from cdapython import Q


def test_check_from_to_json() -> None:
    """_summary_
    This test checks Q to json function it is looking for a SUBQUERY value because From is just alias for SUBQUERY
    """

    q1 = Q(
        'ResearchSubject.primary_diagnosis_condition = "Ovarian Serous Cystadenocarcinoma"'
    )
    q2 = Q('ResearchSubject.identifier.system = "PDC"')
    q3 = Q('ResearchSubject.identifier.system = "GDC"')

    q = q3.From(q1.And(q2))

    assert q.to_json().find("SUBQUERY") != -1
