from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

__version__ = os.getenv("VERSION")
CDA_API_URL = os.getenv("CDA_API_URL")
table_version = os.getenv("DATABASETABLE")