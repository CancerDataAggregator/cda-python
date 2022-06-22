from cdapython import __version__

version = "2022.7.9"


def test_python_version() -> None:
    assert __version__ == version
