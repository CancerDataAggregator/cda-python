from cdapython import Q


def test_glb_count() -> None:
    r = Q.global_counts(host="http://localhost:8080")
    print(r)


test_glb_count()