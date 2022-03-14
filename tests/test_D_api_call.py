from cdapython import Q
from memory_profiler import profile


@profile
def test_call_api():
    # sleep(1)
    q = Q('id = "TCGA-E2-A10A"')
    r = q.run(verify=False)
    r.pretty_print()
    assert isinstance(r.sql, str) is True


test_call_api()
