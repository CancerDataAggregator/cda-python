from invoke import task


@task
def formatting(c) -> None:
    """
    This will run black formatting for you
    Args:
        c (_type_): _description_
    """
    print("Formatting!")
    c.run("black .")


@task
def mypy(c) -> None:
    """
    This will run mypy to check the types in the cdapython
    Args:
        c (_type_): _description_
    """
    print("Checking Types")
    c.run("mypy cdapython")


@task
def tests(c, args) -> None:
    """
    This will run pytest
    Args:
        c (_type_): _description_
    """
    print("Run pytest")
    if args is None:
        c.run("pytest .")
    else:
        c.run(f"pytest {args}")


@task
def lint(c, args) -> None:
    """_summary_
    This will run pylint
    Args:
        c (_type_): _description_
        args (_type_): _description_
    """
    print(args)
    if args is None:
        c.run("pylint")
    else:
        c.run(f"pylint {args}")
    c.run(f"pylint {args}")
