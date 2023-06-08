from cdapython import Q


def test_select():
    a = Q("sex = 'male' AND NOT vital_status = 'Dead'  ").SELECT("vital_status,sex")
    print(a.to_json())
    print(a.run(show_sql=True))
