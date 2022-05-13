import logging

from cloner.cloner_process import ClonerProcess
from cloner.repository import Repository

logger = logging.getLogger(__file__)


def clone_repos(number_of_threads: int, repos_to_clone: list[list[Repository]]) -> None:
    """
    For each given number_of_threads, it creates a ClonerProcess that receives the list in repos_to_clone at that
    the same position.
    If there are more number_of_threads than the length of repos_to_clone, it won't create useless Processes.
    By design, number_of_threads and length of repos_to_clone are equal.

    Note: Cannot be tested (yet) since it needs to get os.system mock per process
    """
    list_of_processes = []
    logger.debug(f"Creating processes to clone repos threads={number_of_threads}")
    for i in range(number_of_threads):
        try:
            process = ClonerProcess(repos_to_clone=repos_to_clone[i], process_id=i)
            list_of_processes.append(process)
            process.start()
        except IndexError:
            pass

    for process in list_of_processes:
        process.join()
    logger.debug("All processes joined")
