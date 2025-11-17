from setuptools import setup, find_packages

# Read requirments
with open("./requirements.txt") as file:
    # Read lines as a list
    packages = file.read().splitlines()

setup(
    name="census-mapping",
    version="0.1",
    packages=find_packages(include=["census", "nomis_census.py"]),
    install_requires=packages
)
