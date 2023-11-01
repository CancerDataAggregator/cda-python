from cdapython import Q


def test_limit_and_offset():
    df = (
        Q('primary_diagnosis_site = "uterus"')
        .LIMIT(20)
        .OFFSET(100)
        .run()
        .to_dataframe()
    )
    print(df)
    assert len(df) == 20
