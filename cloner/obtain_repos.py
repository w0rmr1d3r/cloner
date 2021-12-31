import queue
import threading

import requests

from cloner.repository import Repository

# split into smaller functions


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
    response = requests.get(
        github_url, headers=headers
    )
    json_response = response.json()

    while "next" in response.links.keys():
        response = requests.get(response.links["next"]["url"], headers=headers)
        json_response.extend(response.json())

    put_repos_in_queue(json_response, queue_lock, repo_queue)


def put_repos_in_queue(json_response: dict, queue_lock: threading.Lock, repo_queue: queue.Queue) -> None:
    """
    Puts into the queue repositories obtained from a dictionary
    """
    queue_lock.acquire()
    # each element is a (public) repo, 30 per page
    for repo_number in range(len(json_response)):
        repo_queue.put(
            Repository(
                name=json_response[repo_number]["name"],
                clone_url=json_response[repo_number]["clone_url"],
                repo_id=repo_number,
            )
        )
    queue_lock.release()
