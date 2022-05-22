# Django Tutorial
A template for all new Python projects to follow.

## Getting Started
1. Clone this repo
2. Open with VS Code and start the dev container
3. Open a terminal and run `make setup` (within dev container)
4. Navigate to VS Code Extensions and 'reload' Python extension

## Features

### Makefile Interface
This repo implements the Makefile interface

### Dev Container
A Python-based [dev container](https://code.visualstudio.com/learn/develop-cloud/containers) is provided with all tools and linters configured.
There has been deliberate effort to make VS Code's issue highlighting well-aligned with the CLI-based checks (if not, it should be fixed - the IDE is _the_ earliest and most valuable place to detect code issues).

### Package Management
[Poetry](https://python-poetry.org/) is used to manage packages and provide a deterministic dependency tree.

### Formatting
* [Black](https://black.readthedocs.io/en/stable/) is used for opinionated code formatting.
* [isort](https://pycqa.github.io/isort/) is used for arranging imports into correct order.

### Linting
* [Flake8](https://flake8.pycqa.org/en/latest/) is used with the opinionated [wemake-python-styleguide](https://github.com/wemake-services/wemake-python-styleguide) plugin and some additional plugins.  Collectively, these analyse things like:
    * Code complexity
    * Code smells
    * Insecure code
    * Docstring argument drift
    * Styling and spacing issues
    * Leftover debug statements
* [Pylint](https://pylint.org/) is used to find issues that Flake8 misses.

### Type Checks
[mypy](http://mypy-lang.org/) is used for static type checks.

### Dependency Checks
[Safety](https://pypi.org/project/safety/) is used to analyse the current list of dependencies for security risks.

### Pre-commit Hooks
[Pre-commit](https://pre-commit.com/) is used to run all checks and tests before allowing a commit to proceed.

## Notes
This template is not static - it should evolve from changing needs and feedback during every-day use.
