from cdapython import __version__


version = "2022.3.17"


def test_python_version() -> None:
    assert __version__ == version
