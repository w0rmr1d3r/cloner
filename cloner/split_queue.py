import logging
import queue
import threading

from cloner.repository import Repository

logger = logging.getLogger(__file__)

EXIT_FLAG = False
REPOSITORY_LIST_QUEUE_LOCK = None
REPOSITORY_LIST_QUEUE = None


def set_exit_flag():
    """Will set to `True` the EXIT_FLAG."""
    global EXIT_FLAG
    EXIT_FLAG = True


def reset_exit_flag():
    """Will reset the EXIT_FLAG back to `False`"""
    global EXIT_FLAG
    EXIT_FLAG = False


class ThreadsBelowOne(Exception):
    """Exception to be thrown when the declared threads to split the queue is
    below 1."""

    def __init__(self, message="Threads declared should be higher than 0."):
        super().__init__(message)


def split_queue(
    number_of_threads: int,
    repository_queue: queue.Queue,
    repository_queue_lock: threading.Lock(),
) -> list[list[Repository]]:
    """Splits the queue of repos into a list of lists of repos, one per
    thread."""

    if number_of_threads < 1:
        raise ThreadsBelowOne

    global REPOSITORY_LIST_QUEUE_LOCK, REPOSITORY_LIST_QUEUE
    REPOSITORY_LIST_QUEUE_LOCK = repository_queue_lock
    REPOSITORY_LIST_QUEUE = repository_queue

    thread_list = []
    repos_to_clone = []

    for i in range(number_of_threads):
        thread = SplitterThread(thread_id=i, total_threads=number_of_threads)
        thread_list.append(thread)
        thread.start()

    while not repository_queue.empty():
        pass

    set_exit_flag()

    for splitter_thread in thread_list:
        logger.debug(f"About to join thread {splitter_thread}")
        splitter_thread.join()
        logger.debug(
            f"Length of thread {splitter_thread} clone repo list is {len(splitter_thread.repos_to_clone_list)}"
        )
        repos_to_clone.append(splitter_thread.repos_to_clone_list)

    reset_exit_flag()

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
        logger.debug(f"Thread -> {self.thread_id} has {len(self.repos_to_clone_list)} repos")
        logger.debug(f"Exiting thread -> {self.thread_id}")

    def process_repo(self) -> None:
        """Obtains a repo from the queue and puts it in its list if the mod of
        the repo identifier equals this thread id.

        Puts the repo back to the queue otherwise.
        """
        # The EXIT_FLAG tell us when it's time to stop working
        while not EXIT_FLAG:
            # We acquire the lock before checking anything,
            # this will make working with the queue safe from other threads
            REPOSITORY_LIST_QUEUE_LOCK.acquire()
            if not REPOSITORY_LIST_QUEUE.empty():
                # If it's not empty, we will get an element from the queue and deal with it
                repository = REPOSITORY_LIST_QUEUE.get()
                if repository.repo_id % self.total_threads == self.thread_id:
                    self.repos_to_clone_list.append(repository)
                else:
                    REPOSITORY_LIST_QUEUE.put(repository)
                # We release the lock to let other threads work
                REPOSITORY_LIST_QUEUE_LOCK.release()
            else:
                # If the queue is empty, we will release the lock, to let other threads work
                REPOSITORY_LIST_QUEUE_LOCK.release()

    def __str__(self):
        return f"Thread: {self.thread_id}"
