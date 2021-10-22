from pathlib import Path
import os
from typing import Optional

from dotenv import load_dotenv

env_path = Path(".") / ".env"
if env_path.exists() is True:
    load_dotenv(dotenv_path=env_path)
else:
    from os.path import join, dirname

    dotenv_path = join(dirname(__file__), ".env")
    load_dotenv(dotenv_path)


__version__: Optional[str] = os.getenv("VERSION")
CDA_API_URL: Optional[str] = os.getenv("CDA_API_URL")
table_version: Optional[str] = os.getenv("DATABASETABLE_VERSION")
default_table: Optional[str] = os.getenv("DATABASETABLE")
project_name: Optional[str] = default_table.split(".")[0]
