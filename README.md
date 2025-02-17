# codegrab

[![PyPI](https://img.shields.io/pypi/v/codegrab.svg)](https://pypi.org/project/codegrab/)
[![Changelog](https://img.shields.io/github/v/release/geirfreysson/codegrab?include_prereleases&label=changelog)](https://github.com/geirfreysson/codegrab/releases)
[![Tests](https://github.com/geirfreysson/codegrab/actions/workflows/test.yml/badge.svg)](https://github.com/geirfreysson/codegrab/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/geirfreysson/codegrab/blob/master/LICENSE)

A command line tool to fetch code from github for AI purposes.

## Installation

Install this tool using `pip`:
```bash
pip install codegrab
```
## Usage

For help, run:
```bash
codegrab --help
```
You can also use:
```bash
python -m codegrab --help
```
## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd codegrab
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
