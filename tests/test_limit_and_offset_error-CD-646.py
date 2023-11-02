from cdapython import Q


def test_limit_and_offset():
    df = Q('primary_diagnosis_site = "uterus"').LIMIT(20).OFFSET(100).run().to_list()
    df_2 = Q('primary_diagnosis_site = "uterus"').LIMIT(20).OFFSET(0).run().to_list()
    assert len(df) == 20
    assert df != df_2


def test_limit_with_no_offset():
    df = Q('primary_diagnosis_site = "uterus"').LIMIT(20).OFFSET(100).run().to_list()
    df_2 = Q('primary_diagnosis_site = "uterus"').LIMIT(20).run().to_list()
    assert len(df) == 20
    assert df != df_2
