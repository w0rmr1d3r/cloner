from cloner.print_options import print_ok


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
    print_ok(banner())
