from cdapython import Q

version = "2023.1.9"


def test_python_version() -> None:
    assert Q.get_version() == version
