import logging

import psutil

logger = logging.getLogger(__file__)


def inform_cpu(selected_threads: int):
    """
    Will log a warning if the number of given threads is either
    lower or higher than the amount of cores the system running it has.
    """
    system_cores = psutil.cpu_count()
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
