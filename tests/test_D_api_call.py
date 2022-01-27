from cdapython import Q
from time import sleep


def test_call_api():
    # sleep(1)
    q = Q('id = "TCGA-E2-A10A"')
    r = q.run(verify=False)
    print(r)
    assert isinstance(r.sql, str) is True
