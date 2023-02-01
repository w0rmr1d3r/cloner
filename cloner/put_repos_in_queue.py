import queue
import threading
from typing import Any

from cloner.repository import Repository


def put_repos_in_queue(
    json_response: list[dict[str, Any]],
    queue_lock: threading.Lock,
    repo_queue: queue.Queue,
) -> None:
    """Puts into the queue repositories obtained from a dictionary Each element
    of the json_response is a dictionary containing the GitHub response with
    repository information."""
    queue_lock.acquire()
    for repo_number in range(len(json_response)):
        repo_queue.put(
            Repository(
                name=json_response[repo_number]["name"],
                clone_url=json_response[repo_number]["clone_url"],
                repo_id=repo_number,
            )
        )
    queue_lock.release()
