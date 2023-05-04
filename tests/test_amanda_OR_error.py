import json

from cdapython import Q


def test_json_check() -> None:
    json1 = Q(
        'primary_diagnosis_site = "uterus" OR primary_diagnosis_condition = "Uterine Corpus Endometrial Carcinoma"'
    ).researchsubject.count.to_json()
    assert json.loads(json1)["node_type"] == "OR"

    Query1 = Q('primary_diagnosis_site = "uterus"')
    Query2 = Q('primary_diagnosis_condition = "Uterine Corpus Endometrial Carcinoma"')

    json2 = Query1.OR(Query2).researchsubject.count.to_json()

    assert json.loads(json1) == json.loads(json2)
