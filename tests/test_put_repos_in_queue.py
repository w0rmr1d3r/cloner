import pytest
from pytest import raises

from cloner.put_repos_in_queue import put_repos_in_queue
from cloner.repository import Repository


@pytest.mark.parametrize(
    "json_response,expected_repository",
    [
        (
            [
                {
                    "name": "test_name",
                    "clone_url": "https://github.com/organisation/test_name.git",
                    "archived": False,
                    "is_template": False,
                    "fork": False,
                }
            ],
            Repository(
                name="test_name",
                clone_url="https://github.com/organisation/test_name.git",
                repo_id=0,
            ),
        ),
        (
            [
                {
                    "clone_url": "https://github.com/organisation/test_name.git",
                    "archived": False,
                    "is_template": False,
                    "fork": False,
                }
            ],
            Repository(name="", clone_url="https://github.com/organisation/test_name.git", repo_id=0),
        ),
    ],
)
def test_put_repos_into_queue(json_response, expected_repository, queue_lock, repository_list_queue):
    put_repos_in_queue(
        json_response=json_response,
        queue_lock=queue_lock,
        repo_queue=repository_list_queue,
        ignore_archived=False,
        ignore_template=False,
        ignore_fork=False,
        exclude_repos=[],
    )
    assert len(repository_list_queue.queue) == 1
    assert repository_list_queue.get() == expected_repository


def test_put_repos_into_queue_does_nothing_if_no_answer_obtained(queue_lock, repository_list_queue):
    test_json_response = []

    put_repos_in_queue(
        json_response=test_json_response,
        queue_lock=queue_lock,
        repo_queue=repository_list_queue,
        ignore_archived=False,
        ignore_template=False,
        ignore_fork=False,
        exclude_repos=[],
    )

    assert len(repository_list_queue.queue) == 0


def test_threads_below_1_raises_error(
    queue_lock,
    repository_list_queue,
):
    with raises(KeyError):
        put_repos_in_queue(
            json_response=[
                {
                    "name": "test_name",
                }
            ],
            queue_lock=queue_lock,
            repo_queue=repository_list_queue,
            ignore_archived=False,
            ignore_template=False,
            ignore_fork=False,
            exclude_repos=[],
        )


def test_put_repos_into_queue_full_github_answer(github_response_one_repo, queue_lock, repository_list_queue):
    expected = Repository(
        name="Hello-World",
        clone_url="https://github.com/octocat/Hello-World.git",
        repo_id=0,
        is_template=False,
        archived=False,
    )
    put_repos_in_queue(
        json_response=github_response_one_repo,
        queue_lock=queue_lock,
        repo_queue=repository_list_queue,
        ignore_archived=False,
        ignore_template=False,
        ignore_fork=False,
        exclude_repos=[],
    )
    assert len(repository_list_queue.queue) == 1
    assert repository_list_queue.get() == expected


def test_put_repos_into_queue_ignore_archived(queue_lock, repository_list_queue):
    response = [
        {"clone_url": "https://github.com/organisation/test_name.git", "archived": True},
        {"clone_url": "https://github.com/organisation/test_name.git", "archived": False},
    ]
    put_repos_in_queue(
        json_response=response,
        queue_lock=queue_lock,
        repo_queue=repository_list_queue,
        ignore_archived=True,
        ignore_template=False,
        ignore_fork=False,
        exclude_repos=[],
    )
    assert len(repository_list_queue.queue) == 1


def test_put_repos_into_queue_ignore_template(queue_lock, repository_list_queue):
    response = [
        {"clone_url": "https://github.com/organisation/test_name.git", "is_template": True},
        {"clone_url": "https://github.com/organisation/test_name.git", "is_template": False},
    ]
    put_repos_in_queue(
        json_response=response,
        queue_lock=queue_lock,
        repo_queue=repository_list_queue,
        ignore_archived=False,
        ignore_template=True,
        ignore_fork=False,
        exclude_repos=[],
    )
    assert len(repository_list_queue.queue) == 1


def test_put_repos_into_queue_ignore_fork(queue_lock, repository_list_queue):
    response = [
        {"clone_url": "https://github.com/organisation/test_name.git", "fork": True},
        {"clone_url": "https://github.com/organisation/test_name.git", "fork": False},
    ]
    put_repos_in_queue(
        json_response=response,
        queue_lock=queue_lock,
        repo_queue=repository_list_queue,
        ignore_archived=False,
        ignore_template=False,
        ignore_fork=True,
        exclude_repos=[],
    )
    assert len(repository_list_queue.queue) == 1


def test_put_repos_into_queue_exclude_repos(queue_lock, repository_list_queue):
    response = [
        {"clone_url": "https://github.com/organisation/test_name.git", "name": "repoa"},
        {"clone_url": "https://github.com/organisation/test_name.git", "name": "repob"},
        {"clone_url": "https://github.com/organisation/test_name.git", "name": "repoc"},
        {"clone_url": "https://github.com/organisation/test_name.git", "name": "repod"},
    ]
    put_repos_in_queue(
        json_response=response,
        queue_lock=queue_lock,
        repo_queue=repository_list_queue,
        ignore_archived=False,
        ignore_template=False,
        ignore_fork=False,
        exclude_repos=["repoc", "repob"],
    )
    assert len(repository_list_queue.queue) == 2
