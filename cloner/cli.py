import logging
import queue
import threading

import click
from requests import HTTPError

from cloner.__version__ import __version__
from cloner.banner import print_banner
from cloner.clone_repos import clone_repos
from cloner.cpu_config import SYSTEM_CORES_NOT_RETRIEVED, get_system_cores, inform_cpu
from cloner.obtain_repos import obtain_repos
from cloner.put_repos_in_queue import put_repos_in_queue
from cloner.split_exclude_repos import split_exclude_repos
from cloner.split_queue import split_queue

LOGGING_LEVELS = {
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}


def setup_logging(level: str) -> None:
    """Logging setup and configuration."""
    logging.basicConfig(level=LOGGING_LEVELS[level], format="%(levelname)s - %(message)s")


@click.command()
@click.version_option(package_name="wr-cloner", prog_name="cloner", version=__version__)
@click.argument("github_organization")
@click.option(
    "--token",
    "token",
    type=str,
    default=None,
    help="GitHub token to read private repos. This parameter is needed when cloning from a GitHub Enterprise server.",
    show_default=True,
)
@click.option(
    "--ghe",
    "github_enterprise",
    type=str,
    default=None,
    help="GitHub Enterprise URL. "
    "It needs the GITHUB_ORGANIZATION parameter to clone repos from there and the TOKEN option as well.",
    show_default=True,
)
@click.option(
    "--threads",
    "threads",
    type=int,
    default=4,
    help="Number of threads and processes to use. For maximum threads and processes on the system, use '--max-threads'",
    show_default=True,
)
@click.option(
    "--max-threads",
    "max_threads",
    type=bool,
    is_flag=True,
    default=False,
    help="If declared, uses the maximum available threads and processes in the system. "
    "As per physical cores on the system cpu.",
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
@click.option(
    "--path",
    "clone_path",
    type=str,
    default=None,
    help="Sets a path where to clone the repositories (eg: ./another/path/)",
    show_default=True,
)
@click.option(
    "--git-options",
    "git_options",
    type=str,
    default=None,
    help='Add options to the clone command (eg: --git-options "--depth 1"). By default, clones quietly (--quiet).',
    show_default=True,
)
@click.option(
    "--ignore-archived",
    "ignore_archived",
    type=bool,
    is_flag=True,
    default=False,
    help="If declared, will ignore archived repos when cloning.",
    show_default=True,
)
@click.option(
    "--ignore-template",
    "ignore_template",
    type=bool,
    is_flag=True,
    default=False,
    help="If declared, will ignore template repos when cloning.",
    show_default=True,
)
@click.option(
    "--ignore-fork",
    "ignore_fork",
    type=bool,
    is_flag=True,
    default=False,
    help="If declared, will ignore fork repos when cloning.",
    show_default=True,
)
@click.option(
    "--exclude-repos",
    "exclude_repos",
    type=str,
    default="",
    help='Comma separated list of repository names to exclude from cloning. Example: "repository1,repository2".',
    show_default=True,
)
def cli(  # noqa: PLR0913, PLR0917
    github_organization: str,
    token: str,
    github_enterprise: str,
    threads: int,
    max_threads: bool,
    logging_level: str,
    clone_path: str,
    git_options: str,
    ignore_archived: bool,
    ignore_template: bool,
    ignore_fork: bool,
    exclude_repos: str,
) -> None:
    """A tool to clone efficiently all the repos in an organization."""
    setup_logging(level=logging_level)

    print_banner()

    # We override the value of threads if max_threads is declared and if we can retrieve the number of cores
    if max_threads and get_system_cores() != SYSTEM_CORES_NOT_RETRIEVED:
        threads = get_system_cores()

    inform_cpu(selected_threads=threads)

    logging.info(f"Cloning repos for: {github_organization}")

    repository_list_queue_lock = threading.Lock()
    repository_list_queue = queue.Queue()

    transformed_excluded_repos = split_exclude_repos(exclude_repos=exclude_repos)

    try:
        put_repos_in_queue(
            json_response=obtain_repos(
                github_organization=github_organization,
                github_token=token,
                ghe=github_enterprise,
            ),
            queue_lock=repository_list_queue_lock,
            repo_queue=repository_list_queue,
            ignore_archived=ignore_archived,
            ignore_template=ignore_template,
            ignore_fork=ignore_fork,
            exclude_repos=transformed_excluded_repos,
        )
    except HTTPError:
        logging.error("An error has occurred while obtaining repos", exc_info=True)

    total_repos_to_clone = repository_list_queue.qsize()
    logging.info(f"Total repos to clone: {total_repos_to_clone}")

    if total_repos_to_clone > 0:
        repos_to_clone = split_queue(
            number_of_threads=threads,
            repository_queue=repository_list_queue,
            repository_queue_lock=repository_list_queue_lock,
        )

        logging.info("Cloning repos...")

        clone_repos(
            number_of_threads=threads,
            repos_to_clone=repos_to_clone,
            clone_path=clone_path,
            git_options=git_options,
        )

        logging.info("Repos cloned!")
