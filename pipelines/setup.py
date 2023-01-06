"""Pipeline example ‒ A template Python module using Pearl for data pipelines.
"""

from os import path

from setuptools import find_packages, setup

REQUIRES = [
    "dagster",
    "pearl",
    "pandas",
]

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, "README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="nara-example",
    version="0.1.0",
    description="A template for a collection of data pipelines based on Pearl",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/naralogics/pipeline-example",
    author="Nara Logics",
    author_email="tech@naralogics.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
    ],
    packages=find_packages(exclude=["cereal_example_tests"]),
    install_requires=REQUIRES,
)
