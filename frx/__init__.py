import click
from frx.add import add


@click.version_option()
@click.group()
def main():
    """Manage frx variable."""
    pass


main.add_command(add)
