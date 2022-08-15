import json
from cdapython import Q
import pytest


@pytest.mark.parametrize(
    "values",
    [
        'ResearchSubject.primary_diagnosis_site = "uterus" OR ResearchSubject.primary_diagnosis_condition = "Uterine Corpus Endometrial Carcinoma"',
    ],
)
def test_json_check(values) -> None:
    json1 = Q(values).researchsubject.count.to_json()
    assert json.loads(json1)["node_type"] == "OR"

    Query1 = Q('ResearchSubject.primary_diagnosis_site = "uterus"')
    Query2 = Q(
        'ResearchSubject.primary_diagnosis_condition = "Uterine Corpus Endometrial Carcinoma"'
    )

    json2 = Query1.OR(Query2).researchsubject.count.to_json()

    assert json.loads(json1) == json.loads(json2)
