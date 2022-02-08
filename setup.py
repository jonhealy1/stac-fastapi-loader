"""stac-check setup.py
"""
from setuptools import setup, find_packages

__version__ = "0.1.0"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="stac_fastapi_loader",
    version=__version__,
    description="Tool to load STAC assets into stac-fastapi",
    url="https://github.com/jonhealy1/stac-check",
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=[
        "pystac[validation]==1.1.0",
        "click>=7.1.2",
        "requests>=2.19.1",
        "jsonschema>=3.1.2b0",
        "pytest"
    ],
    entry_points={
        'console_scripts': ['stac_fastapi_loader=stac_fastapi_loader.cli_loader:main']
    },
    author="Jonathan Healy",
    author_email="jonathan.d.healy@gmail.com",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    tests_require=["pytest"]
)