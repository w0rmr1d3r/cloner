import logging
from typing import Any, Optional

import requests

logger = logging.getLogger(__file__)


class TokenNotFoundForGHEException(Exception):
    """Exception to be thrown when token isn't provided to use GHE."""

    def __init__(self, message="A token is needed when cloning from a GHE server"):
        super().__init__(message)


def obtain_repos(
    github_organization: str,
    github_token: Optional[str],
    ghe: Optional[str] = None,
) -> list[dict[str, Any]]:
    """
    Makes a request to the GitHub API to obtain the repos.

    Info is returned as a list of dicts.

    GitHub Public API docs: https://docs.github.com/en/rest?apiVersion=2022-11-28.
    Calling: https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#list-organization-repositories

    GitHub Enterprise docs: https://docs.github.com/en/enterprise-server@3.7
    Or any other version that applies
    """
    if ghe:
        if github_token is None:
            raise TokenNotFoundForGHEException
        github_url = f"https://{ghe}/api/v3/orgs/{github_organization}/repos"
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {github_token}",
        }
    else:
        github_url = f"https://api.github.com/orgs/{github_organization}/repos"
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if github_token:
            headers["Authorization"] = f"token {github_token}"

    timeout_seconds = 60
    params = {"per_page": 100}

    logger.debug("First call to GitHub")
    response = requests.get(github_url, headers=headers, params=params, timeout=timeout_seconds)
    response.raise_for_status()
    json_response = response.json()

    while "next" in response.links.keys():
        logger.debug("Keep calling GitHub")
        response = requests.get(response.links["next"]["url"], headers=headers, params=params, timeout=timeout_seconds)
        json_response.extend(response.json())

    logger.debug("Finished calling GitHub")
    return json_response
