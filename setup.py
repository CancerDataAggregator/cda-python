import pathlib
from datetime import datetime
from setuptools import setup, find_packages

from cdapython import __version__

current_path = pathlib.Path(__file__).parent

name = "cdapython"
version = __version__
now = datetime.utcnow()
desc_path = pathlib.Path(current_path, "README.md")
long_description = desc_path.open("r").read()

setup(
    name=name,
    version=version,
    packages=find_packages(),
    platforms=['POSIX', 'MacOS', 'Windows'],
    python_requires='>=3.6',
    install_requires=[
        "cda-client@git+https://github.com/CancerDataAggregator/cda-service-python-client.git",
    ],
    description='User friendly Python library to access CDA service.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
)