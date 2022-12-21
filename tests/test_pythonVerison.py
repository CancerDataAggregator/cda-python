from cdapython import Q

version = "2022.12.21"


def test_python_version() -> None:
    assert Q.get_version() == version
