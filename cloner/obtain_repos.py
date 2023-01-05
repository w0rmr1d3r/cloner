import logging
import queue
import threading

import requests

from cloner.put_repos_in_queue import put_repos_in_queue

logger = logging.getLogger(__file__)


def obtain_repos(
    github_organization: str,
    github_token: str,
    queue_lock: threading.Lock,
    repo_queue: queue.Queue,
) -> None:
    """
    Makes a request to the GitHub API and then passes that info to the queue.
    GitHub docs: https://docs.github.com/en/rest?apiVersion=2022-11-28
    """
    github_url = f"https://api.github.com/orgs/{github_organization}/repos"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    params = {"per_page": 100}

    if github_token is not None:
        headers["Authorization"] = f"token {github_token}"

    logger.debug("First call to GitHub")
    response = requests.get(github_url, headers=headers, params=params)
    response.raise_for_status()
    json_response = response.json()

    while "next" in response.links.keys():
        logger.debug("Keep calling GitHub")
        response = requests.get(
            response.links["next"]["url"], headers=headers, params=params
        )
        json_response.extend(response.json())

    logger.debug("Finished calling GitHub")
    put_repos_in_queue(json_response, queue_lock, repo_queue)
