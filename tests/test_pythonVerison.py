from cdapython import __version__


version = "2021.1.22"


def test_python_version() -> None:
    assert __version__ == version
