import logging
from typing import Optional

from click import progressbar

from cloner.cloner_process import ClonerProcess
from cloner.repository import Repository

logger = logging.getLogger(__file__)


def clone_repos(
    number_of_threads: int,
    repos_to_clone: list[list[Repository]],
    clone_path: Optional[str] = None,
    git_options: Optional[str] = None,
) -> None:
    """
    For each given number_of_threads, it creates a ClonerProcess.

    Each process receives the list in `repos_to_clone` in the same position.

    If there are more number_of_threads than the length of repos_to_clone, it won't create
    useless Processes. By design, number_of_threads and length of
    repos_to_clone are equal.

    Note: Cannot be tested (yet) since it needs to get `os.system` mock per process
    """
    list_of_processes = []
    logger.debug(f"Creating processes to clone repos threads={number_of_threads}")

    with progressbar(range(number_of_threads), label="Starting processes to clone repos") as bar:
        for i in bar:
            try:
                process = ClonerProcess(
                    repos_to_clone=repos_to_clone[i],
                    process_id=i,
                    clone_path=clone_path,
                    git_options=git_options,
                )
                list_of_processes.append(process)
                process.start()
            except IndexError:
                logger.warning("IndexError has occurred when passing repos to ClonerProcess")

    with progressbar(list_of_processes, label="Joining processes to clone repos") as bar:
        for process in bar:
            process.join()
    logger.debug("All cloner processes joined")
