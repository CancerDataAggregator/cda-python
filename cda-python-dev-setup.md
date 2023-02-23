# Dev Setup Guide
Welcome to the CDA Project!

This is a guide to getting your development environment set up to contribute to the project. 
 
---
# Download Python 3

Check the python version used in pyproject.toml under [tool.poetry.dependencies] and download a version in that range. 

[Download python](https://www.python.org/downloads/)

You can also download using homebrew for mac users
```bash
    brew install python
```
---
# Download a IDE/Text Editor
- We use vscode here is a link to download it [Download vscode](https://code.visualstudio.com/Download)  

- Here is the extension we used (note) please read the extension setups for black and isort.
    
    - [black](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)
    - [python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) 
    - [isort](https://marketplace.visualstudio.com/items?itemName=ms-python.isort)
    - [autoDocstring](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring)
    
    - [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)
    - [gitlens](https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens)

if you don't want to use the black extension you can use the helper script. 

first you need to create a venv in python for Mac and Linux
```bash
    python3 -m venv venv && source venv/bin/activate
```
for windows 
```powershell
    python -m venv venv 
    
    venv\Scripts\activate
```

then you will need to install poetry you can follow this link [install poetry](https://python-poetry.org/docs/#installing-with-pipx)

--- 
# Poetry Commands

### how to install in venv
- `poetry install` : Will install dependencies inside of pyproject.toml inside of the activated `venv`

### how to add packages 
- `poetry add <package>` : This will add dependency to `venv` and update pyproject.toml this will check dependency with the python version

### how to export requirements.txt
- `poetry export --without-hashes  -f requirements.txt --output requirements.txt
` : This will write out the all the dependencies that are in the pyproject.tom in the tool.poetry.dependencies this command is here for a backwards compatibility.

### how to add git dependencies
- `poetry add git+https://github.com/CancerDataAggregator/cda-service-python-client.git#3.3.0` : This is how to add github dependencies to the project

---
# Tools

In your terminal you should be able to use 

`black` Code formatter 

`mypy` Type checking 

`pylint` This will lint the code

`isort` This will sort python imports.

`bandit` checks code for CVES.

`safety` checks install dependencies.

`pytest` A test runner 

---
# Helper Commands
(Note use these commands in a venv)
 - `invoke black-w` : This will run black in a watching state
 - `invoke formatting`  This will run black formatting for you.
 - `invoke lint` This will run pylint
 - ` invoke mypy` This will run mypy to check the types in the cdapython
 - `invoke tests` This will run pytest
 `invoke venv` This will create a venv for you

Thanks for joining the team if you have any questions ask them in the cda stack no question is a dumb question.