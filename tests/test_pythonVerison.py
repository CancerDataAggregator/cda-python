from cdapython import __version__
from os.path import abspath


version = "2021.10.25"



def test_pyVERSION() -> None:
    assert __version__ == version
