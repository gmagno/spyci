from setuptools import setup, find_packages

version = "0.2.0"


# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# Get requirements from requirements.txt file
with open(path.join(here, "requirements.txt")) as f:
    requirements = f.read().replace("==", ">=").splitlines()

# Get requirements from requirements-dev.txt file
with open(path.join(here, "requirements-dev.txt")) as f:
    requirements_dev = f.read().replace("==", ">=").splitlines()

setup(
    name="spr",
    version=version,
    description="A tiny Python package to parse spice raw data files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/goncalo-godwitlabs/spr",
    author="goncalo-godwitlabs",
    author_email="goncalo@godwitlabs.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
        "Programming Language :: Python :: 2.7",
    ],
    keywords="spice matplotlib rawspice raw",
    packages=find_packages(
        exclude=[
            "examples",
            "tests"
        ]),
    install_requires=requirements,
    extras_require={
        "dev": requirements_dev,
    },
    data_files=[(
        '.', [
            "requirements.txt",
            "requirements-dev.txt",
        ]
    )],
    project_urls={
        "Bug Reports": "https://github.com/goncalo-godwitlabs/spr/issues",
        "Source": "https://github.com/goncalo-godwitlabs/spr",
    },
)
