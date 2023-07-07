import click


def print_ok(message: str):
    click.secho(message, fg="green")


def print_info(message: str):
    click.secho(message, fg="blue")


def print_warn(message: str):
    click.secho(message, fg="yellow")


def print_error(message: str):
    click.secho(message, fg="red")
