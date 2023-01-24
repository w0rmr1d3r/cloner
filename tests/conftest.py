import queue
import threading

import pytest

from cloner.repository import Repository


@pytest.fixture
def random_repository(faker) -> Repository:
    name = faker.first_name()
    return Repository(
        name=name,
        clone_url=f"https://github.com/organization/{name}.git",
        repo_id=faker.random_number(digits=4),
    )


@pytest.fixture
def random_repository_even_id(faker) -> Repository:
    name = faker.first_name()
    return Repository(
        name=name,
        clone_url=f"https://github.com/organization/{name}.git",
        repo_id=2,
    )


@pytest.fixture
def random_repository_odd_id(faker) -> Repository:
    name = faker.first_name()
    return Repository(
        name=name,
        clone_url=f"https://github.com/organization/{name}.git",
        repo_id=1,
    )


@pytest.fixture
def queue_lock() -> threading.Lock:
    return threading.Lock()


@pytest.fixture
def repository_list_queue():
    return queue.Queue()
