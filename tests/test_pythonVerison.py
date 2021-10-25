from cdapython import __version__
import os
from pathlib import Path


def getVersion(filepath: str):
    with open(filepath, "r") as f:
        for i in f.readlines():
            if i.find("VERSION") != -1:
                return str(i.split("=")[1].strip().replace('"', ""))
version = getVersion("./cdapython/constantVariables.py")
Path.absolute(str(Path("./cdapython/constantVariables.py").resolve()))


def test_pyVERSION() -> None:
    assert __version__ == version
