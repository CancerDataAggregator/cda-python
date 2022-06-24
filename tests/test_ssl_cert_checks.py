from cdapython import Q, columns
from tests.global_settings import host


def test_ssl_q():
    q = Q('id = "TCGA-13-1409"')
    r = q.run(verify=False, host=host)
    assert r.count == 1


columns(verify=False, host=host)
