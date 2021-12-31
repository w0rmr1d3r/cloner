# cloner

A tool to clone efficiently all the repos in an organization

[![CodeQL](https://github.com/w0rmr1d3r/cloner/actions/workflows/codeql-analysis.yml/badge.svg?branch=master)](https://github.com/w0rmr1d3r/cloner/actions/workflows/codeql-analysis.yml)
[![Known Vulnerabilities](https://snyk.io/test/github/w0rmr1d3r/cloner/badge.svg)](https://snyk.io/test/github/w0rmr1d3r/cloner)
[![Generic badge](https://img.shields.io/badge/python-3.10-success.svg)](https://shields.io/)

Current status of the project -> [here](https://github.com/w0rmr1d3r/cloner/projects/1?fullscreen=true)

## Requirements

* [pyenv](https://github.com/pyenv/pyenv)
* [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)
* Virtual env created with Python 3.10.0 (supported version)
* Install requirements with `make install`

## Usage

With the virtualenv active:

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

## Running Tests

With the virtual env active:

```bash
make install-dev
make unit
```

## Contributing

Issues and Pull Requests are welcome :)

## Security

If a security issue is found, please follow the instructions in the [SECURITY.md](SECURITY.md) file.

## License

[MIT](https://github.com/w0rmr1d3r/cloner/blob/master/LICENSE)

`Makefile` and `setup.py` based on [Skyscanner cfripper](https://github.com/Skyscanner/cfripper).

## Other & Troubleshooting

Multithreading doesn't work to clone repos, since the `os.system` call is 1 for each PID. The splitting is done with
multithreading, the cloning with multiprocessing. Same amount of threads and processes.

[Windows usage and support](docs/WINDOWS.md)

## Stargazers over time

[![Stargazers over time](https://starchart.cc/w0rmr1d3r/cloner.svg)](https://starchart.cc/w0rmr1d3r/cloner)
