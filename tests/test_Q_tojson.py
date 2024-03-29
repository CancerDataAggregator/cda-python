from cdapython import Q


def test_to_json_check() -> None:
    sex = Q('sex = "female"')
    cancer = Q('primary_diagnosis_condition = "Breast Invasive Carcinoma"')
    ageL = Q("days_to_birth <= -30*365")
    ageU = Q("days_to_birth >= -45*365")

    q1 = sex.AND(cancer.AND(ageL.AND(ageU)))

    assert q1.to_json().find("AND") != -1
