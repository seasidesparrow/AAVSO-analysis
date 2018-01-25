from setuptools import setup

setup(
    name = "aavso",
    version = "2.0",
    author = "Matthew Templeton",
    description = ("A set of data manipulation tools useful for analyzing photometry from the AAVSO International Database."),
    keywords = "aavso photometry variable star",
    url = "https://github.com/seasidesparrow/AAVSO-analysis",
    install_requires = ['numpy', 'pandas', 'matplotlib'],
)
