from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

__version__ = os.getenv("VERSION")
CDA_API_URL = "https://cda.cda-dev.broadinstitute.org"
table_version = os.getenv("DATABASETABLE")