# codegrab

[![PyPI](https://img.shields.io/pypi/v/codegrab.svg)](https://pypi.org/project/codegrab/)
[![Changelog](https://img.shields.io/github/v/release/geirfreysson/codegrab?include_prereleases&label=changelog)](https://github.com/geirfreysson/codegrab/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/geirfreysson/codegrab/blob/master/LICENSE)

# codegrab

codegrab is a command-line tool that allows you to extract Python module or function code from local files or directly from a GitHub repository. It concatenates all files fetched to prepare for feeding into LLMs.

## Features
- Retrieve an entire Python module locally or from a GitHub repository.
- Extract specific function definitions, including decorators.
- Supports specifying a GitHub repository and branch to fetch files remotely.
- Concats all results.

## Why this is useful

By fetching code and concatting it into a string, you can feed it into tools like Simon Willison's command-line tool [llm](https://github.com/simonw/llm).

The following will take one function from the specified code base, compare it to another, and use OpenAI to give feedback on why one works and not the other by piping it into the `llm` command.
```
uv run codegrab module.location:function --repo [private repo] \
 | uv run codegrab other_module.location:function --repo [private repo] \
 | llm --system "The first function does not work, the second one does. The first one fails when I supply stats=['mean'] whereas the second one successfully includes stats. Can you see what the difference could be? Can you suggest changes to the first implementation so that it accepts stats in the same way the second one does?"
```

Fetching code as a string could also be used to load a prompt with lots of examples to show it how to write domain specific code and so on.

## Installation

```sh
pip install codegrab
```

Alternatively, you can run it without installing using uv:

```sh
uvx codegrab
```

## Usage

### Extract a Local Python Module
To retrieve the full code of a module from your local file system:

```sh
codegrab module.submodule
```

### Fetch from a GitHub Repository
If the `--repo` option is provided, CodeGrab fetches the file from a GitHub repository instead of the local system:

```sh
codegrab module.submodule --repo https://github.com/user/repo
```

By default, CodeGrab fetches from the repository's default branch. You can specify a different branch using the `--branch` option:

```sh
codegrab module.submodule --repo https://github.com/user/repo --branch dev
```

Example:

Download and concat the LLM module from Simon Willison's command-line `llm` tool.

```sh
codegrab llm --repo https://github.com/simonw/llm
```

### Extract a Specific Function
To retrieve only the code for a specific function within a module:

```sh
codegrab module.submodule:function_name
```

Example: 

```sh
codegrab llm.cli:prompt --repo https://github.com/simonw/llm
```
This will retreive the `prompt` method from the `llm` repository.

> [!NOTE]  
> codegrab doesn't support scoping the function being retreived to a class, it currently fethces the first function that matches the name in the file.


### Environment Variables
To avoid GitHub rate limiting, you can set a personal access token:

```sh
export GITHUB_TOKEN=your_personal_token
```

## Error Handling
- If the file or function is not found, an error message is displayed.
- If the GitHub request fails, an HTTP error code is shown.

## License
MIT License

## Contributions
Feel free to open issues and submit pull requests to improve codegrab!

