import logging
import os
from functools import lru_cache

logger = logging.getLogger(__file__)


@lru_cache
def get_system_cores() -> int:
    """Returns the available system cores or physical cpus by calling the OS to
    retrieve such information. If it cannot be retrieved, it will return -1.

    Not using `len(os.sched_getaffinity(0))` since when it runs,
    the current process can already be limited to a set of cores.

    Ref. https://docs.python.org/3/library/os.html#os.cpu_count
    """
    cpu_count = os.cpu_count()
    if cpu_count is None:
        logging.warning("Could not determine the number of CPUs")
        return -1
    return cpu_count


def inform_cpu(selected_threads: int):
    """Will log a warning if the number of given threads is either lower or
    higher than the amount of cores the system running it has.

    It won't log anything if either is the same number or wasn't able to
    retrieve the cpu cores.
    """
    system_cores = get_system_cores()
    if system_cores == -1:
        return
    if selected_threads < system_cores:
        logging.warning(
            f"You have selected less threads than available in your system. "
            f"Available={system_cores} Selected={selected_threads}"
        )
    elif selected_threads > system_cores:
        logging.warning(
            f"You have selected more threads than available in your system. "
            f"Available={system_cores} Selected={selected_threads}"
        )
