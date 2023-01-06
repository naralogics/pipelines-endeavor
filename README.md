# Pipelines

This template project shows how to use Nara Logics Pipelines for rapid, step-by-step data orchestration and connectome
construction.

## Overview

## Prerequisites
* Python 3.10
* A virtual environment (Virtualenv, etc.)

## Setup
The steps below walk you through an initial setup and a clean Python environment.
We use [`Pipenv`](https://realpython.com/pipenv-guide/) to manage our project environment
and [`pre-commit`](https://pre-commit.com) to run CI actions both locally and in PR checks.

1. Install Python 3.10 - https://www.python.org/downloads/

2. Install Virtualenv - https://pypi.org/project/virtualenv/

3. Make sure your virtual environment is running - `which python`

4. Install pipenv
```bash
pip install pipenv
```

5. Install dependencies
```bash
pipenv sync --dev
```
This will set up a new virtual environment based on your current global Python and the project
Pipenv's required Python version, and install the resolved dependencies of the project in that
virtual environment.

### Ensuring local environment remains in-sync with project requirements added by others

You can just use the same command as above, `pipenv sync --dev`, to ensure your local environment contains
all your required dependencies.

### Updating project dependencies

You use `pipenv` to change versions of existing dependencies or add new ones:

- To change dependencies, the most robust way today is two separate steps, first resolving
  dependencies, and second, syncing your virtual environment so that it contains your new and updated
  packages:

    ```bash
    pipenv lock --dev && pipenv sync --dev
    ```

- To add a new dependency such as `requests`, you can run `pipenv install requests`. This will
  add `requests` package as a new dependency to your `Pipfile`, update your lock file, and install
  the package and all of its required dependencies in your projects virtual environment.

## Using your project

### Running your pipelines

Running a pipeline from the web interface:
```bash
cd pipelines

dagit -f cereal_example/catalog.py
```

To run the cereal_example pipeline present in this project, run:

```bash
dagit -f pipelines/cereal_example/catalog.py
```

This will bring up a local web dashboard you can use to explore, run and debug your
pipelines. Click on the link: http://127.0.0.1:3000/

### Updating your code and making PR's

After making a set of changes to your code, you can run the same CI actions Github runs as part of
PR checks in your local environment:

```bash
pipenv run check-all -a
```

This command will run all the unit tests, formatting, quick linting and fixes set up for your project.

We define these commands as scripts in `Pipfile` and make use of `pre-commit` to run actions.
You can use any arguments that `pre-commit run` command will accept to customize them.

## Updates: 07/2022

* The pipelines nodes_pipeline and properties_pipeline (referred to in documentation elsewhere) have been renamed to connectome_1_nodes and connectome_2_properties in an attempt to show that they're the two pipelines to run in order to build the connectome and in what order. Be aware that other documentation about this project located elsewhere may be out of date in places.

* If you have a newer Mac and have trouble instaling Pythoon 3.10, see this document Lucas wrote: https://narame.atlassian.net/wiki/spaces/TECH/pages/3224174593/ARM+Mac+x86+Architecture+Setup+M1+M2+Chips
