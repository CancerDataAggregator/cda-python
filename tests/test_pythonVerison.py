from cdapython import __version__


version = "2021.11.4"


def test_pyVERSION() -> None:
    assert __version__ == version
