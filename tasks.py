import time

from invoke import task
from rich import print
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class Handler(FileSystemEventHandler):
    def __init__(self):
        print("ran tasks.py Handler __init__")
        self.event_type = None
        self.src_path = None

    def on_any_event(self, event):
        # if event.is_directory:
        #     return None
        print("ran tasks.py Handler on_any_event")
        if event.src_path.find("__pycache__") == -1:
            self.event_type = event.event_type
            self.src_path = event.src_path
            print(f"{time.asctime()} noticed: {event.event_type} on: {event.src_path}")


@task
def black_w(c, args):
    """
    This will run black in a watching state
    Args:
        c (_type_): _description_
    """
    print("ran tasks.py black_w")
    print("[bold yellow] Black is watching files [/bold yellow]")
    if args == "lint":
        print(" [bold yellow]pylint is watching[/bold yellow]")
    path = "cdapython"
    file_event_handler = Handler()
    observer = Observer()
    observer.schedule(file_event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            try:
                time.sleep(10)
                if file_event_handler.event_type == "created":
                    continue
                if file_event_handler.event_type == "modified":
                    c.run(f"black {file_event_handler.src_path}")
                    if args == "lint":
                        c.run(f"pylint {file_event_handler.src_path}")
            except Exception as e:
                print(e)

    except KeyboardInterrupt:
        observer.stop()
    observer.join()


@task
def venv(c):
    """
    This will create a venv for you
    Args:
        c (_type_): _description_
    """
    print("ran tasks.py venv")
    print("Create venv ")
    c.run("python3 -m venv venv && source venv/bin/activate")


@task
def formatting(c) -> None:
    print("ran tasks.py formatting")
    """
    This will run black formatting for you
    Args:
        c (_type_): _description_
    """
    print("Formatting!")
    c.run("black .")


@task
def mypy(c, args=None) -> None:
    """
    This will run mypy to check the types in the cdapython
    Args:
        c (_type_): _description_
    """
    print("ran tasks.py mypy")
    print("Checking Types")
    if args is None:
        c.run("mypy cdapython")
    else:
        c.run(f"mypy {args}")


@task
def tests(c, args=None) -> None:
    """
    This will run pytest
    Args:
        c (_type_): _description_
    """
    print("ran tasks.py tests")
    print("Run pytest")
    if args is None:
        c.run("pytest .")
    else:
        c.run(f"pytest {args}")


@task
def lint(c, args=None) -> None:
    """
    This will run pylint
    Args:
        c (_type_): _description_
        args (_type_): _description_
    """
    print("ran tasks.py lint")
    print(f"linting {args}")
    if args is None:
        c.run("pylint")
    else:
        c.run(f"pylint {args}")
    c.run(f"pylint {args}")


@task
def uninstall(c, args=None) -> None:
    print("ran tasks.py uninstall")
    print("uninstall and reinstall")
    c.run("pip uninstall cdapython -y  && pip install -e .")
