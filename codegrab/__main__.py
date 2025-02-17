try:
    from .cli import cli  # Try relative import first
except ImportError:
    from codegrab.cli import cli  # Fall back to absolute import

if __name__ == "__main__":
    cli()
