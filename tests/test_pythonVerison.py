
from cdapython import __version__
import os 
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

def test_pyVERSION():
    assert __version__ == os.getenv("VERSION")