import queue
import threading
from typing import Any

from cloner.repository import Repository


def put_repos_in_queue(
    json_response: list[dict[str, Any]],
    queue_lock: threading.Lock,
    repo_queue: queue.Queue,
    ignore_archived: bool,
    ignore_template: bool,
    ignore_fork: bool,
) -> None:
    """Puts into the queue repositories obtained from a list of dicts.

    Each element of the json_response is a dictionary containing the GitHub response with
    repository information.

    If ignore_archived is passed and the repo is archived, won't add it to the queue.

    Raises `KeyError` in case the `clone_url` in a response doesn't exist.
    """
    queue_lock.acquire()
    for repo_number in range(len(json_response)):
        is_repo_template = json_response[repo_number].get("is_template", False)
        is_repo_archived = json_response[repo_number].get("archived", False)
        is_repo_fork = json_response[repo_number].get("fork", False)
        if ignore_archived and is_repo_archived:
            continue
        if ignore_template and is_repo_template:
            continue
        if ignore_fork and is_repo_fork:
            continue
        repo_queue.put(
            Repository(
                name=json_response[repo_number].get("name", ""),
                clone_url=json_response[repo_number]["clone_url"],
                repo_id=repo_number,
                is_template=is_repo_template,
                archived=is_repo_archived,
                fork=is_repo_fork,
            )
        )
    queue_lock.release()
