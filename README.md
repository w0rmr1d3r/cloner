# cloner

A tool to clone efficiently all the repos in an organization

[![CodeQL](https://github.com/w0rmr1d3r/cloner/actions/workflows/codeql-analysis.yml/badge.svg?branch=master)](https://github.com/w0rmr1d3r/cloner/actions/workflows/codeql-analysis.yml)


## Installation

### MacOS (not yet tested)

```bash
python3 -m venv .venv
pip3 install virtualenv
source .venv/bin/activate
pip3 install -r requirements.txt
python3 cloner --help
```

### Windows10

```bash
python3 -m venv .\.venv\
pip3 install virtualenv
.\.venv\Scripts\activate
pip3 install -r .\requirements.txt
python3 cloner --help
```

## Usage

Cloning only public repos:

```bash
python3 cloner <organization>
```

Cloning all the repos your user can see (GitHub token needed):

```bash
python3 cloner <organization> --token=<your_github_token>
```

More info:

```bash
python3 cloner --help
```

To exit the virtual env:

```bash
deactivate
```

## Running Tests (WIP)

With the virtual env active and in the root folder:

```bash
pip3 install -r requirements-dev.txt
pytest tests
```

## Contributing

Issues and Pull Requests are welcome :)

## License

[MIT](https://github.com/w0rmr1d3r/cloner/blob/master/LICENSE)

## Other & Troubleshooting

Multithreading doesn't work to clone repos, since the `os.system` call is 1 for each PID. The splitting is done with
multithreading, the cloning with multiprocessing. Same amount of threads and processes.

If we can't activate the virtual env in Windows10, review with this:

```bash
> Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope CurrentUser
> Get-ExecutionPolicy -List
```
