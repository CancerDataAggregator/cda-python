from cdapython import Q

version = "2023.9.12"


def test_python_version() -> None:
    assert Q.get_version() == version
