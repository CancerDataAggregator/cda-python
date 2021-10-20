from cdapython import Q


def test_call_api():
    q = Q('id = "TCGA-E2-A10A"')
    r = q.run()
    assert isinstance(r.sql, str) is True
