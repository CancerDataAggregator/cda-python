from datetime import datetime
from pathlib import Path

from setuptools import find_packages, setup


def get_version(filepath: str):
    print("ran setup.py get_version")
    version = None
    version_client = None
    with open(filepath, "r") as f:
        for i in f.readlines():
            if i.startswith("version = "):
                version = str(i.split("=")[1].strip().replace('"', ""))
            if i.startswith("CLIENT_VERSION"):
                version_client = str(i.split("=")[1].strip().replace('"', ""))
    return (version, version_client)


_version, version_client = get_version("pyproject.toml")


with open("pyproject.toml") as f:
    contents = f.read()

# Extract dependencies section
start = contents.find("[tool.poetry.dependencies]") + len("[tool.poetry.dependencies]")
end = contents.find("\n\n", start)
dependencies = contents[start:end].strip()

# Split dependencies into a list
dependency_list = [dep.strip() for dep in dependencies.split("\n") if dep.strip()]

setup_list = []
for i in dependency_list[1:]:
    if i.find("git") != -1:
        dep, _, url, number = i.split("=")
        url = url.replace('"', "").replace(",", "").replace("rev", "").strip()
        dep = dep.strip()
        number = number.strip().replace('"', "").replace("}", "")
        git_url = f"{dep}@git+{url}@{number}"
        setup_list.append(git_url)
    else:
        i = i.replace("=", "==").replace('"', "").replace("^", "")
        i = f"{i}"
        print(i)
        setup_list.append(i)


current_path = Path(__file__).parent

NAME = "cdapython"
VERSION: str = _version
now = datetime.utcnow()
desc_path = Path(current_path, "README.md")
with open(desc_path, "r", encoding="utf-8", errors="surrogateescape") as fh:
    long_description = fh.read()


setup(
    name=NAME,
    packages=find_packages(
        where=".", exclude=("tests",)
    ),  # add __init__.py in folders you want to be bundled in build
    classifiers=[
        "cdapython",
        "CancerDataAggregator",
        "CancerDataAggregator python",
    ],
    include_package_data=True,
    package_data={"cdapython": ["py.typed"], "": [".env", "*.lark"]},
    package_dir={"cdapython": "cdapython"},
    version=VERSION,
    py_modules=["cdapython"],
    platforms=["POSIX", "MacOS", "Windows"],
    python_requires=">=3.8",
    url="https://github.com/CancerDataAggregator/cdapython",
    install_requires=setup_list,
    description="User friendly Python library to access CDA service.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": ["cdapython_Q = cdapython.__main__:main"],
    },
)
