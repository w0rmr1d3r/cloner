from pathlib import Path

from setuptools import find_packages, setup

from cloner import __version__

project_root_path = Path(__file__).parent

install_requires = [
    "click>=8.0.3",
    "requests>=2.27.1",
]

dev_requires = [
    "black>=22.3.0",
    "coverage>=6.3.2",
    "faker>=12.0.1",
    "flake8>=6.0.0",
    "isort>=5.10.0",
    "pip-tools~=6.5",
    "pytest>=6.2.5",
    "responses>=0.20.0",
]

classifiers = """\
Development Status :: 5 - Production/Stable
Environment :: Console
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.9
Programming Language :: Python :: 3.10
Programming Language :: Python :: 3.11
"""

# About Python versions. Supported 3.9 and above
# If supporting newer versions, update CI, coverage and classifiers
# If minimum version supported changes, update CI, coverage, classifiers, setup and release.

setup(
    name="wr-cloner",
    version=__version__.__version__,
    author="w0rmr1d3r",
    author_email="",
    description="A tool to clone efficiently all the repos in an organization",
    entry_points={"console_scripts": ["cloner=cloner.cli:cli"]},
    long_description=(project_root_path / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/w0rmr1d3r/cloner",
    project_urls={},
    classifiers=classifiers.splitlines(),
    packages=find_packages(exclude=("docs", "tests")),
    platforms="any",
    python_requires=">=3.9.0",
    install_requires=install_requires,
    tests_require=dev_requires,
    extras_require={"dev": dev_requires},
)
