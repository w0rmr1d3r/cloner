from pathlib import Path

from setuptools import find_packages, setup

from cloner import __version__

project_root_path = Path(__file__).parent

install_requires = [
    "click==8.0.3",
    "requests==2.26.0",
]

dev_requires = [
    "black==22.1.0",
    "faker==12.0.1",
    "flake8==4.0.1",
    "isort==5.10.0",
    "pip-tools==5.3.1",
    "pytest==6.2.5",
    "responses==0.18.0",
]

setup(
    name="cloner",
    version=__version__.__version__,
    author="w0rmr1d3r",
    author_email="",
    entry_points={"console_scripts": ["cloner=cloner.cli:cli"]},
    long_description=(project_root_path / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/w0rmr1d3r/cloner",
    description="A tool to clone efficiently all the repos in an organization",
    packages=find_packages(exclude="tests"),
    platforms="any",
    python_requires=">=3.10.0",
    install_requires=install_requires,
    tests_require=dev_requires,
    extras_require={"dev": dev_requires},
)
