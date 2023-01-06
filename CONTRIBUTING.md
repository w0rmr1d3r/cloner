# Contributing

Issues and Pull Requests are welcome :)

### Requirements

* [pyenv](https://github.com/pyenv/pyenv)
* [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)
* Virtual env created with at least Python 3.9
* Install dev requirements with `make install-dev`
* Ready to contribute!

### Running Tests

With the virtual env active:

```bash
# Only once
make install-dev
# Both linting and tests
make test
# Only tests
make unit
# Only code lint
make lint
```
