import os
from pathlib import Path


def read_lark(grammer_file: str, grammer_folder: str = "lark") -> str:
    print("ran parsers/utils.py read_lark")
    _ROOT: Path = Path(__file__).parent
    GRAMMAR_PATH = os.path.join(_ROOT, grammer_folder, grammer_file)
    return GRAMMAR_PATH
