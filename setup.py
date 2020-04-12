# First Party
from setuptools import setup

setup(
    name="minislite",
    version="0.99",
    packages=["minislite"],
    url="https://github.com/ahmetkotan/minislite",
    license="",
    author="ahmetkotan",
    author_email="ahmtkotan@gmail.com",
    description="Mini and Secure SQLite ORM",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: SQL",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Database",
        "Topic :: Database :: Database Engines/Servers",
    ],
)
