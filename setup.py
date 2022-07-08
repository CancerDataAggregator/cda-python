from datetime import datetime
from pathlib import Path

from setuptools import find_packages, setup


def get_version(filepath: str):
    version = None
    version_client = None
    with open(filepath, "r") as f:
        for i in f.readlines():
            if i.startswith("VERSION:"):
                version = str(i.split("=")[1].strip().replace('"', ""))
            if i.startswith("CLIENT_VERSION"):
                version_client = str(i.split("=")[1].strip().replace('"', ""))
    return (version, version_client)


__version__, version_client = get_version("cdapython/constant_variables.py")
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
    packages=find_packages(exclude=("tests",)),
    classifiers=[
        "cdapython",
        "CancerDataAggregator",
        "CancerDataAggregator python",
    ],
    include_package_data=True,
    package_data={"cdapython": ["py.typed"], "": [".env", "cdapython/config.ini"]},
    package_dir={"cdapython": "cdapython"},
    version=VERSION,
    py_modules=["cdapython"],
    platforms=["POSIX", "MacOS", "Windows"],
    python_requires=">=3.6",
    url="https://github.com/CancerDataAggregator/cdapython",
    install_requires=[
        "tdparser>=1.1.6",
        "numpy>=1.21.5",
        "wheel>=0.36.2",
        "urllib3>=1.26.8",
        "rich>=12.0.1",
        "matplotlib>=3.5.1",
        "typing-extensions==4.2.0",
        "pandas==1.3.5",
        "ipywidgets>=7.7.0",
        "cda-client@git+https://github.com/CancerDataAggregator/cda-service-python-client.git@3.0.0",
        "python-dotenv>=0.18.0",
        "ipython>=7.32.0",
    ],
    description="User friendly Python library to access CDA service.",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
