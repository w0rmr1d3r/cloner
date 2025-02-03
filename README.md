# cloner

A tool to clone efficiently all the repos in an organization

[![PyPI](https://img.shields.io/pypi/v/wr-cloner)](https://pypi.org/project/wr-cloner/)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/w0rmr1d3r/cloner)](https://github.com/w0rmr1d3r/cloner/releases)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wr-cloner)
![GitHub last commit](https://img.shields.io/github/last-commit/w0rmr1d3r/cloner)
[![CI](https://github.com/w0rmr1d3r/cloner/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/w0rmr1d3r/cloner/actions/workflows/ci.yml)
[![CodeQL](https://github.com/w0rmr1d3r/cloner/actions/workflows/codeql.yml/badge.svg?branch=master)](https://github.com/w0rmr1d3r/cloner/actions/workflows/codeql.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/w0rmr1d3r/cloner/badge)](https://scorecard.dev/viewer/?uri=github.com/w0rmr1d3r/cloner)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/9982/badge)](https://www.bestpractices.dev/projects/9982)
[![PyPi downloads](https://img.shields.io/pypi/dm/wr-cloner?label=PyPi%20downloads)](https://pypistats.org/packages/wr-cloner)
[![PyPI Downloads](https://static.pepy.tech/badge/wr-cloner/month)](https://pepy.tech/projects/wr-cloner)

## Install

_In PyPi it's called **wr-cloner**, cloner was already taken :sad:_

```bash
pip install wr-cloner
```

## Usage

_Note: If using cloner after cloning the project and not a PyPi package, add "python" at the start.
There's an example of that in the examples section._

```text
Usage: cloner [OPTIONS] GITHUB_ORGANIZATION

  A tool to clone efficiently all the repos in an organization.

Options:
  --version                       Show the version and exit.
  --token TEXT                    GitHub token to read private repos. This
                                  parameter is needed when cloning from a
                                  GitHub Enterprise server.
  --ghe TEXT                      GitHub Enterprise URL. It needs the
                                  GITHUB_ORGANIZATION parameter to clone repos
                                  from there and the TOKEN option as well.
  --threads INTEGER               Number of threads and processes to use. For
                                  maximum threads and processes on the system,
                                  use '--max-threads'  [default: 4]
  --max-threads                   If declared, uses the maximum available
                                  threads and processes in the system. As per
                                  physical cores on the system cpu.
  --logging [ERROR|WARNING|INFO|DEBUG]
                                  Logging level  [default: INFO]
  --path TEXT                     Sets a path where to clone the repositories
                                  (eg: ./another/path/)
  --git-options TEXT              Add options to the clone command (eg: --git-
                                  options "--depth 1"). By default, clones
                                  quietly (--quiet).
  --ignore-archived               If declared, will ignore archived repos when
                                  cloning.
  --ignore-template               If declared, will ignore template repos when
                                  cloning.
  --ignore-fork                   If declared, will ignore fork repos when
                                  cloning.
  --exclude-repos TEXT            Comma separated list of repository names to
                                  exclude from cloning. Example:
                                  "repository1,repository2".
  --help                          Show this message and exit.
```

### Examples

```bash
# For github.com with 8 threads
cloner --threads 8 GITHUB_ORGANIZATION

# For github.com with the maximum threads on the system running
cloner --max-threads GITHUB_ORGANIZATION

# For GHE, default threads
cloner --ghe GHE_URL --token SUPER_SECURE_TOKEN GITHUB_ORGANIZATION

# Cloning with options
cloner --git-options "--depth 1" GITHUB_ORGANIZATION
```

### Examples if cloning the repo

```bash
# Install dependencies with
make install
# Adjust PYTHONPATH
export PYTHONPATH=$PYTHONPATH:.
# Use it
python cloner GITHUB_ORGANIZATION
```

## Contributing

Check the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## Security

Follow the instructions in the [SECURITY.md](SECURITY.md) file.

## License

[MIT](https://github.com/w0rmr1d3r/cloner/blob/master/LICENSE)

## Known Issues

- Multithreading doesn't work to clone repos, since the `os.system` call is 1 for each PID. The splitting is done with
  multithreading, the cloning with multiprocessing. Same amount of threads and processes.
- [Windows usage and support](docs/WINDOWS.md)
- If seeing `RPC failed; curl 92 HTTP/2 stream 5 was not closed cleanly: CANCEL (err 8)` either adjust your git config,
  as
  per [this StackOverflow issue](https://stackoverflow.com/questions/59282476/error-rpc-failed-curl-92-http-2-stream-0-was-not-closed-cleanly-protocol-erro).
  If still persists, either decrease the number of threads using the `--threads` option or adjust the depth of cloning
  with `--git-options "--depth 10"` (10 or any other small number).

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=w0rmr1d3r/cloner&type=Date)](https://star-history.com/#w0rmr1d3r/cloner&Date)
