from cdapython import Q
from tests.global_settings import host


def test_call_api():
    q = Q('id = "TCGA-E2-A10A"')
    r = q.run(verify=False, host=host)
    assert isinstance(r.sql, str) is True
    print(r)


test_call_api()
