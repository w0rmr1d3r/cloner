import logging
import queue
import threading

import click

from obtain_repos import obtain_repos
from __version__ import __version__
from cloner_process import ClonerProcess

repository_list_queue_lock = threading.Lock()
repository_list_queue = queue.Queue()
exit_flag = False

LOGGING_LEVELS = {
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}


def setup_logging(level: str) -> None:
    """Logging setup and configuration."""
    logging.basicConfig(level=LOGGING_LEVELS[level], format='%(levelname)s - %(message)s')


# todo - can this be moved to another file? if so, do so
class SplitterThread(threading.Thread):
    """Class to split the queue of repos into a list."""

    def __init__(self, thread_id: int, total_threads: int):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.repos_to_clone_list = []
        self.total_threads = total_threads

    def run(self):
        logging.debug(f"Starting thread -> {self.thread_id}")
        self.process_repo()
        logging.debug(f"Thread -> {self.thread_id} has {len(self.repos_to_clone_list)} repos")
        logging.debug(f"Exiting thread -> {self.thread_id}")

    def process_repo(self) -> None:
        """
        Obtains a repo from the queue and puts it in its list if the mod of the repo identifier equals this thread id.
        Puts the repo back to the queue otherwise.
        """
        while not exit_flag:
            repository_list_queue_lock.acquire()
            if not repository_list_queue.empty():
                repository = repository_list_queue.get()
                if repository.repo_id % self.total_threads == self.thread_id:
                    self.repos_to_clone_list.append(repository)
                else:
                    repository_list_queue.put(repository)
                repository_list_queue_lock.release()
                # logging.debug(f"Thread {self.thread_id} processing {repository.name}")
            else:
                repository_list_queue_lock.release()

    def __str__(self):
        return f"Thread: {self.thread_id}"


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

    cloner_threads_list = []
    for i in range(threads):
        thread = SplitterThread(thread_id=i, total_threads=threads)
        cloner_threads_list.append(thread)
        thread.start()

    while not repository_list_queue.empty():
        pass

    global exit_flag
    exit_flag = True

    for t in cloner_threads_list:
        logging.debug(f"Length of thread {t} clone repo list is {len(t.repos_to_clone_list)}")
        t.join()

    logging.info('Cloning repos...')

    list_of_processes = []
    for i in range(threads):
        process = ClonerProcess(repos_to_clone=cloner_threads_list[i].repos_to_clone_list, process_id=i)
        list_of_processes.append(process)
        process.start()

    for process in list_of_processes:
        process.join()

    logging.info('Repos cloned!')


# can this be deleted?
if __name__ == "__main__":
    cli()

# todo -> https://stackoverflow.com/questions/11436502/closing-all-threads-with-a-keyboard-interrupt
# add license in all parts of the software?
