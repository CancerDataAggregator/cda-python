import json
from cdapython import Q


def test_json_check() -> None:
    json1 = Q(
        'ResearchSubject.primary_diagnosis_site = "uterus" OR ResearchSubject.primary_diagnosis_condition = "Uterine Corpus Endometrial Carcinoma"'
    ).researchsubject.count.to_json()

    Query1 = Q('ResearchSubject.primary_diagnosis_site = "uterus"')
    Query2 = Q(
        'ResearchSubject.primary_diagnosis_condition = "Uterine Corpus Endometrial Carcinoma"'
    )

    json2 = Query1.OR(Query2).researchsubject.count.to_json()

    assert json.loads(json1) == json.loads(json2)
