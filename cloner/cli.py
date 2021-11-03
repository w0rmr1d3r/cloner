import logging
import queue
import threading

import click

from __version__ import __version__
from cloner_process import ClonerProcess
from obtain_repos import obtain_repos
from split_queue import split_queue

repository_list_queue_lock = threading.Lock()
repository_list_queue = queue.Queue()

LOGGING_LEVELS = {
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}


def setup_logging(level: str) -> None:
    """Logging setup and configuration."""
    logging.basicConfig(level=LOGGING_LEVELS[level], format='%(levelname)s - %(message)s')


@click.command()
@click.version_option(prog_name='cloner', version=__version__)
@click.argument('github_organization')
@click.option(
    '--token',
    'token',
    type=str,
    default=None,
    help='GitHub token to read private repos.',
    show_default=True,
)
@click.option(
    '--threads',
    'threads',
    type=int,
    default=4,
    help='Number of threads and processes to use.',
    show_default=True,
)
@click.option(
    "--logging",
    "logging_level",
    type=click.Choice(LOGGING_LEVELS.keys(), case_sensitive=True),
    default="INFO",
    help="Logging level",
    show_default=True,
)
def cli(github_organization, token, threads, logging_level):
    """Clones all visible repositories for a given organization."""
    setup_logging(level=logging_level)

    logging.info(f"Cloning repos for: {github_organization}")

    obtain_repos(github_organization=github_organization,
                 github_token=token,
                 queue_lock=repository_list_queue_lock,
                 repo_queue=repository_list_queue)

    logging.info(f"Total repos to clone: {repository_list_queue.qsize()}")

    repos_to_clone = split_queue(number_of_threads=threads,
                                 repository_queue=repository_list_queue,
                                 repository_queue_lock=repository_list_queue_lock)

    logging.info('Cloning repos...')

    list_of_processes = []
    for i in range(threads):
        process = ClonerProcess(repos_to_clone=repos_to_clone[i], process_id=i)
        list_of_processes.append(process)
        process.start()

    for process in list_of_processes:
        process.join()

    logging.info('Repos cloned!')


# can this be deleted?
if __name__ == "__main__":
    cli()

# todo -> https://stackoverflow.com/questions/11436502/closing-all-threads-with-a-keyboard-interrupt
