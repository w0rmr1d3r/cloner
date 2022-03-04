from cloner.cloner_process import ClonerProcess
from cloner.repository import Repository


# todo - needs tests
def clone_repos(number_of_threads: int, repos_to_clone: list[list[Repository]]) -> None:
    list_of_processes = []
    for i in range(number_of_threads):
        process = ClonerProcess(repos_to_clone=repos_to_clone[i], process_id=i)
        list_of_processes.append(process)
        process.start()

    for process in list_of_processes:
        process.join()
