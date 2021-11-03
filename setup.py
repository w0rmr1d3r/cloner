from pathlib import Path

from setuptools import find_packages, setup

from cloner.__version__ import __version__

project_root_path = Path(__file__).parent

install_requires = [
    "click==8.0.3",
    "requests==2.26.0",
]

# todo
dev_requires = [
    "faker==9.7.1",
    "pytest==6.2.5",
    # "black==19.10b0",
    # "flake8>=3.3.0",
    # "isort==4.3.21",
    # "pytest-cov>=2.5.1",
    # "pip-tools>=5.3.1",
    # "moto==1.3.13",
]

# todo
docs_requires = [
#     "ansi2html==1.5.2",
#     "Markdown==3.2.2",
#     "markdown-include==0.5.1",
#     "mkdocs-exclude==1.0.2",
#     "mkdocs-macros-plugin==0.4.9",
#     "mkdocs-material==5.5.12",
#     "mkdocs-material-extensions==1.0",
#     "mkdocs-minify-plugin==0.3.0",
#     "mkdocs==1.1.2",
#     "pygments==2.5.2",
]

# todo review this and requirements
# todo setuptools + package?
setup(
    name="cloner",
    version=__version__,
    author="w0rmr1d3r",
    author_email="",
    entry_points={"console_scripts": ["cloner=cloner.cli:cli"]},
    long_description=(project_root_path / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/w0rmr1d3r/cloner",
    description="",  # todo
    packages=find_packages(exclude=("docs", "tests")),
    platforms="any",
    python_requires=">=3.9",
    install_requires=install_requires,
    tests_require=dev_requires,
    extras_require={"dev": dev_requires, "docs": docs_requires},
)
