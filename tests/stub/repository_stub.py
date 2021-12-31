from faker import Faker

from cloner.repository import Repository

fake = Faker()


def random_repository() -> Repository:
    name = fake.first_name()
    return Repository(
        name=name,
        clone_url=f"https://github.com/organization/{name}.git",
        repo_id=fake.random_number(digits=4, fix_len=False),
    )
