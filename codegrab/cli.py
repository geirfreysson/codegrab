import click
import requests
import re
import os
from urllib.parse import urlparse
import ast

GITHUB_API_URL = "https://api.github.com/repos/{owner}/{repo}/contents/{path}"
LIST_FILES_URL = "https://api.github.com/repos/{owner}/{repo}/contents/"


def get_default_branch(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {}
    
    github_token = os.getenv("GITHUB_TOKEN")
    if github_token:
        headers["Authorization"] = f"token {github_token}"
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("default_branch", "main")
    return "main"

def get_github_file(owner, repo, path, ref=None):
    if not ref:
        ref = get_default_branch(owner, repo)
    url = GITHUB_API_URL.format(owner=owner, repo=repo, path=path)
    headers = {"Accept": "application/vnd.github.v3.raw"}
    
    github_token = os.getenv("GITHUB_TOKEN")
    if github_token:
        headers["Authorization"] = f"token {github_token}"
    
    response = requests.get(url, headers=headers, params={"ref": ref})
    
    if response.status_code == 200:
        return response.text
    else:
        click.echo(f"Error: {response.status_code} - {response.text}", err=True)
        return None

def list_python_files(owner, repo, ref=None):
    if not ref:
        ref = get_default_branch(owner, repo)
    url = LIST_FILES_URL.format(owner=owner, repo=repo)
    headers = {}
    
    github_token = os.getenv("GITHUB_TOKEN")
    if github_token:
        headers["Authorization"] = f"token {github_token}"
    
    response = requests.get(url, headers=headers, params={"ref": ref})
    
    if response.status_code == 200:
        files = [f["path"] for f in response.json() if f["type"] == "file" and f["path"].endswith(".py")]
        return files
    else:
        click.echo(f"Error: {response.status_code} - {response.text}", err=True)
        return []

def extract_function_code(content: str, function_name: str) -> str:
    """
    Extracts the function definition and its body from a given Python class code.

    Parameters:
        content (str): The string representation of the class code.
        function_name (str): The name of the function to extract.

    Returns:
        str: The extracted function definition including decorators.
    """
    tree = ast.parse(content)
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            # Get the start and end line numbers
            start_line = node.lineno - 1  # Convert to 0-based index
            end_line = node.end_lineno  # Last line of the function
            
            # Extract relevant lines
            lines = content.splitlines()
            extracted_code = "\n".join(lines[start_line:end_line])
            return extracted_code

    return f"Function '{function_name}' not found."



@click.command()
@click.argument("module_function", required=True)
@click.option("--repo", help="Specify GitHub repository URL (e.g., https://github.com/user/repo)")
@click.option("--branch", default=None, help="Specify branch or commit hash.")
def cli(module_function, repo, branch):
    "Fetch a module or function locally or from a GitHub repository."
    try:
        if repo:
            parsed_url = urlparse(repo)
            if parsed_url.netloc != "github.com" or len(parsed_url.path.strip("/").split("/")) != 2:
                click.echo("Error: Invalid GitHub repository URL. Expected format: https://github.com/owner/repo", err=True)
                return
            
            owner, repo_name = parsed_url.path.strip("/").split("/")
            
            if not branch:
                branch = get_default_branch(owner, repo_name)
            
            if ":" in module_function:
                module_path, function_name = module_function.split(":", 1)
            else:
                module_path, function_name = module_function, None
            
            file_path = module_path.replace(".", "/") + ".py"
            content = get_github_file(owner, repo_name, file_path, branch)
            
            if content:
                if function_name:
                    function_code = extract_function_code(content, function_name)
                    if function_code:
                        click.echo(function_code)
                    else:
                        click.echo(f"Error: Function '{function_name}' not found.", err=True)
                else:
                    click.echo(content)
            else:
                click.echo(f"Error: Could not retrieve file '{file_path}' from repository.", err=True)
        else:
            if ":" in module_function:
                module_path, function_name = module_function.split(":", 1)
            else:
                module_path, function_name = module_function, None
            
            file_path = module_path.replace(".", "/") + ".py"
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    content = f.read()
                
                if function_name:
                    function_code = extract_function_code(content, function_name)
                    if function_code:
                        click.echo(function_code)
                    else:
                        click.echo(f"Error: Function '{function_name}' not found.", err=True)
                else:
                    click.echo(content)
            else:
                click.echo(f"Error: File '{file_path}' not found.", err=True)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)

