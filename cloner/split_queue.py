import logging
import queue
import threading

from cloner.repository import Repository

logger = logging.getLogger(__file__)

exit_flag = False
repository_list_queue_lock = None
repository_list_queue = None

# todo - all this class needs tests


def split_queue(
    number_of_threads: int,
    repository_queue: queue.Queue,
    repository_queue_lock: threading.Lock(),
) -> list[list[Repository]]:
    """Splits the queue of repos into a list of repo lists, one per thread"""

    global repository_list_queue_lock, repository_list_queue
    repository_list_queue_lock = repository_queue_lock
    repository_list_queue = repository_queue

    thread_list = []
    repos_to_clone = []

    for i in range(number_of_threads):
        thread = SplitterThread(thread_id=i, total_threads=number_of_threads)
        thread_list.append(thread)
        thread.start()

    while not repository_queue.empty():
        pass

    global exit_flag
    exit_flag = True

    for t in thread_list:
        logger.debug(
            f"Length of thread {t} clone repo list is {len(t.repos_to_clone_list)}"
        )
        t.join()
        repos_to_clone.append(t.repos_to_clone_list)

    return repos_to_clone


class SplitterThread(threading.Thread):
    """Class to split the queue of repos into a list."""

    def __init__(self, thread_id: int, total_threads: int):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.repos_to_clone_list = []
        self.total_threads = total_threads

    def run(self):
        logger.debug(f"Starting thread -> {self.thread_id}")
        self.process_repo()
        logger.debug(
            f"Thread -> {self.thread_id} has {len(self.repos_to_clone_list)} repos"
        )
        logger.debug(f"Exiting thread -> {self.thread_id}")

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
            else:
                repository_list_queue_lock.release()

    def __str__(self):
        return f"Thread: {self.thread_id}"
