from cdapython import __version__


version = "2021.11.19"


def test_pyVERSION() -> None:
    assert __version__ == version
