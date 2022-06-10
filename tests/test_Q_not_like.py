from cdapython import Q
from tests.global_settings import host


def test_not_like() -> None:
    Q('sex NOT LIKE "m%"').subject.count.run(host=host)


test_not_like()
