import queue
import threading
from typing import Any

from click import progressbar

from cloner.repository import Repository


def put_repos_in_queue(  # noqa: PLR0913, PLR0917
    json_response: list[dict[str, Any]],
    queue_lock: threading.Lock,
    repo_queue: queue.Queue,
    ignore_archived: bool,
    ignore_template: bool,
    ignore_fork: bool,
    exclude_repos: list[str],
) -> None:
    """
    Puts into the queue repositories obtained from a list of dicts.

    Each element of the json_response is a dictionary containing the GitHub response with
    repository information.

    If ignore_archived is passed and the repo is archived, won't add it to the queue.

    Raises `KeyError` in case the `clone_url` in a response doesn't exist.
    """
    queue_lock.acquire()
    with progressbar(range(len(json_response)), label="Adding repos to queue") as bar:
        for repo_number in bar:
            is_repo_template = json_response[repo_number].get("is_template", False)
            is_repo_archived = json_response[repo_number].get("archived", False)
            is_repo_fork = json_response[repo_number].get("fork", False)
            repo_name = json_response[repo_number].get("name", "")
            if ignore_archived and is_repo_archived:
                continue
            if ignore_template and is_repo_template:
                continue
            if ignore_fork and is_repo_fork:
                continue
            if repo_name in exclude_repos:
                continue
            repo_queue.put(
                Repository(
                    name=repo_name,
                    clone_url=json_response[repo_number]["clone_url"],
                    repo_id=repo_number,
                    is_template=is_repo_template,
                    archived=is_repo_archived,
                    fork=is_repo_fork,
                )
            )
    queue_lock.release()
