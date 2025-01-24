def split_exclude_repos(exclude_repos: str) -> list[str]:
    """
    Splits the given str of repos to exclude to a list of repos.

    Expects a str of comma separated values. The return list can be an empty list if the
    given input is an empty str.
    """
    result = []
    for repo in exclude_repos.split(","):
        if repo:
            result.append(repo)
    return result
