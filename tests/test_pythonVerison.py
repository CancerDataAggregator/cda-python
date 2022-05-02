from cdapython import __version__


version = "2022.5.2"


def test_python_version() -> None:
    assert __version__ == version
