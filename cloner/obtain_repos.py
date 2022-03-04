import queue
import threading

import requests

from cloner.put_repos_in_queue import put_repos_in_queue


def obtain_repos(
    github_organization: str,
    github_token: str,
    queue_lock: threading.Lock,
    repo_queue: queue.Queue,
) -> None:
    """
    Makes a request to the GitHub API and then passes that info to the queue.
    """
    github_url = f"https://api.github.com/orgs/{github_organization}/repos"
    headers = {"Accept": "application/vnd.github.v3+json"}

    if github_token is not None:
        headers["Authorization"] = f"token {github_token}"

    # TODO obtain more per page, so less calls are done
    response = requests.get(github_url, headers=headers)
    response.raise_for_status()
    json_response = response.json()

    while "next" in response.links.keys():
        response = requests.get(response.links["next"]["url"], headers=headers)
        json_response.extend(response.json())

    put_repos_in_queue(json_response, queue_lock, repo_queue)
