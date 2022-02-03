from cdapython import Q, query


def test_glb_count() -> None:
    r = query('sex = "male" OR sex = "female"')
    q1 = r.counts(host="http://localhost:8080", limit=100)
    print(q1)


test_glb_count()
