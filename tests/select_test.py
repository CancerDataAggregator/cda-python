from cdapython import Q
from tests.global_settings import host, project


def test_select():
    a = Q("sex = 'male' AND NOT vital_status = 'Dead'  ").mutation.SELECT(
        "vital_status,sex"
    )
    print(a.to_json())
    # print(a.run(show_sql=True))


test_select()
