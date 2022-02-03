from cdapython import Q, query


def test_glb_count() -> None:
    r = query('sex = "male" OR sex = "female"')
    q1 = r.counts(host="http://35.192.60.10:8080/", limit=100)
    q1.pretty_print()
