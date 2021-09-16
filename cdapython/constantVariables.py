from pathlib import Path
import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

__version__: Optional[str] = os.getenv("VERSION")
CDA_API_URL: Optional[str] = os.getenv("CDA_API_URL")
table_version: Optional[str] = os.getenv("DATABASETABLE_VERSION")
default_table: Optional[str] = os.getenv("DATABASETABLE")
