from cdapython import __version__


version = "2021.10.25"


def test_pyVERSION() -> None:
    assert __version__ == version
