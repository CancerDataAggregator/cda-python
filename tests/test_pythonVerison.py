from cdapython import __version__

version = "2022.6.22"


Q("sex = 'male'").Is("sex = 'female'")


def test_python_version() -> None:
    assert __version__ == version
