import logging
from typing import Optional

from cloner.cloner_process import ClonerProcess
from cloner.repository import Repository

logger = logging.getLogger(__file__)


def clone_repos(
    number_of_threads: int,
    repos_to_clone: list[list[Repository]],
    clone_path: Optional[str] = None,
    git_options: Optional[str] = None,
) -> None:
    """For each given number_of_threads, it creates a ClonerProcess that
    receives the list in repos_to_clone at that the same position. If there are
    more number_of_threads than the length of repos_to_clone, it won't create
    useless Processes. By design, number_of_threads and length of
    repos_to_clone are equal.

    Note: Cannot be tested (yet) since it needs to get os.system mock per process
    """
    list_of_processes = []
    logger.debug(f"Creating processes to clone repos threads={number_of_threads}")
    for i in range(number_of_threads):
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

    for process in list_of_processes:
        process.join()
    logger.debug("All cloner processes joined")
