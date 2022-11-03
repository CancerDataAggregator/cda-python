# CDA Python

This library sits on top of the machine generated
[CDA Python Client](https://github.com/CancerDataAggregator/cda-service-python-client) and offers some syntactic
sugar to make it more pleasant to query the CDA.

Documentation for CDA python is in our readthedocs repo and browsable at [https://cda.readthedocs.io/](https://cda.readthedocs.io/)

## Accessing Example Notebooks

Interactive versions of those notebooks can be used at this MyBinder link:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/CancerDataAggregator/readthedocs/HEAD?labpath=docs%2FExamples%2FWelcome.ipynb)

If you would like to bulk download the notebooks without the website, they are in [this folder](https://github.com/CancerDataAggregator/readthedocs/tree/main/docs/Examples)

# Contributing

If you have comments, questions, or feature requests for CDA python or the documentation site, please tell us at our [Discussions page](https://github.com/CancerDataAggregator/readthedocs/discussions)

If you have used CDA python in your work and want to be featured as a use case, start a conversation with us in the [Show and Tell](https://github.com/CancerDataAggregator/readthedocs/discussions/categories/show-and-tell)

If you have used CDA python and would like to contribute your own notebook for others to use, please make a pull request to our [Community Notebooks repo](https://github.com/CancerDataAggregator/Community-Notebooks)

## Swagger endpoints

You can access our swagger endpoints directly at https://cda.datacommons.cancer.gov/api/swagger-ui.html

# Installation Guide

There are two methods for local installation in virtual environments: Docker or Conda + pip.

Installation without a virtual environment may have unexpected/unresolvable
conflicts, and is not supported.

## Docker

### requirements

- git [(Install)](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- terminal/command line

1. [Download and install docker](https://www.docker.com/products/docker-desktop/)

2. Open Terminal or PowerShell and run:
```bash
git clone https://github.com/CancerDataAggregator/cda-python.git
```

3.  Navigate to the cda-python folder:
```bash
cd cda-python
```

4. Build the docker container:
```bash
docker-compose up --build
```

5. Open a Browser to [http://localhost:8888](http://localhost:8888).
This will open a docker container with all the required packages for using the API in ipython notebook.

### notes

- To stop the container from running, return to the terminal window (from step 2), and type **Control C to stop** the container.

### notes

To delete the container from your machine, use this command in the cda-python project directory.

```bash
docker compose down
```

## Conda + Pip install

### requirements

- terminal/command line
- python version >= 3.7 [(Install)](https://www.python.org/downloads/)
- conda [Install](https://docs.conda.io/en/latest/miniconda.html)

1. Open Terminal or PowerShell and create a new conda environment:

```bash
conda create -n cda python=3.7
```
  type `y` when prompted

2. Activate the environment:
  ```bash
  conda activate cda
  conda install jupyter
  pip install git+https://github.com/CancerDataAggregator/cda-python.git
  cd cda-python
  jupyter notebook
  ```
  type `y` when prompted

3. Click on the folder called `notebooks`, then the file called `example.ipynb` to
  open the example workflow, or create a new notebook to run your own.


### notes
You only need to create a new conda environment once!

- To exit the conda environment, return to the terminal window (from step 1), and type **Control C to stop** the notebook then:

```bash
conda deactivate
```
- To return to the notebook in conda, open a terminal and type:

```bash
conda activate cda
jupyter notebooks
```



## For Testers use this Binder

Click on the logo below. This will
launch a Jupyter Notebook instance with our example notebook ready to run.

[![MyBinder.org](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/CancerDataAggregator/cda-python/integration)
