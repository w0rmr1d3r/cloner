class Repository:
    """Class to abstract the needed attributes of a repository."""

    def __init__(self, name: str, clone_url: str, repo_id: int):
        self.name = name
        self.clone_url = clone_url
        self.repo_id = repo_id

    def __str__(self):
        return f"Repo: {self.name} URL: {self.clone_url}"

    def __eq__(self, other):
        if isinstance(other, Repository):
            return self.name == other.name and self.clone_url == other.clone_url and self.repo_id == other.repo_id
        return False
