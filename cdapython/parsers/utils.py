import os
from pathlib import Path


def read_lark(grammer_file: str, grammer_folder: str = "lark") -> str:
    _ROOT: Path = Path(__file__).parent
    GRAMMAR_PATH = os.path.join(_ROOT, grammer_folder, grammer_file)
    return GRAMMAR_PATH
