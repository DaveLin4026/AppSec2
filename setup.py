import setuptools
# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
#https://pythonhosted.org/an_example_pypi_project/setuptools.html

setuptools.setup(
    name="AppSec2",
    version="0.0.1",
    author="David Linares",
    author_email = "dl4026@nyu.edu",
    description = ("CS-GY9163: Application Security",
    packages=setuptools.find_packages(),
)
