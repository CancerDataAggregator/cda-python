# noxfile.py


import tempfile
import nox

locations = ["cdapython"]
python_versions = ["3.8", "3.9", "3.10", "3.7"]


@nox.session()
def pip_install(session):
    session.install("-r", "requirements.txt")
    session.install("-r", "requirements-dev.txt")


@nox.session(python="3.7")
def typecheck(session):
    session.install("-r", "requirements.txt")
    session.install("pytype")
    session.run("pytype", "cdapython")


@nox.session(python=python_versions)
def pip_update(session):
    session.install("pip-tools")
    session.run("pip-compile", "-r", "requirements-dev.in")
    session.run("pip-compile", "-r", "requirements.in")


@nox.session(python=python_versions)
def tests(session):
    session.install("-r", "requirements.txt")
    session.install("-r", "requirements-dev.txt")
    session.install("pytest")
    args = session.posargs or ["."]
    session.run("pytest", *args)


@nox.session(python=python_versions)
def lint(session):
    args = session.posargs or locations
    session.install(
        "flake8",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-import-order",
    )
    session.run("flake8", *args)


@nox.session(python=python_versions)
def black(session):
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@nox.session(python=python_versions)
def safety(session):
    with tempfile.NamedTemporaryFile() as requirements:
        session.install("safety")
        # session.run("safety", "check", f"--file=requirements.txt", "--full-report")
        session.run("safety", "check", f"--file=requirements-dev.txt", "--full-report")
