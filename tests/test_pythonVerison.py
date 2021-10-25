from cdapython import __version__
import os
from pathlib import Path


version = "2021.10.22"


def test_pyVERSION() -> None:
    assert __version__ == version
