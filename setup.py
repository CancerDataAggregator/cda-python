from datetime import datetime
from setuptools import setup, find_packages
from pathlib import Path


def get_version(filepath: str):
    with open(filepath, "r") as f:
        for i in f.readlines():
            if i.find("VERSION") != -1:
                return str(i.split("=")[1].strip().replace('"', ""))


__version__ = get_version("cdapython/constantVariables.py")
print(__version__)
current_path = Path(__file__).parent

NAME = "cdapython"
VERSION: str = __version__
now = datetime.utcnow()
desc_path = Path(current_path, "README.md")
with open(desc_path, "r", encoding="utf-8", errors="surrogateescape") as fh:
    long_description = fh.read()

setup(
    name=NAME,
    packages=find_packages(),
    include_package_data=True,
    package_data={"cdapython": ["py.typed"], "": [".env"]},
    package_dir={"cdapython": "cdapython"},
    version=VERSION,
    py_modules=["cdapython"],
    platforms=["POSIX", "MacOS", "Windows"],
    python_requires=">=3.6",
    install_requires=[
        "tdparser",
        "numpy",
        "wheel",
        "urllib3",
        "pandas",
        "unsync",
        "cda-client@git+https://github.com/CancerDataAggregator/cda-service-python-client.git",
        "python-dotenv",
    ],
    description="User friendly Python library to access CDA service.",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
