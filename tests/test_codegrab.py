import pytest
from unittest.mock import patch, mock_open
from click.testing import CliRunner
from codegrab.cli import cli, get_github_file, list_python_files, extract_function_code


@patch('requests.get')
def test_get_github_file(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = 'def test_function():\n    pass\n'
    
    content = get_github_file('owner', 'repo', 'path/to/file.py')
    assert content == 'def test_function():\n    pass\n'


def test_extract_function_code():
    code = """
def test_function():
    pass

def another_function():
    pass
"""
    function_code = extract_function_code(code, 'test_function')
    assert function_code.strip() == 'def test_function():\n    pass'


@patch('os.getenv')
@patch('requests.get')
def test_cli_remote(mock_get, mock_getenv):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = 'def test_function():\n    pass\n'
    mock_getenv.return_value = None
    
    runner = CliRunner()
    result = runner.invoke(cli, ['path.to.module:test_function', '--repo', 'https://github.com/owner/repo'])
    assert result.exit_code == 0
    assert 'def test_function()' in result.output


@patch("builtins.open", mock_open(read_data="def local_function():\n    pass\n"))
@patch('os.path.isdir', return_value=False)
@patch('os.path.exists', return_value=True)
def test_cli_local(mock_exists, mock_isdir):
    runner = CliRunner()
    result = runner.invoke(cli, ['path.to.module:local_function'])
    
    assert result.exit_code == 0
    assert 'def local_function()' in result.output


@patch("builtins.open", mock_open(read_data="def function():\n    pass\n"))
@patch('os.path.isdir', return_value=False)
@patch('os.path.exists', return_value=True)
def test_cli_local_file_not_found(mock_exists, mock_isdir):
    runner = CliRunner()
    result = runner.invoke(cli, ['non.existent.path:local_function'])
    
    assert result.exit_code == 0
    assert "Function 'local_function' not found." in result.output


@patch("builtins.open", mock_open(read_data="def another_function():\n    pass\n"))
@patch('os.path.isdir', return_value=False)
@patch('os.path.exists', return_value=True)
def test_cli_local_function_not_found(mock_exists, mock_isdir):
    runner = CliRunner()
    result = runner.invoke(cli, ['existing.path:non_existent_function'])    
    assert result.exit_code == 0
    assert "Function 'non_existent_function' not found." in result.output