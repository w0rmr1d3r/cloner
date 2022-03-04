from _pytest.fixtures import fixture

from cloner.repository import Repository


@fixture
def random_repository(faker) -> Repository:
    name = faker.first_name()
    return Repository(
        name=name,
        clone_url=f"https://github.com/organization/{name}.git",
        repo_id=faker.random_number(digits=4, fix_len=False),
    )


def test_repository_as_string(random_repository):
    name = random_repository.name
    assert (
        random_repository.__str__()
        == f"Repo: {name} URL: https://github.com/organization/{name}.git"
    )


def test_repository_can_be_compared(faker):
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
