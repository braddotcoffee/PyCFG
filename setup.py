from setuptools import setup

setup(
    name="PyCFG",
    version="1.0.0",
    url="https://github.com/bwbonanno/PyCFG",
    license="MIT License",
    author="Bradford Bonanno",
    description=(
        "Library for building and interacting with Python\
                 control-flow graphs"
    ),
    packages=["src"],
    test_suites="tests",
)
