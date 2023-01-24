from _pytest.python_api import raises

from cloner.split_queue import ThreadsBelowOne, split_queue


def test_queue_of_1_repo_and_1_thread_returns_a_list_of_1_item_of_1_repo(
    queue_lock, repository_list_queue, random_repository
):
    queue_lock.acquire()
    repository_list_queue.put(random_repository)
    queue_lock.release()

    result = split_queue(
        number_of_threads=1,
        repository_queue=repository_list_queue,
        repository_queue_lock=queue_lock,
    )

    assert result == [[random_repository]]


def test_queue_of_1_repo_and_2_threads_returns_a_list_of_2_items_one_with_repo_other_empty(
    queue_lock,
    repository_list_queue,
    random_repository_odd_id,
    random_repository_even_id,
):
    queue_lock.acquire()
    repository_list_queue.put(random_repository_odd_id)
    repository_list_queue.put(random_repository_even_id)
    queue_lock.release()

    result = split_queue(
        number_of_threads=2,
        repository_queue=repository_list_queue,
        repository_queue_lock=queue_lock,
    )

    assert result == [[random_repository_even_id], [random_repository_odd_id]]


def test_threads_below_1_raises_error(
    queue_lock,
    repository_list_queue,
):
    with raises(ThreadsBelowOne):
        split_queue(
            number_of_threads=-1,
            repository_queue=repository_list_queue,
            repository_queue_lock=queue_lock,
        )


def test_empty_queue_returns_empty_list_of_lists_equal_to_threads(queue_lock, repository_list_queue):
    result = split_queue(
        number_of_threads=3,
        repository_queue=repository_list_queue,
        repository_queue_lock=queue_lock,
    )

    assert result == [[], [], []]
