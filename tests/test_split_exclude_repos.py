from cloner.split_exclude_repos import split_exclude_repos


def test_split_exclude_repos_splits_a_repo():
    given_input = "repoa"
    expected_output = ["repoa"]

    result = split_exclude_repos(exclude_repos=given_input)

    assert expected_output == result


def test_split_exclude_repos_splits_several_repos():
    given_input = "repoa,repob,repoc"
    expected_output = ["repoa", "repob", "repoc"]

    result = split_exclude_repos(exclude_repos=given_input)

    assert expected_output == result


def test_split_exclude_repos_splits_repos_final_comma():
    given_input = "repoa,repob,repoc,"
    expected_output = ["repoa", "repob", "repoc"]

    result = split_exclude_repos(exclude_repos=given_input)

    assert expected_output == result


def test_split_exclude_repos_splits_empty_input():
    given_input = ""
    expected_output = []

    result = split_exclude_repos(exclude_repos=given_input)

    assert expected_output == result


def test_split_exclude_repos_splits_one_comma_input():
    given_input = ","
    expected_output = []

    result = split_exclude_repos(exclude_repos=given_input)

    assert expected_output == result


def test_split_exclude_repos_splits_several_comma_input():
    given_input = ",,,,,,,"
    expected_output = []

    result = split_exclude_repos(exclude_repos=given_input)

    assert expected_output == result
