import click


def banner() -> str:
    """Returns the banner as a str."""
    return """
───╔╗
───║║
╔══╣║╔══╦═╗╔══╦═╗
║╔═╣║║╔╗║╔╗╣║═╣╔╝
║╚═╣╚╣╚╝║║║║║═╣║
╚══╩═╩══╩╝╚╩══╩╝
"""


def print_banner():
    """Prints the banner."""
    click.secho(banner(), fg="green")
