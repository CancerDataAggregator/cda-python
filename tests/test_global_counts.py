from cdapython import Q, query
from tests.global_settings import host


def test_glb_count() -> None:
    r = query('sex = "male" OR sex = "female"')
    q1 = r.count.run(host=host, limit=100)
    print(q1)


test_glb_count()
