import queue
import threading

from _pytest.fixtures import fixture

from cloner.put_repos_in_queue import put_repos_in_queue
from cloner.repository import Repository


@fixture()
def queue_lock():
    # todo - make this a "common" fixture
    return threading.Lock()


def test_put_repos_into_queue_puts_obtained_repos_as_repositories_into_a_given_queue(
    queue_lock,
):
    repository_list_queue = queue.Queue()  # todo - could this be a global fixture
    test_json_response = [
        {
            "name": "test_name",
            "clone_url": "https://github.com/organisation/test_name.git",
        }
    ]
    expected_repository = Repository(
        name="test_name",
        clone_url="https://github.com/organisation/test_name.git",
        repo_id=0,
    )

    put_repos_in_queue(
        json_response=test_json_response,
        queue_lock=queue_lock,
        repo_queue=repository_list_queue,
    )

    assert len(repository_list_queue.queue) == 1
    assert repository_list_queue.get() == expected_repository


def test_put_repos_into_queue_does_nothing_if_no_answer_obtained(queue_lock):
    repository_list_queue = queue.Queue()  # todo - could this be a global fixture
    test_json_response = []

    put_repos_in_queue(
        json_response=test_json_response,
        queue_lock=queue_lock,
        repo_queue=repository_list_queue,
    )

    assert len(repository_list_queue.queue) == 0
