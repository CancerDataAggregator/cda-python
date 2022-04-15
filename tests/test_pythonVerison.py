from cdapython import __version__


version = "2022.4.13"


def test_python_version() -> None:
    assert __version__ == version
