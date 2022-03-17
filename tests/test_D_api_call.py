from cdapython import Q
from memory_profiler import profile
from tests.global_settings import host


@profile
def test_call_api():
    # sleep(1)
    q = Q('id = "TCGA-E2-A10A"')
    r = q.run(verify=False, host=host)
    # assert isinstance(r.sql, str) is True
    print(r)


test_call_api()
