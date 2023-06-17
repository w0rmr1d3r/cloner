import queue
import threading
from typing import Any

from cloner.repository import Repository


def put_repos_in_queue(
    json_response: list[dict[str, Any]], queue_lock: threading.Lock, repo_queue: queue.Queue, ignore_archived: bool
) -> None:
    """Puts into the queue repositories obtained from a list of dicts.

    Each element of the json_response is a dictionary containing the GitHub response with
    repository information.

    If ignore_archived is passed and the repo is archived, won't add it to the queue.

    Raises `KeyError` in case the `cloner_url` in a response doesn't exist.
    """
    queue_lock.acquire()
    for repo_number in range(len(json_response)):
        if ignore_archived and json_response[repo_number].get("archived", False):
            continue
        repo_queue.put(
            Repository(
                name=json_response[repo_number].get("name", ""),
                clone_url=json_response[repo_number]["clone_url"],
                repo_id=repo_number,
                is_template=json_response[repo_number].get("is_template", False),
                archived=json_response[repo_number].get("archived", False),
            )
        )
    queue_lock.release()
