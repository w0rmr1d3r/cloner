from cloner.repository import Repository


def test_repository_as_string(random_repository):
    name = random_repository.name
    assert str(random_repository) == f"Repo: {name} URL: https://github.com/organization/{name}.git"


def test_repository_can_be_compared():
    repository_one = Repository(
        name="repo_one",
        clone_url="https://github.com/organization/repo_one.git",
        repo_id=1,
    )
    repository_other = Repository(
        name="repo_one",
        clone_url="https://github.com/organization/repo_one.git",
        repo_id=1,
    )
    assert repository_one == repository_other


def test_repository_can_be_compared_and_is_different():
    repository_one = Repository(
        name="repo_one",
        clone_url="https://github.com/organization/repo_one.git",
        repo_id=2,
    )
    repository_other = Repository(
        name="repo_one",
        clone_url="https://github.com/organization/repo_one.git",
        repo_id=1,
    )
    assert repository_one != repository_other


def test_repository_can_be_compared_and_is_false_when_compared_to_another_object():
    repository_one = Repository(
        name="repo_one",
        clone_url="https://github.com/organization/repo_one.git",
        repo_id=2,
    )
    assert repository_one != int(1)
