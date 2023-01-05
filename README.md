# cloner

A tool to clone efficiently all the repos in an organization

[![PyPI](https://img.shields.io/pypi/v/wr-cloner)](https://pypi.org/project/wr-cloner/)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/w0rmr1d3r/cloner)](https://github.com/w0rmr1d3r/cloner/releases)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wr-cloner)
![GitHub last commit](https://img.shields.io/github/last-commit/w0rmr1d3r/cloner)

[![CI](https://github.com/w0rmr1d3r/cloner/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/w0rmr1d3r/cloner/actions/workflows/ci.yml)
[![Known Vulnerabilities](https://snyk.io/test/github/w0rmr1d3r/cloner/badge.svg)](https://snyk.io/test/github/w0rmr1d3r/cloner)
[![Treeware (Trees)](https://img.shields.io/treeware/trees/w0rmr1d3r/cloner)](https://plant.treeware.earth/w0rmr1d3r/cloner)
[![PyPi downloads](https://img.shields.io/pypi/dm/wr-cloner?label=PyPi%20downloads)](https://pypistats.org/packages/wr-cloner)

## Install

```bash
pip install wr-cloner
```

_Yes, it's called **wr-cloner** in PyPi, since **cloner** was already taken :sad:_

## Usage

```text
Usage: cloner [OPTIONS] GITHUB_ORGANIZATION

  Clones all visible repositories for a given organization.

Options:
  --version                       Show the version and exit.
  --token TEXT                    GitHub token to read private repos.
  --threads INTEGER               Number of threads and processes to use.
                                  [default: 4]
  --logging [ERROR|WARNING|INFO|DEBUG]
                                  Logging level  [default: INFO]
  --help                          Show this message and exit.
```

### Example

```bash
python cloner --threads 8 GITHUB_ORGANIZATION
```

## Contributing

Check the [CONTRIBUTING.md](CONTRIBUTING.md) file.

Current status of the project -> [here](https://github.com/w0rmr1d3r/cloner/projects/1?fullscreen=true)

## Security

Follow the instructions in the [SECURITY.md](SECURITY.md) file.

## License

[MIT](https://github.com/w0rmr1d3r/cloner/blob/master/LICENSE)

## Treeware

This package is [Treeware](https://treeware.earth). If you use it in production, then we ask that you [**buy the world a
tree**](https://plant.treeware.earth/w0rmr1d3r/cloner) to thank us for our work. By contributing to the Treeware forest
you’ll be creating employment for local families and restoring wildlife habitats.

## Other & Troubleshooting

Multithreading doesn't work to clone repos, since the `os.system` call is 1 for each PID. The splitting is done with
multithreading, the cloning with multiprocessing. Same amount of threads and processes.

[Windows usage and support](docs/WINDOWS.md)

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=w0rmr1d3r/cloner&type=Date)](https://star-history.com/#w0rmr1d3r/cloner&Date)
