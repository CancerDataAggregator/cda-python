import sys


def Q_import_path_str(method: str = "run") -> str:
    """
    This function is a patch for python 3.11. The `mock.patch` importing system changed
    this will cause a error if the path is not a absolute path to the module.
    This will support both 3.11 and older python versions.
    Args:
        method (str, optional): _description_. Defaults to "run".
    Returns:
        str: returns module path
    """
    if (sys.version_info.major, sys.version_info.minor) == (3, 11):
        return f"cdapython.Q.Q.{method}"
    return f"cdapython.Q.{method}"
