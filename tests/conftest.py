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
        repo_id=faker.random_number(digits=4, fix_len=False),
    )


@pytest.fixture
def queue_lock() -> threading.Lock:
    return threading.Lock()


@pytest.fixture
def repository_list_queue():
    return queue.Queue()
