from cdapython import __version__


version = "2021.12.29"


def test_python_version() -> None:
    assert __version__ == version
