from cdapython import Q


def test1():
    assert Q.statusbigquery() == "everything is fine"
