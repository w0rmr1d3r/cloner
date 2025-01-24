from dataclasses import dataclass


@dataclass
class Repository:
    """Dataclass to abstract the only needed attributes of a repository."""

    name: str
    clone_url: str
    repo_id: int
    is_template: bool = False
    archived: bool = False
    fork: bool = False

    def __str__(self):
        return f"Repo: {self.name} URL: {self.clone_url}"

    def __eq__(self, other):
        if isinstance(other, Repository):
            return self.name == other.name and self.clone_url == other.clone_url and self.repo_id == other.repo_id
        return False

    def __hash__(self):
        return hash(self.name)
